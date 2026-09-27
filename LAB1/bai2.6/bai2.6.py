#!/usr/bin/env python3
"""
================================================================================
 Nhóm 5 - Nhiệm vụ 2.6
================================================================================
THUẬT TOÁN TỔNG QUAN
--------------------
  Bước 1  Chuẩn hóa ciphertext (chỉ giữ chữ cái, viết hoa) để phân tích thống kê.
  Bước 2  Ước lượng độ dài khóa bằng 2 phương pháp độc lập:
            (a) Kasiski Examination — tìm n-gram lặp lại, lấy ước số của
                khoảng cách giữa các lần lặp làm "phiếu bầu" cho độ dài khóa.
            (b) Index of Coincidence trung bình từng cột — độ dài khóa đúng
                cho IC gần với IC tiếng Anh (~0.0655) nhất.
          Kết hợp phiếu Kasiski + độ khớp IC để chọn ra một tập ứng viên.
  Bước 3  Với MỖI ứng viên: suy từng ký tự khóa bằng phân tích tần suất
          (thử 26 shift Caesar mỗi cột, chọn shift khớp tần suất tiếng Anh
          nhất theo Chi-squared), rồi giải mã thử toàn bộ văn bản.
  Bước 4  Kiểm chứng chéo: so Chi-squared của các bản rõ ứng viên, rút gọn
          khóa về chu kỳ nhỏ nhất, loại trùng lặp, chọn kết quả tốt nhất.
  Bước 5  Hiển thị: bảng IC/Kasiski, khóa từng ứng viên, bản rõ tốt nhất
          (giữ nguyên định dạng gốc), và breakdown từng ký tự khóa.
"""

import os
import sys
import re
import math
from collections import Counter
from itertools import combinations

# ---------------------------------------------------------------------------
# 1. HẰNG SỐ THAM CHIẾU
# ---------------------------------------------------------------------------
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Tần suất chữ cái tiếng Anh (%) - dùng cho Chi-squared
ENGLISH_FREQ_PCT = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 'F': 2.228,
    'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025,
    'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929, 'Q': 0.095, 'R': 5.987,
    'S': 6.327, 'T': 9.056, 'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150,
    'Y': 1.974, 'Z': 0.074,
}
# Tần suất dạng tỉ lệ (0..1), cùng thứ tự A..Z - dùng để đo IC-target
EN_FREQ_RATIO = [ENGLISH_FREQ_PCT[c] / 100 for c in ALPHA]

IC_ENGLISH = 0.0655   # Index of Coincidence trung bình của tiếng Anh
IC_RANDOM = 0.0385    # Index of Coincidence của chuỗi ngẫu nhiên (tham chiếu)
MAX_KEY_LEN = 20       # giới hạn trên khi dò độ dài khóa
DEFAULT_TOP_N = 6      # số ứng viên độ dài khóa mặc định sẽ thử giải mã


# ---------------------------------------------------------------------------
# 2. CHUẨN HÓA & NHẬP DỮ LIỆU (nhập tay hoặc đọc từ file)
# ---------------------------------------------------------------------------
def normalize(text: str) -> str:
    """Chỉ giữ ký tự chữ cái A-Z, chuyển hết về chữ hoa. Dùng cho phân tích
    thống kê (Kasiski, IC, Chi-squared)"""
    return re.sub(r'[^A-Za-z]', '', text).upper()


