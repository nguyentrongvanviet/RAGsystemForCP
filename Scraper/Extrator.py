import fitz  # PyMuPDF
import re
import sys
import os 
def extract_and_clean_pdf(pdf_path):
    print(f"Đang phân tích layout và trích xuất: {pdf_path}...")

    try:
        # Mở file bằng engine C++ của MuPDF
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise RuntimeError(f"Không thể mở file PDF. Lỗi: {e}")

    full_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Lấy text theo từng block (giúp giữ cấu trúc đoạn văn tốt hơn lấy text thô)
        blocks = page.get_text("blocks")

        for block in blocks:
            text = block[4].strip() # Text nằm ở index 4 của block metadata

            # 1. BỘ LỌC RÁC (Heuristics)
            # Bỏ qua các block quá ngắn (thường là số trang)
            if len(text) < 10:
                continue

            # 2. CHUẨN HÓA TEXT
            # Xóa các khoảng trắng thừa, nối các dòng bị ngắt ngoặc (hyphenation)
            # text = text.replace('\n', ' ')
            text = re.sub(r'\s+', ' ', text)

            full_text.append(text)

    # Nối toàn bộ tài liệu
    document_string = " ".join(full_text)

    print(f"✅ Đã trích xuất thành công {len(full_text)} khối văn bản.")
    return document_string

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python [Extrator.py](http://_vscodecontentref_/0) <path_to_pdf>")
        sys.exit(1)

    pdf_file = sys.argv[1]

    if not os.path.isfile(pdf_file):
        print(f"File không tồn tại: {pdf_file}")
        sys.exit(1)

    raw_text = extract_and_clean_pdf(pdf_file)
    print("\n--- TRÍCH XUẤT MẪU ---")
    print(raw_text)