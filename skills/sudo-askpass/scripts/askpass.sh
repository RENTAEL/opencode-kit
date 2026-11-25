#!/usr/bin/env bash
# askpass helper for `sudo -A`: pops a password dialog on the desktop session.
# Prints the entered password to stdout for sudo; never logs or stores it.
set -euo pipefail

MSG="${SUDO_ASKPASS_MSG:-DrewR: sudo needs your password}"
TIMEOUT="${SUDO_ASKPASS_TIMEOUT:-180}"

user="${SUDO_USER:-${USER:-$(id -un)}}"

has_gui() { [[ -n "${DISPLAY:-}" || -n "${WAYLAND_DISPLAY:-}" ]]; }

# Calling shell has no display? Inherit the session env from plasmashell.
if ! has_gui; then
  pid="$(pgrep -u "$user" -x plasmashell | head -n1 || true)"
  if [[ -n "$pid" && -r "/proc/$pid/environ" ]]; then
    while IFS='=' read -r key value; do
      case "$key" in
        DISPLAY|WAYLAND_DISPLAY|XDG_RUNTIME_DIR|DBUS_SESSION_BUS_ADDRESS|XAUTHORITY|XDG_SESSION_TYPE)
          export "$key=$value" ;;
      esac
    done < "/proc/$pid/environ"
  fi
fi

# kdialog (26.08.0) has no --timeout option: blocks until answered/cancelled.
if has_gui && command -v kdialog >/dev/null 2>&1; then
  exec kdialog --title 'sudo' --password "$MSG"
fi

if has_gui && command -v zenity >/dev/null 2>&1; then
  exec zenity --password "--timeout=$TIMEOUT" '--title=sudo'
fi

# Last resort: real tty only. Without a tty, systemd-ask-password queues the
# query for an agent that may never answer -> would hang forever.
if [[ -t 0 ]] && command -v systemd-ask-password >/dev/null 2>&1; then
  exec systemd-ask-password "--timeout=$TIMEOUT" "$MSG"
fi

echo "sudo_askpass: no usable prompt backend (no display, no tty)" >&2
exit 1
