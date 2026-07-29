# Platforms

The scaffold is files only, so the differences between operating systems are
paths and line endings, nothing more. Detect the OS yourself; do not ask.

## Windows 11

- `HOME` is the user profile folder: `C:\Users\<name>` (`%USERPROFILE%` in
  cmd/PowerShell, `~` in Git Bash). `HOME/.claude/CLAUDE.md` means
  `C:\Users\<name>\.claude\CLAUDE.md`.
- Claude Code on Windows runs shell steps under Git Bash, so forward-slash
  paths work inside the agent. When you PRINT a path for the person to open
  themselves, print the backslash form, because that is what Explorer and
  their editor expect.
- Write files with LF line endings and let their editor handle the rest. Do
  not add `.gitattributes` or touch git config; the personal layer is not a
  repo.
- Nothing here uses launchd, cron, services, or Task Scheduler. If a future
  layer wants scheduling, it is opt-in and documented, never assumed.
- Dot-folders (`.claude`) are fine on Windows; Explorer shows them normally.

## macOS / Linux

- `HOME` is `~`. Everything else reads exactly as written in
  [scaffold.md](scaffold.md).
- No launchd agents, no cron entries. Files only.

## Both

- Create parent folders as needed; never assume they exist.
- If the person's home folder syncs to a cloud drive (OneDrive redirects
  Documents on many Windows machines), the dot-folders in the user profile
  root are normally outside that sync. That is the behavior we want: personal
  memory stays on the machine unless the person moves it deliberately.