def get_ciphertext() -> str:
    """
      - Chọn 1: dán ciphertext trực tiếp vào terminal
      - Chọn 2: nhập đường dẫn file để chương trình tự đọc
    """
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if not os.path.isfile(path):
            print(f"[!] Không tìm thấy file: {path}")
            sys.exit(1)
        with open(path, 'r', encoding='utf-8') as f:
            print(f"[+] Đã đọc ciphertext từ file: {path}")
            return f.read()

    print("=" * 60)
    print("  VIGENÈRE CIPHER - AUTOMATIC KEY BREAKER")
    print("=" * 60)
    print("  1. Nhập/dán ciphertext trực tiếp")
    print("  2. Đọc ciphertext từ file")
    choice = input("\nLựa chọn (1/2): ").strip()

    if choice == '2':
        path = input("Nhập đường dẫn file: ").strip()
        if not os.path.isfile(path):
            print(f"[!] Không tìm thấy file: {path}")
            sys.exit(1)
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    print("Dán ciphertext vào")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 3. KASISKI EXAMINATION
# ---------------------------------------------------------------------------
def kasiski_distance_votes(letters: str, ngram_lens=(3, 4, 5)) -> Counter:
    """
    Tìm mọi n-gram (độ dài 3-5) lặp lại trong bản mã, ghi nhận khoảng cách
    giữa các lần xuất hiện. Mỗi ước số (2..MAX_KEY_LEN) của khoảng cách đó
    được xem là một "phiếu bầu" cho độ dài khóa tương ứng.
    """
    votes = Counter()
    for n in ngram_lens:
        positions = {}
        for i in range(len(letters) - n + 1):
            gram = letters[i:i + n]
            positions.setdefault(gram, []).append(i)

        for gram, idxs in positions.items():
            if len(idxs) < 2:
                continue
            for a, b in combinations(idxs, 2):
                distance = b - a
                for factor in range(2, MAX_KEY_LEN + 1):
                    if distance % factor == 0:
                        votes[factor] += 1
    return votes


# ---------------------------------------------------------------------------
# 4. INDEX OF COINCIDENCE
# ---------------------------------------------------------------------------
def index_of_coincidence(s: str) -> float:
    n = len(s)
    if n < 2:
        return 0.0
    counts = Counter(s)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator


def average_ic_for_keylen(letters: str, key_len: int) -> float:
    """IC trung bình của các cột con khi tách bản mã theo độ dài khóa key_len."""
    ics = []
    for i in range(key_len):
        column = letters[i::key_len]
        if len(column) >= 2:
            ics.append(index_of_coincidence(column))
    return sum(ics) / len(ics) if ics else 0.0


# ---------------------------------------------------------------------------
# 5. KẾT HỢP KASISKI + IC -> DANH SÁCH ỨNG VIÊN ĐỘ DÀI KHÓA
# ---------------------------------------------------------------------------
def rank_key_length_candidates(letters: str, top_n: int = DEFAULT_TOP_N):
    """
    Trả về:
      - report: danh sách (key_len, avg_ic, delta_ic, kasiski_votes) cho
                mọi độ dài 1..MAX_KEY_LEN, để hiển thị bảng đầy đủ.
      - candidates: danh sách top_n độ dài khóa đáng thử nhất, SẮP THEO
                ĐỘ LỆCH IC NHỎ NHẤT trước (đây là điểm sửa lỗi so với bản
                xếp theo IC cao nhất), có cộng điểm thưởng nếu được Kasiski
                bỏ phiếu nhiều.
    """
    kasiski_votes = kasiski_distance_votes(letters)
    max_vote = max(kasiski_votes.values()) if kasiski_votes else 1

    report = []
    for k in range(1, MAX_KEY_LEN + 1):
        avg_ic = average_ic_for_keylen(letters, k)
        delta = abs(avg_ic - IC_ENGLISH)
        votes = kasiski_votes.get(k, 0)
        report.append((k, avg_ic, delta, votes))

    # điểm tổng hợp: độ khớp IC (0..1, càng cao càng tốt) + thưởng theo
    # tỉ lệ phiếu Kasiski (chuẩn hóa theo phiếu cao nhất)
    scored = []
    for k, avg_ic, delta, votes in report:
        if k == 1:
            continue  # độ dài 1 (Caesar thường) 
        ic_closeness = max(0.0, 1 - delta / IC_ENGLISH)
        vote_bonus = votes / max_vote if max_vote else 0
        score = 0.7 * ic_closeness + 0.3 * vote_bonus
        scored.append((k, score))

    scored.sort(key=lambda x: -x[1])
    candidates = [k for k, _ in scored[:top_n]]
    return report, candidates, kasiski_votes


# ---------------------------------------------------------------------------
# 6. PHÂN TÍCH TẦN SUẤT TỪNG CỘT -> SUY TỪNG KÝ TỰ CỦA KHÓA
# ---------------------------------------------------------------------------
def chi_squared_score(observed_counts: Counter, n: int) -> float:
    """Chi-squared giữa phân bố quan sát (observed_counts, tổng = n) và
    phân bố chuẩn tiếng Anh."""
    chi2 = 0.0
    for letter, expected_pct in ENGLISH_FREQ_PCT.items():
        expected = expected_pct / 100 * n
        observed = observed_counts.get(letter, 0)
        if expected > 0:
            chi2 += (observed - expected) ** 2 / expected
    return chi2


