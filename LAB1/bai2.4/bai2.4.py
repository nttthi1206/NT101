"""
Playfair Cipher - Ma hoa / Giai ma
Cho phep nhap khoa va van ban de ma hoa hoac giai ma.
Hien thi ma tran Playfair 5x5 tuong ung voi khoa da nhap.
"""

def build_matrix(key):
    key = key.upper().replace("J", "I")
    key = "".join(ch for ch in key if ch.isalpha())

    seen = set()
    matrix_letters = []
    for ch in key:
        if ch not in seen:
            seen.add(ch)
            matrix_letters.append(ch)

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # no J, merged with I
        if ch not in seen:
            seen.add(ch)
            matrix_letters.append(ch)

    matrix = [matrix_letters[i*5:(i+1)*5] for i in range(5)]
    return matrix


def print_matrix(matrix):
    print("\nMa tran Playfair 5x5:")
    print("+----" * 5 + "+")
    for row in matrix:
        print("| " + " | ".join(row) + " |")
        print("+----" * 5 + "+")
    print()


def find_position(matrix, ch):
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == ch:
                return r, c
    return None


def prepare_text(text, mode="encrypt"):
    text = text.upper().replace("J", "I")
    text = "".join(ch for ch in text if ch.isalpha())

    if mode == "decrypt":
        # ciphertext always comes in clean digraphs already
        return text

    # encrypt: build digraphs, insert filler between duplicate letters,
    # and pad with filler if length is odd
    result = []
    i = 0
    n = len(text)
    while i < n:
        a = text[i]
        if i + 1 < n:
            b = text[i+1]
            if a == b:
                result.append(a + "X")
                i += 1
            else:
                result.append(a + b)
                i += 2
        else:
            result.append(a + "X")
            i += 1
    return "".join(result)


def playfair_encrypt(matrix, plaintext):
    prepared = prepare_text(plaintext, "encrypt")
    ciphertext = []
    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i+1]
        ra, ca = find_position(matrix, a)
        rb, cb = find_position(matrix, b)

        if ra == rb:  # same row -> shift right
            ciphertext.append(matrix[ra][(ca+1) % 5])
            ciphertext.append(matrix[rb][(cb+1) % 5])
        elif ca == cb:  # same column -> shift down
            ciphertext.append(matrix[(ra+1) % 5][ca])
            ciphertext.append(matrix[(rb+1) % 5][cb])
        else:  # rectangle -> swap columns
            ciphertext.append(matrix[ra][cb])
            ciphertext.append(matrix[rb][ca])

    return "".join(ciphertext)


def playfair_decrypt(matrix, ciphertext):
    prepared = prepare_text(ciphertext, "decrypt")
    if len(prepared) % 2 != 0:
        prepared = prepared[:-1]  # bo ky tu le cuoi neu co

    plaintext = []
    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i+1]
        ra, ca = find_position(matrix, a)
        rb, cb = find_position(matrix, b)

        if ra == rb:  # same row -> shift left
            plaintext.append(matrix[ra][(ca-1) % 5])
            plaintext.append(matrix[rb][(cb-1) % 5])
        elif ca == cb:  # same column -> shift up
            plaintext.append(matrix[(ra-1) % 5][ca])
            plaintext.append(matrix[(rb-1) % 5][cb])
        else:  # rectangle -> swap columns
            plaintext.append(matrix[ra][cb])
            plaintext.append(matrix[rb][ca])

    return "".join(plaintext)


def read_multiline(prompt):
    """
    Cho phep nhap/dan van ban tren nhieu dong (vi du copy-paste ban ma
    dai duoc chia thanh nhieu dong). Nhan Enter tren mot dong trong
    (khong go gi ca) de ket thuc nhap.
    """
    print(prompt + ":")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            if lines:  # da co du lieu -> ket thuc
                break
            else:      # dong trong dau tien -> bo qua, tiep tuc doi nhap
                continue
        lines.append(line)
    return "".join(lines)


def main():
    print("=== PLAYFAIR CIPHER ===")
    key = input("Nhap khoa (key): ").strip()
    matrix = build_matrix(key)
    print_matrix(matrix)

    mode = input("Chon che do (E = ma hoa / D = giai ma): ").strip().upper()

    if mode == "E":
        plaintext = read_multiline("Nhap ban ro (plaintext)")
        cipher = playfair_encrypt(matrix, plaintext)
        print(f"\nBan ro da chuan hoa: {prepare_text(plaintext, 'encrypt')}")
        print(f"Ban ma (ciphertext): {cipher}")
    elif mode == "D":
        ciphertext = read_multiline("Nhap ban ma (ciphertext)")
        plain = playfair_decrypt(matrix, ciphertext)
        print(f"\nBan ma: {ciphertext.upper()}")
        print(f"\nBan ro (plaintext) sau khi giai ma: {plain}")
    else:
        print("Che do khong hop le. Vui long chon E hoac D.")


if __name__ == "__main__":
    main()