---
title: Repeating XOR
event: Self-authored practice challenge
category: crypto
date: 2026-09-30
points: 0
---

# self-authored-repeating-xor

Not from a real competition — a repeating-key XOR challenge I generated myself (`make_challenge.py`) so I'd have an honest writeup of the classic Hamming-distance attack, run against ciphertext I could actually verify byte-for-byte.

`ciphertext.bin` is ~1.3 KB of English text, XOR'd against a repeating key the solver never sees.

## Step 1 — guess the key length

Two ciphertext blocks that both start at the same offset within the key's repeating period were XOR'd with the *same* key bytes, so XOR-ing those two blocks together cancels the key out and leaves plaintext-XOR-plaintext. English text XOR'd with English text has a lower average Hamming distance (bits differing per byte) than random data does — so scanning candidate key lengths and taking the average normalized Hamming distance across several block pairs should show a dip at the real key length.

```
$ python solve.py
key length candidates (lower = more likely), top 5:
  size= 30  avg_hamming=2.634
  size= 36  avg_hamming=2.653
  size= 12  avg_hamming=2.666
  size= 18  avg_hamming=2.668
  size= 24  avg_hamming=2.692
```

The real key is 6 bytes, but the lowest-distance candidate here is 30 — a multiple of 6, not 6 itself. That's expected: any multiple of the true key length also aligns blocks to the same key bytes, so it cancels just as cleanly, and with more repeats the averaging is even more stable. In practice this doesn't matter for step 2.

## Step 2 — solve each column as single-byte XOR

Split the ciphertext into `key_length` interleaved columns (byte `i`, `i + key_length`, `i + 2*key_length`, ...). Every byte in one column was XOR'd with the exact same key byte, so each column is an ordinary single-byte-XOR problem — brute force all 256 candidates per column, score by English letter frequency (same heuristic as [`xor-bruteforce`](../../../re-tools/xor-bruteforce) in re-tools), keep the best.

## Step 3 — the harmonic key still works

Because 30 is a multiple of 6, solving with `key_length = 30` doesn't recover garbage — it recovers `shadowshadowshadowshadowshadow`, i.e. the real 6-byte key `shadow` repeated 5 times. XOR-ing the ciphertext against that 30-byte key is identical to XOR-ing it against the real 6-byte key on a repeating basis, so decryption succeeds either way:

```
recovered key: b'shadowshadowshadowshadowshadow'
plaintext: the flag is flag{vigenere_never_really_left_us}. repeating key xor is just
vigenere over bytes instead of letters, ...
```

Lesson worth keeping: the Hamming-distance step doesn't have to land on the *exact* key length to succeed — a clean multiple of it decrypts correctly too, since the recovered "key" is just the true key tiled.

## Files

- `make_challenge.py` — generates `ciphertext.bin` from a plaintext and a secret key (run once, not part of solving)
- `ciphertext.bin` — the challenge file
- `solve.py` — key-length guess, per-column brute force, decryption
