# ctf-writeups

Write-ups for CTF challenges I have solved, mostly reverse engineering and binary exploitation. Each one
explains the method, not only the flag: what I looked at first, what did not work, and what the challenge
was really testing.

## Index

<!-- index:start -->
No write-ups yet.
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
