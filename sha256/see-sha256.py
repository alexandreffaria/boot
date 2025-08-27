import struct

# === SHA-256 constants ===

# First 32 bits of the fractional parts of the cube roots of the first 64 primes
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# Initial hash values
def initial_hash_values():
    return [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

def rotr(x, n):
    return (x >> n | x << (32 - n)) & 0xFFFFFFFF

def pad_message(message):
    print("\n=== Padding ===")
    message_bytes = message.encode('utf-8')
    message_bit_len = len(message_bytes) * 8
    print(f"Original message length: {len(message_bytes)} bytes, {message_bit_len} bits")

    # Append '1' bit and then pad with '0's until message is 448 mod 512 bits
    message_bytes += b'\x80'
    while (len(message_bytes) * 8) % 512 != 448:
        message_bytes += b'\x00'

    # Append 64-bit big-endian message length
    message_bytes += struct.pack('>Q', message_bit_len)

    print(f"Padded message length: {len(message_bytes)} bytes ({len(message_bytes) * 8} bits)")
    return message_bytes

def process_block(block, h):
    print("\n=== Message Schedule (w[0..63]) ===")
    w = []

    # Break block into sixteen 32-bit big-endian words
    for i in range(16):
        word = struct.unpack('>I', block[i*4:i*4+4])[0]
        w.append(word)
        print(f"w[{i:2}] = {word:08x} ({word})")

    # Extend to 64 words
    for i in range(16, 64):
        s0 = rotr(w[i-15], 7) ^ rotr(w[i-15], 18) ^ (w[i-15] >> 3)
        s1 = rotr(w[i-2], 17) ^ rotr(w[i-2], 19) ^ (w[i-2] >> 10)
        word = (w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF
        w.append(word)
        print(f"w[{i:2}] = {word:08x} ({word})")

    a, b, c, d, e, f, g, h0 = h

    print("\n=== Compression Rounds ===")
    for i in range(64):
        S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
        ch = (e & f) ^ (~e & g)
        temp1 = (h0 + S1 + ch + K[i] + w[i]) & 0xFFFFFFFF
        S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (S0 + maj) & 0xFFFFFFFF

        h0 = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF

        print(f"Round {i:02}:")
        print(f"  a={a:08x}, b={b:08x}, c={c:08x}, d={d:08x}")
        print(f"  e={e:08x}, f={f:08x}, g={g:08x}, h={h0:08x}")
        print("")

    # Add the compressed chunk to the current hash value
    final = [
        (x + y) & 0xFFFFFFFF for x, y in zip([a, b, c, d, e, f, g, h0], h)
    ]

    print("\n=== Final Hash Values ===")
    for i, val in enumerate(final):
        print(f"h{i} = {val:08x} ({val})")

    return final

def sha256_verbose(message):
    print(f"\n==== SHA-256: Processing message '{message}' ====")
    h = initial_hash_values()
    print("\n=== Initial Hash Values ===")
    for i, val in enumerate(h):
        print(f"h{i} = {val:08x} ({val})")

    padded = pad_message(message)

    # Only works for 1 block
    assert len(padded) == 64, "Only 1 block supported in this demo"
    h = process_block(padded, h)

    digest = ''.join(f'{val:08x}' for val in h)
    print(f"\n=== Final Digest ===\n{digest}")
    return digest

# Run it
sha256_verbose("boot.dev")
