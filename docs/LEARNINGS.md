# Learnings

## 2026-04-24: SDK starts as a greenfield package

The repository currently contains only project instructions, so the SDK can be
structured from first principles around MailChannels Email API behavior rather
than preserving an existing implementation. The first implementation should make
`/send-async` and sub-account operations first-class because those are
MailChannels-specific differentiators rather than secondary endpoints.

## 2026-04-24: uv pytest is not a native uv command

The current uv CLI rejects `uv pytest` as an unknown subcommand. The SDK uses
the portable pytest harness `uv run pytest` instead. SmolVM tests can run by
copying a tar archive of the working tree into a Python VM because direct
SmolVM bind mounts appeared empty in this macOS sandbox.
