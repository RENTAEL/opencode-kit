---
name: sudo-askpass
description: "Prompts the user for their sudo password via a desktop dialog and feeds it to `sudo -A`. The password travels only between the dialog and sudo's stdin pipe."
---
# sudo_askpass

Prompts the user for their sudo password via a desktop dialog and feeds it to
`sudo -A`. The password travels only between the dialog and sudo's stdin pipe.

## Hard rules

1. NEVER ask the user to paste their password into chat.
2. NEVER run plain interactive `sudo` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this agent has no controlling tty, so
   it blocks forever. Always go through `sudo -A`.
3. If a command fails with "a password is required", retry once through the
   askpass flow below before reporting failure.
4. Announce that a password dialog is about to pop up and the reason for why sudo is needed so the user stays informed and in control.

## Usage

    export SUDO_ASKPASS=$HOME/.config/opencode/skills/sudo_askpass/scripts/askpass.sh
    sudo -A <command>

or one-shot:

    SUDO_ASKPASS=$HOME/.config/opencode/skills/sudo_askpass/scripts/askpass.sh

## Backend chain (verified on this machine)

1. `kdialog --password` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â primary; KDE Wayland session (plasmashell)
2. `zenity --password` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fallback
3. `systemd-ask-password` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ONLY when stdin is a real tty. Without a tty it
   enqueues the query for an ask-password agent that nothing on this desktop
   answers, so the script deliberately refuses that path.

The script inherits DISPLAY/WAYLAND/DBus/XDG_RUNTIME_DIR from the running
plasmashell process if the calling shell lacks them. zenity dialogs time out
after 180s (`SUDO_ASKPASS_TIMEOUT` overrides); kdialog has no timeout support
(verified on kdialog 26.08.0) and blocks until answered or cancelled.
Cancel/timeout exits non-zero and sudo fails cleanly instead of hanging.
