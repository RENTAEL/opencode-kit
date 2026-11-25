# Security Policy

## Reporting a vulnerability
This project is a set of Markdown instructions (a Claude Code / Agent Skill); it
ships no executable server code. Still, if you find a security-relevant issue -
for example a prompt pattern that could cause an agent to leak data or take
unsafe actions - please report it responsibly.

- **Email:** arushmukundan@gmail.com
- Please do **not** open a public issue for sensitive reports.
- Include steps to reproduce and the potential impact.

You can expect an acknowledgement within a few days.

## Supported versions
The latest release on the `main` branch is supported.

## Safe-use note
This skill instructs an AI agent. Review skills before trusting them in your
environment, and be mindful of `allowed-tools` grants when running agent skills
in a project.