def best_shift_for_column(column: str):
    """Thử 26 phép dịch Caesar cho một cột, trả về (shift tốt nhất, chi2)."""
    n = len(column)
    if n == 0:
        return 0, float('inf')
    best_shift, best_chi2 = 0, float('inf')
    for shift in range(26):
        counts = Counter()
        for ch in column:
            p = (ord(ch) - ord('A') - shift) % 26
            counts[chr(p + ord('A'))] += 1
        chi2 = chi_squared_score(counts, n)
        if chi2 < best_chi2:
            best_chi2, best_shift = chi2, shift
    return best_shift, best_chi2


def recover_key(letters: str, key_len: int):
    """Suy khóa độ dài key_len bằng phân tích tần suất Chi-squared từng cột."""
    key_chars = []
    column_details = []
    for i in range(key_len):
        column = letters[i::key_len]
        shift, chi2 = best_shift_for_column(column)
        key_chars.append(chr(shift + ord('A')))
        column_details.append((i, shift, chi2))
    return ''.join(key_chars), column_details


# ---------------------------------------------------------------------------
# 7. GIẢI MÃ VIGENÈRE - GIỮ NGUYÊN ĐỊNH DẠNG GỐC (hoa/thường, dấu câu...)
# ---------------------------------------------------------------------------
def vigenere_decrypt_preserve_format(ciphertext: str, key: str) -> str:
    """Giải mã trên văn bản GỐC (chưa chuẩn hóa): ký tự không phải chữ cái
    được giữ nguyên vị trí và không làm lệch chỉ số khóa; hoa/thường của
    ciphertext được giữ lại ở bản rõ."""
    result = []
    key = key.upper()
    key_index = 0
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            result.append(chr((ord(ch.upper()) - ord('A') - shift) % 26 + base))
            key_index += 1
        else:
            result.append(ch)
    return ''.join(result)

# 8. RÚT GỌN KHÓA VỀ CHU KỲ LẶP NHỎ NHẤT (khắc phục lỗi chọn bội số)

