---
title: Serial Check
event: Self-authored practice challenge
category: rev
date: 2026-09-30
points: 0
---

# self-authored-serial-check

Not from a real competition — a small crackme I wrote myself to have a concrete, honest example of the reversing workflow, since I didn't want to publish "solved" writeups for challenges I hadn't actually solved. `crackme.c` is the source; `crackme.exe` is the compiled binary (`gcc -O0`, x86-64, Windows PE).

The program takes one argument. If it's the right 8-character serial, it prints a flag.

## Step 1 — the easy way out

Before touching a disassembler:

```
$ strings crackme.exe | grep flag
flag{that_was_addition_and_xor_all_along}
```

The success string sits in `.rdata` in plain text. `strings` alone gets the flag — the check logic never needed reversing at all. Worth remembering: an obfuscated *check* doesn't protect a plaintext *string reference* sitting right next to it.

## Step 2 — reversing the check anyway

Assuming the flag was fetched dynamically instead (network, decrypted at runtime, whatever), the check function needs reversing for real. Disassembly (`objdump -M intel -d`) of `check()`:

```
140001450 <check>:
  ...
  14000145c: movabs rax, 0xf02c7a0199423713      ; key[8], little-endian
  14000146a: movabs rax, 0x2afeb36ddefcb61        ; target[8], little-endian
  ...
  1400014ad: mov  rdx, [rbp+0x10]      ; input pointer
  1400014b8: movzx eax, [rax]          ; input[i]
  1400014c8: movzx eax, [rax]          ; key[i]
  1400014cb: lea  edx, [rcx+rax*1]     ; input[i] + key[i]
  1400014d9: movzx eax, [rbp+rax*1-0x19]  ; key[(i+1) % 8]
  1400014de: xor  eax, edx             ; (input[i] + key[i]) ^ key[(i+1) % 8]
  1400014f1: cmp  [rbp-0x11], al       ; compare against target[i]
```

So per byte: `scrambled[i] = (input[i] + key[i]) ^ key[(i+1) % 8]`, compared against a fixed 8-byte `target`. Both `key` and `target` are loaded as two `movabs` immediates (little-endian 8-byte blocks) right at the top of the function — pull them straight out of the disassembly, no need to dump memory at runtime.

## Step 3 — invert it

Addition and XOR both invert cleanly:

```
input[i] = (target[i] ^ key[(i+1) % 8]) - key[i]   (mod 256)
```

`solve.py` implements exactly that and prints the serial:

```
$ python solve.py
CR4CKM3!

$ ./crackme.exe CR4CKM3!
flag{that_was_addition_and_xor_all_along}
```

## Files

- `crackme.c` — source
- `crackme.exe` — the compiled binary that was actually reversed above
- `solve.py` — recovers the serial from the disassembled constants
