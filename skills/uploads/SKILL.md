---
name: daily-morning-brief
description: Daily morning briefing (calendar, email, Teams, Zoho Desk) at 8:30 AM SAST on weekdays
---
Invoke the "morning" skill to render the user's morning brief as a styled HTML artifact. This is an unattended scheduled run, so skip any interactive setup, connector-suggestion cards, or clarifying questions — just gather the data and render the brief per the skill's instructions.

Write the brief in English.

Sources to use (per the skill's Gather step):
- Calendar: Outlook Calendar (mcp__...__outlook_calendar_search), today 00:00 to tomorrow 00:00 in Africa/Johannesburg time. This drives the visual anchor/terrain and Acts.
- Email: Outlook (mcp__...__outlook_email_search), Inbox — find threads where the user was asked something directly and hasn't replied (check Sent Items to confirm no reply went out); fallback to unread in the last 2 days.
- Chat: Microsoft Teams (mcp__...__chat_message_search) — mentions/DMs to the user from the last ~2 days that end in a question they haven't answered or reacted to.
- Zoho Desk support tickets: scope to the IT Support department and the current user's agent id from the Zoho connector config. Use searchTickets scoped to that department, modifiedTimeRange covering the last ~3 days. Treat tickets assigned to the user with status "Pending Support" (i.e. last thread direction "in", waiting on them) and no recent reply as Needs attention candidates — pull the latest thread via getThreads for a verbatim quote of the ask. Tickets that moved to "Pending Customer", "Resolved", or "Closed" recently, or where the user sent the most recent outbound thread, are Resolved candidates (e.g. "ticket handed off to X, now waiting on them").

Sort everything into Needs attention / Resolved exactly as the skill describes (cost of ignoring today, verified against the source, quotes verbatim). Follow the skill's Write, Build, and Verify steps exactly, including embedding the Fraunces font from the skill's assets/fonts directory as base64, and screenshotting the result to check rendering before finishing if a browser is available in the sandbox.

Save the finished HTML file to the outputs folder so the user can open it.