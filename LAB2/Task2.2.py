from Crypto.Cipher import AES

key = b'1234567890123456'                      # 16 byte = AES-128
iv = b'abcdefghijklmnop'                       # IV co đinh, 16 byte
nonce = b'12345678'                            # nonce cho CTR, 8 byte
plaintext = b"UIT_LAB_UIT_LAB_UIT_LAB_UIT_LAB_"  # 32 byte = 2 khoi

print("Plaintext:", plaintext.hex(), f"({len(plaintext)} byte)\n")

# ma hoa bang 5 mode
results = {
    "ECB": AES.new(key, AES.MODE_ECB).encrypt(plaintext),
    "CBC": AES.new(key, AES.MODE_CBC, iv=iv).encrypt(plaintext),
    "CFB": AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128).encrypt(plaintext),
    "OFB": AES.new(key, AES.MODE_OFB, iv=iv).encrypt(plaintext),
    "CTR": AES.new(key, AES.MODE_CTR, nonce=nonce).encrypt(plaintext),
}

# In hex và so sanh cac khoi 16 byte
for name, ct in results.items():
    b1, b2 = ct[:16], ct[16:32]
    print(f"{name}: {ct.hex()}")
    print(f"   Block 1: {b1.hex()}")
    print(f"   Block 2: {b2.hex()}")
    print(f"   Hai khoi giong nhau: {b1 == b2}\n")

# Thêm: CBC voi IV toan 0, de doi chieu voi ket qua trong JCrypTool
ct0 = AES.new(key, AES.MODE_CBC, iv=bytes(16)).encrypt(plaintext)
print("CBC (IV toan 0):", ct0.hex())
