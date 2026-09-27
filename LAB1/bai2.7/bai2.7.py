"""
Rail Fence Cipher - Ma hoa va giai ma
======================================
Thuat toan ma hoa hoan vi (transposition cipher) co dien.
Nguyen ly: ban ro duoc viet theo duong zigzag tren so luong "rail"
(duong ray) cho truoc, sau do doc lai lan luot tung rail tu tren
xuong duoi de tao thanh ban ma. Giai ma thuc hien nguoc lai: xac
dinh vi tri zigzag cua tung ky tu ban ma va sap xep lai theo dung
thu tu ban dau.

Chay chuong trinh: python3 rail_fence_cipher.py
Chuong trinh se hien menu de nguoi dung nhap ban ro/ban ma va
so rail truc tiep tu ban phim.
"""

from collections import Counter


def _zigzag_pattern(length: int, rails: int):
    """Sinh chuoi chi so rail (0..rails-1) theo duong zigzag cho
    'length' vi tri lien tiep. Day chinh la 'so do duong ray' dung
    chung cho ca ma hoa va giai ma."""
    pattern = []
    rail, direction = 0, 1
    for _ in range(length):
        pattern.append(rail)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction
    return pattern


def encrypt(plaintext: str, rails: int) -> str:
    """Ma hoa plaintext bang Rail Fence Cipher voi so rail cho truoc."""
    if rails < 2:
        raise ValueError("So rail phai >= 2")

    fence = [[] for _ in range(rails)]
    pattern = _zigzag_pattern(len(plaintext), rails)

    for ch, r in zip(plaintext, pattern):
        fence[r].append(ch)

    return "".join("".join(row) for row in fence)


def decrypt(ciphertext: str, rails: int) -> str:
    """Giai ma ciphertext da duoc ma hoa bang Rail Fence Cipher."""
    if rails < 2:
        raise ValueError("So rail phai >= 2")

    n = len(ciphertext)
    pattern = _zigzag_pattern(n, rails)
    counts = Counter(pattern)

    # Cat ciphertext thanh cac doan tuong ung voi tung rail
    rows, idx = [], 0
    for r in range(rails):
        rows.append(list(ciphertext[idx: idx + counts[r]]))
        idx += counts[r]

    # Duyet lai theo dung thu tu zigzag, lay tung ky tu tu rail tuong ung
    pointers = [0] * rails
    plaintext = []
    for r in pattern:
        plaintext.append(rows[r][pointers[r]])
        pointers[r] += 1

    return "".join(plaintext)


def visualize(text: str, rails: int) -> str:
    """Tra ve chuoi hien thi truc quan duong zigzag (de minh hoa/bao cao)."""
    grid = [[" " for _ in range(len(text))] for _ in range(rails)]
    pattern = _zigzag_pattern(len(text), rails)
    for i, (ch, r) in enumerate(zip(text, pattern)):
        grid[r][i] = ch
    return "\n".join("".join(row) for row in grid)


def _read_rails() -> int:
    while True:
        raw = input("Nhap so rail (>=2): ").strip()
        try:
            rails = int(raw)
            if rails >= 2:
                return rails
            print("So rail phai >= 2, thu lai.")
        except ValueError:
            print("Vui long nhap mot so nguyen, thu lai.")


def _run_encrypt():
    text = input("Nhap ban ro can ma hoa: ")
    rails = _read_rails()
    print("\nSo do zigzag:")
    print(visualize(text, rails))
    print(f"\nBan ma: {encrypt(text, rails)}\n")


def _run_decrypt():
    text = input("Nhap ban ma can giai ma: ")
    rails = _read_rails()
    result = decrypt(text, rails)
    print(f"\nSo do zigzag:")
    print(visualize(result, rails))
    print(f"\nBan ro sau khi giai ma: {result}\n")


def _demo():
    plaintext = "HELLO RAIL FENCE CIPHER"
    rails = 4

    print("\n=== VI DU MINH HOA RAIL FENCE CIPHER ===\n")
    print(f"Ban ro (plaintext): {plaintext!r}")
    print(f"So rail: {rails}\n")

    print("So do zigzag:")
    print(visualize(plaintext, rails))
    print()

    ciphertext = encrypt(plaintext, rails)
    print(f"Ban ma (ciphertext): {ciphertext!r}\n")

    recovered = decrypt(ciphertext, rails)
    print(f"Ban ro giai ma duoc: {recovered!r}")

    print("\nKiem tra:", "DUNG" if recovered == plaintext else "SAI", "\n")


def main():
    while True:
        print("===== RAIL FENCE CIPHER =====")
        print("1. Ma hoa")
        print("2. Giai ma")
        print("3. Chay vi du minh hoa co san")
        print("4. Thoat")
        choice = input("Chon (1-4): ").strip()

        if choice == "1":
            _run_encrypt()
        elif choice == "2":
            _run_decrypt()
        elif choice == "3":
            _demo()
        elif choice == "4":
            print("Ket thuc chuong trinh.")
            break
        else:
            print("Lua chon khong hop le, vui long thu lai.\n")


if __name__ == "__main__":
    main()