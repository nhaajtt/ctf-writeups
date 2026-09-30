#!/usr/bin/env python3
"""Break repeating-key XOR on ciphertext.bin:

1. Guess the key length with normalized Hamming distance between blocks
   (the classic approach — for the right key length, XOR-ing two blocks
   cancels the key and leaves plaintext-vs-plaintext distance, which is
   lower than for a wrong length).
2. Split the ciphertext into `key_length` columns (byte i, i+len, i+2*len...)
   and solve each column as an independent single-byte XOR, scored by an
   English letter-frequency heuristic.
3. Reassemble the key and decrypt.
"""

import string
from itertools import combinations

_ENGLISH_FREQ = {
    "e": 12.7, "t": 9.1, "a": 8.2, "o": 7.5, "i": 7.0, "n": 6.7, "s": 6.3,
    "h": 6.1, "r": 6.0, "d": 4.3, "l": 4.0, "c": 2.8, "u": 2.8, "m": 2.4,
    "w": 2.4, "f": 2.2, "g": 2.0, "y": 2.0, "p": 1.9, "b": 1.5, "v": 1.0,
    "k": 0.8, "j": 0.15, "x": 0.15, "q": 0.10, "z": 0.07,
}
_PRINTABLE = set(bytes(string.printable, "ascii"))


def score(data: bytes) -> float:
    if not data:
        return 0.0
    total = 0.0
    for b in data:
        ch = chr(b).lower()
        if ch in _ENGLISH_FREQ:
            total += _ENGLISH_FREQ[ch]
        elif b in _PRINTABLE:
            total += 0.5
        else:
            total -= 3.0
    return total / len(data)


def hamming(a: bytes, b: bytes) -> int:
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


def guess_key_length(ct: bytes, max_len: int = 40, max_blocks: int = 20):
    best = []
    for size in range(2, max_len + 1):
        num_blocks = min(max_blocks, len(ct) // size)
        blocks = [ct[i * size:(i + 1) * size] for i in range(num_blocks)]
        if len(blocks) < 2:
            continue
        distances = [hamming(a, b) / size for a, b in combinations(blocks, 2)]
        avg = sum(distances) / len(distances)
        best.append((avg, size))
    best.sort()
    return best


def break_single_byte_column(column: bytes) -> int:
    best_key, best_score = 0, float("-inf")
    for key in range(256):
        decoded = bytes(b ^ key for b in column)
        s = score(decoded)
        if s > best_score:
            best_score, best_key = s, key
    return best_key


def solve(ct: bytes, key_length: int) -> bytes:
    key = bytes(
        break_single_byte_column(ct[i::key_length])
        for i in range(key_length)
    )
    return key


if __name__ == "__main__":
    with open("ciphertext.bin", "rb") as f:
        ct = f.read()

    candidates = guess_key_length(ct)
    print("key length candidates (lower = more likely), top 5:")
    for avg, size in candidates[:5]:
        print(f"  size={size:3d}  avg_hamming={avg:.3f}")

    best_size = candidates[0][1]
    key = solve(ct, best_size)
    plaintext = bytes(b ^ key[i % len(key)] for i, b in enumerate(ct))

    print(f"\nrecovered key: {key!r}")
    print(f"plaintext: {plaintext.decode('ascii', 'replace')}")
