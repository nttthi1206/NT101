"Nhóm 5: Nhiệm vụ 2.1"


def F(right, subkey):
    "Hàm F nội bộ: XOR nửa phải với khóa con, giữ lại 4 bit thấp."
    return (right ^ subkey) & 0x0F


def feistel_round(L_in, R_in, subkey):
    """Một vòng Feistel:
       LE_i = RE_{i-1}
       RE_i = LE_{i-1} XOR F(RE_{i-1}, K_i)
    """
    L_out = R_in
    R_out = L_in ^ F(R_in, subkey)
    return L_out, R_out


def hamming(a, b):
    """Số bit khác nhau giữa hai giá trị."""
    return bin(a ^ b).count("1")


def track_avalanche(msg, key):
    """Mã hóa 4 vòng Feistel, in (L, R) sau mỗi vòng.
       Trả về danh sách trạng thái 8 bit (L<<4 | R) sau mỗi vòng."""
    L, R = (msg >> 4) & 0x0F, msg & 0x0F
    subkeys = [key & 0x0F, (key >> 4) & 0x0F, (key + 1) & 0x0F, (key + 2) & 0x0F]
    states = [(L << 4) | R]
    print(f"Khởi tạo: L={format(L, '04b')}, R={format(R, '04b')}")
    for i in range(4):
        L, R = feistel_round(L, R, subkeys[i])
        states.append((L << 4) | R)
        print(f"Vòng {i+1}: L={format(L, '04b')}, R={format(R, '04b')}  (K{i+1}={format(subkeys[i], '04b')})")
    return states


if __name__ == "__main__":
    KEY = 0x12
    print("--- Mã hóa M1 = 0xAB ---")
    s1 = track_avalanche(0xAB, KEY)
    print("\n--- Mã hóa M2 = 0xAC ---")
    s2 = track_avalanche(0xAC, KEY)

    print("\n--- So sánh M1 và M2 qua từng vòng ---")
    print(f"{'Bước':<10}{'M1':<12}{'M2':<12}{'XOR':<12}{'Số bit khác'}")
    for i, (a, b) in enumerate(zip(s1, s2)):
        name = "Khởi tạo" if i == 0 else f"Vòng {i}"
        print(f"{name:<10}{format(a,'08b'):<12}{format(b,'08b'):<12}{format(a^b,'08b'):<12}{hamming(a,b)}")
    print(f"\nBản mã M1 = {s1[-1]:#04x}, bản mã M2 = {s2[-1]:#04x}")