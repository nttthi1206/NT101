import collections

def get_multiline_input():
    print("Nhập ciphertext (Nhập một dòng chỉ chứa chữ 'DONE' để kết thúc quá trình nhập):")
    lines = []
    while True:
        line = input()
        if line.strip() == 'DONE':
            break
        lines.append(line)
    return "\n".join(lines)

def print_frequency_analysis(text):
    # Lọc chỉ lấy chữ cái và chuyển thành chữ thường để đếm
    letters = [c.lower() for c in text if c.isalpha()]
    total = len(letters)
    
    if total == 0:
        print("Không tìm thấy chữ cái nào để thống kê.")
        return
    
    counter = collections.Counter(letters)
    
    print("\n" + "-"*45)
    print(f"{'THỐNG KÊ TẦN SUẤT CHỮ CÁI':^45}")
    print("-"*45)
    print(f"{'Chữ cái':<10} | {'Số lần xuất hiện':<20} | {'Tỷ lệ %':<10}")
    print("-"*45)
    
    for char, count in counter.most_common():
        percent = (count / total) * 100
        print(f"   {char.upper():<7} | {count:<20} | {percent:.2f}%")
    print("-"*45)
    print("Mẹo: Trong tiếng Anh, các chữ cái phổ biến nhất là E, T, A, O, I, N, S, H, R.")

def apply_mapping(text, mapping):
    result = []
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            c_lower = char.lower()
            
            # Nếu ký tự đã được giả thuyết, tiến hành thay thế
            if c_lower in mapping:
                mapped_char = mapping[c_lower]
                result.append(mapped_char.upper() if is_upper else mapped_char.lower())
            else:
                # Nếu chưa có trong bảng ánh xạ, giữ nguyên ký tự gốc
                result.append(char)
        else:
            result.append(char)
    return "".join(result)

def main():
    text = get_multiline_input()
    if not text.strip():
        print("Không có dữ liệu đầu vào.")
        return

    print_frequency_analysis(text)
    
    mapping = {}
    print("\n--- BẮT ĐẦU GIẢI MÃ ---")
    print("- Cú pháp thêm/đổi: c=p (Ví dụ: g=t nghĩa là thay 'g' trong mật mã thành 't' trong bản rõ)")
    print("- Cú pháp xóa: del c (Ví dụ: del g để xóa ánh xạ của 'g')")
    print("- Gõ 'exit' để kết thúc.")

    while True:
        print("\n" + "="*80)
        print("BẢN RÕ TẠM THỜI (Các chữ đã giải mã sẽ hòa vào ngữ cảnh):")
        print("="*80)
        print(apply_mapping(text, mapping))
        print("="*80)
        print(f"Bảng ánh xạ hiện tại: {mapping}")
        
        cmd = input("\nNhập lệnh (vd: g=t, del g, exit): ").strip().lower()
        
        if cmd == 'exit':
            print("Đã thoát công cụ giải mã.")
            break
        elif cmd.startswith("del "):
            parts = cmd.split(" ")
            if len(parts) == 2:
                c = parts[1].strip()
                if c in mapping:
                    del mapping[c]
                    print(f"[+] Đã xóa ánh xạ cho chữ '{c}'.")
                else:
                    print(f"[-] Chữ '{c}' chưa được ánh xạ.")
        elif "=" in cmd:
            parts = cmd.split("=")
            if len(parts) == 2 and len(parts[0].strip()) == 1 and len(parts[1].strip()) == 1:
                c = parts[0].strip()
                p = parts[1].strip()
                mapping[c] = p
                print(f"[+] Đã cập nhật ánh xạ: '{c}' -> '{p}'.")
            else:
                print("[-] Sai cú pháp! Hãy nhập đúng 1 ký tự, ví dụ: g=t")
        else:
            print("[-] Lệnh không hợp lệ.")

if __name__ == "__main__":
    main()