# ctf-writeups

Write-ups for CTF challenges I have solved, mostly reverse engineering and binary exploitation. Each one
explains the method, not only the flag: what I looked at first, what did not work, and what the challenge
was really testing.

## Index

<!-- index:start -->
| Date | Event | Challenge | Category |
|---|---|---|---|
| 2026-09-30 | Self-authored practice challenge | [Repeating XOR](writeups/self-authored/self-authored-repeating-xor/README.md) | crypto |
| 2026-09-30 | Self-authored practice challenge | [ret2win](writeups/self-authored/self-authored-ret2win/README.md) | pwn |
| 2026-09-30 | Self-authored practice challenge | [Serial Check](writeups/self-authored/self-authored-serial-check/README.md) | rev |
<!-- index:end -->

## Layout

```
writeups/
  <event>/
    <challenge>.md
```

Each write-up starts with a short header (title, event, category, date) that the index is built from. Start
from [TEMPLATE.md](TEMPLATE.md) or run:

```
node scripts/new.mjs "<event>" "<challenge>" rev
```

Push to `master` and the index above updates itself.

## Rules

Read [RULES.md](RULES.md) before publishing. In short: only after the event has ended, never with live
malware or private data, and always credit the team.

## License

MIT for the scripts and templates. Write-ups may be shared with credit to the author.
