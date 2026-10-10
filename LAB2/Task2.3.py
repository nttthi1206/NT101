"""Nhiệm vụ 2.3 - Hiệu ứng thác đổ (Avalanche) của DES."""
from Crypto.Cipher import DES


def to_bits(data: bytes) -> str:
    """Chuyển bytes sang chuỗi nhị phân, đủ 8 bit mỗi byte."""
    return bin(int.from_bytes(data, "big"))[2:].zfill(len(data) * 8)


def hamming(b1: bytes, b2: bytes) -> int:
    """Hamming Distance: số bit khác nhau giữa hai chuỗi bytes cùng độ dài."""
    return sum(x != y for x, y in zip(to_bits(b1), to_bits(b2)))


def des_ecb(key: bytes, data: bytes) -> bytes:
    return DES.new(key, DES.MODE_ECB).encrypt(data)


def avalanche_test(key: bytes, p1: bytes, p2: bytes):
    """Mã hóa p1, p2 cùng một key, so sánh hai bản mã."""
    c1, c2 = des_ecb(key, p1), des_ecb(key, p2)
    d = hamming(c1, c2)
    total = len(c1) * 8
    print(f"Key = {key.decode()}")
    print(f"  C1 = {c1.hex()}  ({to_bits(c1)})")
    print(f"  C2 = {c2.hex()}  ({to_bits(c2)})")
    print(f"  Hamming Distance = {d}/{total} bit -> {d / total * 100:.2f}%\n")
    return d, total


def key_avalanche(p: bytes, k1: bytes, k2: bytes):
    """Cùng một bản rõ, đổi key: so sánh hai bản mã."""
    c1, c2 = des_ecb(k1, p), des_ecb(k2, p)
    d = hamming(c1, c2)
    dk = hamming(k1, k2)
    print(f"Key {k1.decode()} vs {k2.decode()}: key khác {dk} bit, "
          f"bản mã khác {d}/64 bit -> {d / 64 * 100:.2f}%")


if __name__ == "__main__":
    p1 = b"STAYHOME"
    p2 = b"STAYHOMA"   # chỉ khác 1 ký tự cuối so với p1
    print(f"Hamming distance giữa p1 và p2: {hamming(p1, p2)} bit\n")

    keys = [b"87654321", b"24521654", b"24521726"]   # key gốc + 2 MSSV
    results = []
    for k in keys:
        results.append(avalanche_test(k, p1, p2))

    avg = sum(d for d, _ in results) / sum(t for _, t in results) * 100
    print(f"Trung bình tỷ lệ bit thay đổi: {avg:.2f}%\n")

    print("--- Thử thêm: cùng bản rõ, đổi key ---")
    key_avalanche(p1, keys[1], keys[2])
    key_avalanche(p2, keys[1], keys[2])