def minimal_period(key: str) -> str:
    """
    Nếu khóa là một chuỗi lặp lại (vd "HCMUITHCMUIT" lặp từ "HCMUIT"),
    trả về đơn vị lặp nhỏ nhất. Nếu không lặp, trả về chính khóa đó.
    """
    n = len(key)
    for period in range(1, n + 1):
        if n % period != 0:
            continue
        unit = key[:period]
        if unit * (n // period) == key:
            return unit
    return key

# ---------------------------------------------------------------------------
# 9. CHI-SQUARED CỦA TOÀN BỘ BẢN RÕ (dùng để KIỂM CHỨNG CHÉO giữa các ứng viên)
# ---------------------------------------------------------------------------
def full_text_chi_squared(letters_only_plaintext: str) -> float:
    n = len(letters_only_plaintext)
    if n == 0:
        return float('inf')
    counts = Counter(letters_only_plaintext)
    return chi_squared_score(counts, n)


# ---------------------------------------------------------------------------
# 10. CHƯƠNG TRÌNH CHÍNH
# ---------------------------------------------------------------------------
def main():
    raw_text = get_ciphertext()
    letters = normalize(raw_text)

    if len(letters) < 20:
        print("[!] Ciphertext quá ngắn để phân tích thống kê đáng tin cậy "
              "(cần tối thiểu ~20 ký tự chữ cái).")
        return

    top_n_input = input(
        f"\nSố ứng viên độ dài khóa muốn thử? [mặc định={DEFAULT_TOP_N}]: "
    ).strip()
    top_n = int(top_n_input) if top_n_input.isdigit() and int(top_n_input) > 0 else DEFAULT_TOP_N

    # ---- BƯỚC 1 ----
    print("\nBƯỚC 1: CHUẨN HÓA CIPHERTEXT")
    print(f"Số ký tự chữ cái sau khi chuẩn hóa: {len(letters)}")
    print(f"IC toàn bộ ciphertext: {index_of_coincidence(letters):.4f}  "
          f"(tiếng Anh ≈ {IC_ENGLISH:.4f}, ngẫu nhiên ≈ {IC_RANDOM:.4f})")

    # ---- BƯỚC 2 ----
    print("\nBƯỚC 2: ƯỚC LƯỢNG ĐỘ DÀI KHÓA (Kasiski + Index of Coincidence)")
    report, candidates, kasiski_votes = rank_key_length_candidates(letters, top_n)

    print(f"{'Do dai khoa':>12} | {'IC trung binh':>14} | {'Lech IC':>10} | {'Phieu Kasiski':>14}")
    for k, avg_ic, delta, votes in report:
        marker = "  <-- ung vien" if k in candidates else ""
        print(f"{k:>12} | {avg_ic:>14.4f} | {delta:>10.4f} | {votes:>14}{marker}")

    print(f"\n[+] Danh sách ứng viên sẽ thử (sắp theo độ khớp IC + phiếu Kasiski): {candidates}")
    print("    (Lưu ý: các độ dài là bội số của độ dài khóa thật, vd 6→12→18,\n"
          "     thường đều lọt vào danh sách vì cũng cho IC tốt; bước 3-4 dưới\n"
          "     đây sẽ rút gọn và chọn ra khóa ngắn nhất, đúng bản chất nhất.)")

    # ---- BƯỚC 3 + 4: thử từng ứng viên, kiểm chứng chéo bằng Chi-squared ----
 
    print("\nBƯỚC 3: PHÂN TÍCH TẦN SUẤT & KIỂM CHỨNG CHÉO TỪNG ")

    results = []  # (chi2_fulltext, key_len, key_raw, key_minimal, plaintext)
    for key_len in candidates:
        key_raw, _ = recover_key(letters, key_len)
        plaintext = vigenere_decrypt_preserve_format(raw_text, key_raw)
        plain_letters = normalize(plaintext)
        chi2 = full_text_chi_squared(plain_letters)
        key_minimal = minimal_period(key_raw)
        results.append((chi2, key_len, key_raw, key_minimal, plaintext))

    results.sort(key=lambda x: x[0])

    print(f"{'Do dai':>7} | {'Khoa suy ra':>16} | {'Khoa rut gon':>14} | {'Chi-squared ban ro':>20}")
    for chi2, key_len, key_raw, key_minimal, _ in results:
        print(f"{key_len:>7} | {key_raw:>16} | {key_minimal:>14} | {chi2:>20.2f}")

    # loại trùng lặp: nhiều độ dài khác nhau có thể quy về cùng 1 khóa rút gọn
    seen_minimal = set()
    deduped = []
    for row in results:
        _, _, _, key_minimal, _ = row
        if key_minimal not in seen_minimal:
            seen_minimal.add(key_minimal)
            deduped.append(row)

    best_chi2, best_len_raw, best_key_raw, best_key, best_plain = deduped[0]

    # ---- BƯỚC 5: hiển thị breakdown khóa cuối cùng ----
    print("\nBƯỚC 4: BREAKDOWN KÝ TỰ KHÓA CUỐI CÙNG")
    final_key_len = len(best_key)
    _, column_details = recover_key(letters, final_key_len)
    print(f"Khóa được chọn (đã rút gọn về chu kỳ nhỏ nhất): \"{best_key}\" "
          f"(độ dài {final_key_len})")
    print(f"\n{'Cot':>5} | {'Ky tu khoa':>10} | {'Shift':>6} | {'Chi-squared cot':>16}")
    for i, shift, chi2 in column_details:
        print(f"{i:>5} | {chr(shift + ord('A')):>10} | {shift:>6} | {chi2:>16.2f}")

    # ---- BƯỚC 6: kết quả cuối cùng ----
    print("\nBƯỚC 5: BẢN RÕ (giữ nguyên định dạng gốc:")
    print(best_plain)

    print("=" * 72)
    print(f"TÓM TẮT:")
    print(f"  - Độ dài khóa thật (đã rút gọn) : {final_key_len}")
    print(f"  - Khóa                          : \"{best_key}\"")
    print(f"  - Chi-squared bản rõ            : {best_chi2:.2f}  "
          f"(càng nhỏ càng giống tiếng Anh chuẩn)")
    print(f"  - IC bản rõ                     : "
          f"{index_of_coincidence(normalize(best_plain)):.4f}  "
          f"(tiếng Anh ≈ {IC_ENGLISH:.4f})")
    print("=" * 72)


if __name__ == "__main__":
    main()