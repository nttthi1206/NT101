import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = os.urandom(16)
iv = os.urandom(16)
data = os.urandom(1000)           # 1. Tao du lieu 1000 byte
padded = pad(data, 16)            # 1008 byte = 63 khoi (ECB/CBC bat buoc phai co padding)

def new_cipher(mode):
    if mode == "ECB": return AES.new(key, AES.MODE_ECB)
    if mode == "CBC": return AES.new(key, AES.MODE_CBC, iv=iv)
    if mode == "CFB": return AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
    if mode == "OFB": return AES.new(key, AES.MODE_OFB, iv=iv)

print(f"Du lieu: {len(data)} byte, sau padding: {len(padded)} byte ({len(padded)//16} khoi)\n")

for mode in ["ECB", "CBC", "CFB", "OFB"]:
    # 2. Mã hoa AES-128
    ct = bytearray(new_cipher(mode).encrypt(padded))

    # 3. Đao 1 bit tai byte thu 26 (chi so 25)
    ct[25] ^= 0x01

    # 4. Giai ma va đem khoi bi hong
    dec = new_cipher(mode).decrypt(bytes(ct))
    bad_blocks = [i for i in range(len(padded) // 16)
                  if dec[i*16:(i+1)*16] != padded[i*16:(i+1)*16]]
    bad_bytes = sum(a != b for a, b in zip(dec, padded))
    bad_bits = sum(bin(a ^ b).count("1") for a, b in zip(dec, padded))

    print(f"{mode}: {len(bad_blocks)} khoi hong {bad_blocks} | {bad_bytes} byte sai | {bad_bits} bit sai")