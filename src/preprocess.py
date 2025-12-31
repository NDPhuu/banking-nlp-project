import re
import unicodedata
import pandas as pd
import os

# ==============================================================================
# 1. TỪ ĐIỂN MỞ RỘNG (ĐÃ CẬP NHẬT THEO DATA CỦA BẠN)
# ==============================================================================
teencode_dict = {
    # --- Phủ định & Đồng ý ---
    "k": "không", "ko": "không", "kh": "không", "hk": "không", "hok": "không",
    "hông": "không", "hong": "không", "khg": "không", "kg": "không", "k0": "không", "o": "không",
    "đc": "được", "dc": "được", "dx": "được", "dcd": "được", "dk": "được",
    "uk": "ừ", "uh": "ừ", "um": "ừ", "uhm": "ừ",
    "ok": "tốt", "oke": "tốt", "okk": "tốt", "okkk": "tốt", "okok": "tốt", "oki": "tốt",
    "yes": "có", "ye": "vâng",
    "bt": "bình thường", "bth": "bình thường",

    # --- Đại từ & Đối tượng ---
    "ng": "người", "n": "người",
    "ngt": "người ta", "ngta": "người ta", "nta": "người ta", "nđgt": "người ta",
    "mn": "mọi người", "mng": "mọi người",
    "m": "mày", "t": "tao", "tui": "tôi", "mik": "mình", "mjk": "mình", "mk": "mình",
    "b": "bạn", "bn": "bạn",
    "ad": "nhân viên", "admin": "quản trị viên", "add": "quản trị viên",
    "ae": "anh em", "hs": "học sinh", "sv": "sinh viên",

    # --- Hành động & Trạng thái ---
    "lm": "làm", "lam": "làm",
    "r": "rồi", "roi": "rồi", "rui": "rồi", "rùi": "rồi",
    "h": "giờ", "hjo": "giờ",
    "bh": "bây giờ", "bjo": "bây giờ",
    "trc": "trước", "ms": "mới",
    "bit": "biết", "bik": "biết", "bít": "biết",
    "thik": "thích", "thix": "thích",
    "iu": "yêu", "yeu": "yêu",
    "fai": "phải", "phai": "phải",
    "ktra": "kiểm tra", "check": "kiểm tra",
    "tl": "trả lời", "rep": "trả lời",
    "nt": "nhắn tin", "ib": "nhắn tin",
    "goi": "gọi",
    "xai": "xài", "sài": "xài",
    "sd": "sử dụng", "sđ": "sử dụng",
    
    # --- Đăng ký / Đăng nhập / App ---
    "dky": "đăng ký", "đki": "đăng ký",
    "đnh": "đăng nhập", "dn": "đăng nhập", "log": "đăng nhập", "login": "đăng nhập", "dgnhập": "đăng nhập",
    "out": "thoát", "văng": "thoát", "dis": "thoát", "đis": "thoát", "crash": "thoát",
    "load": "tải", "loading": "tải", "xoay": "tải", "quay": "tải",
    "up": "cập nhật", "update": "cập nhật", "cap": "cập nhật",

    # --- Từ nối & Cảm thán ---
    "vs": "với", "voi": "với", "cới": "với",
    "j": "gì", "ji": "gì", "gị": "gì",
    "z": "vậy", "v": "vậy", "zậy": "vậy",
    "wa": "quá", "wá": "quá", "qa": "quá",
    "lun": "luôn", "lunk": "luôn",
    "cx": "cũng",
    "nhìu": "nhiều", "nhiu": "nhiều",
    "ak": "à", "ah": "à",
    "hen": "hẹn", "cs": "có", "kb": "kết bạn",
    "tbao": "thông báo", "info": "thông tin", "sk": "sự kiện",
    "gdich": "giao dịch", "tt": "thanh toán",
    "dt": "điện thoại", "stk": "số tài khoản",
    "acc": "tài khoản", "tkhoan": "tài khoản",

    # --- Thuật ngữ Ngân hàng / Tech ---
    "tk": "tài khoản",
    "mk": "mật khẩu", "pass": "mật khẩu", "passwword": "mật khẩu",
    "ck": "chuyển khoản", "banking": "chuyển khoản",
    "gd": "giao dịch",
    "sdt": "số điện thoại", "đt": "điện thoại",
    "nh": "ngân hàng", "bank": "ngân hàng",
    "nv": "nhân viên",
    "cskh": "chăm sóc khách hàng", "tđ": "tổng đài",
    "qc": "quảng cáo", "ads": "quảng cáo",
    "km": "khuyến mãi",

    # Mapping dây chuyền (Chain)
    "ap": "app", "aap": "app", "áp": "app", "appp": "app",
    "app": "ứng dụng",
    "wifi": "mạng", "3g": "mạng", "4g": "mạng", "5g": "mạng", "net": "mạng",
    "0tp": "otp", "otp": "mã xác thực", "opt": "mã xác thực", "otg": "mã xác thực", "ma": "mã",
    "qr": "mã qr",
    "cccd": "căn cước công dân", "cmnd": "chứng minh nhân dân",
    "vnid": "vneid", "vneld": "vneid",
    "face": "khuôn mặt", "faceid": "khuôn mặt", "sinh trắc": "sinh trắc học",
    "lang": "lag", "lag": "giật", "lác": "giật", "lagg": "giật", "đơ": "giật", "treo": "giật",

    # --- Slang / Chửi thề ---
    "dmm": "địt mẹ mày", "đmm": "địt mẹ mày", "dm": "địt mẹ", "đm": "địt mẹ",
    "vcl": "vãi lồn", "vl": "vãi lồn", "vkl": "vãi lồn", "vãi": "vãi",
    "cl": "cái lồn", "lồn": "lồn", "loz": "lồn", "l": "lồn",
    "cc": "con cặc", "cặc": "cặc", "cak": "cặc",
    "ncc": "như con cặc", "như l": "như lồn", "như c": "như cặc",
    "như hạch": "tệ", "như shit": "tệ", "như cứt": "tệ",
    "qq": "quần què",
    "oc": "óc chó",
    "cmn": "con mẹ nó",
    "éo": "đéo", "dell": "đéo", "đell": "đéo",
    "lõ": "lởm", "lỏ": "lởm",
    "ngu": "ngu", "nguu": "ngu",
    "tệ": "tệ", "tẹ": "tệ", "dở": "tệ", "chán": "tệ",
}

# ==============================================================================
# 2. TỪ ĐIỂN SỬA LỖI CHÍNH TẢ & DẤU (TYPO CORRECTION)
# (Giữ lại cái này để sửa lỗi dấu trước khi map teencode)
# ==============================================================================
typo_dict = {
    "tien": "tiền", "tiên": "tiền",
    "bi": "bị", "bịnh": "bệnh",
    "hẹn": "hẹn", "hen": "hẹn",
    "tro": "trò",
    "ngay": "ngày",
    "nua": "nữa", "nửa": "nữa",
    "roi": "rồi", "rui": "rồi",
    "xai": "xài",
    "gửi": "gửi", "gui": "gửi",
    "tai": "tải",
    "nguoiaf": "người",
    "xuất xắc": "xuất sắc",
}

# ==============================================================================
# 3. DANH SÁCH BẢO VỆ (KHÔNG TÁCH TỪ/KHÔNG XÓA)
# ==============================================================================
protected_phrases = {
    "z fold": "z_fold", "z flip": "z_flip", "gen z": "gen_z",
    "zalo pay": "zalo_pay", "zalo app": "zalo_app", "zalopay": "zalopay",
    "apple pay": "apple_pay", "samsung pay": "samsung_pay", "google pay": "google_pay",
    "smart otp": "smart_otp",
    "vietcombank": "vietcombank", "agribank": "agribank", "vietinbank": "vietinbank",
    "techcombank": "techcombank", "sacombank": "sacombank", "tpbank": "tpbank",
    "mbbank": "mbbank", "bidv": "bidv", "vpbank": "vpbank", "msb": "msb",
    "ocb": "ocb", "shb": "shb", "vib": "vib", "acb": "acb", "hdbank": "hdbank",
    "cake": "cake_bank", "timo": "timo_bank", "tnex": "tnex_bank", "momo": "momo",
    "viettel money": "viettel_money", "viettelpay": "viettelpay",
    "mobile banking": "mobile_banking", "internet banking": "internet_banking",
    "s24fe": "s24fe", "s24 fe": "s24fe",
}

# ==============================================================================
# 4. HÀM XỬ LÝ CHÍNH
# ==============================================================================

def _apply_phrase_fixes(text: str) -> str:
    """Sửa lỗi cả cụm từ trước khi tách từ"""
    replacements = [
        ("mã mã xác thực", "mã xác thực"),
        ("ứng ứng dụng", "ứng dụng"),
        ("ngân ngân hàng", "ngân hàng"),
        ("tài tài khoản", "tài khoản"),
        ("môm", "momo"), ("mơ mơ", "momo"),
        ("chai nhiem tot", "trải nghiệm tốt"),
        ("yei cau", "yêu cầu"),
        ("ngàn hang", "ngân hàng"), ("qui tin", "quy định"),
        ("ung dung", "ứng dụng"),
        ("áp sai ok", "app xài ok"),
        ("ho trò", "hỗ trợ"),
        ("con ca", "con cặc"),
    ]
    for src, dst in replacements:
        text = text.replace(src, dst)
    return text

def _map_token_chain(token: str, max_hops: int = 3) -> str:
    """Map bắc cầu: lang -> lag -> giật"""
    cur = token
    for _ in range(max_hops):
        # 1. Check Teencode
        nxt = teencode_dict.get(cur)
        # 2. Nếu không có trong teencode, check Typo (để sửa dấu)
        if not nxt:
            nxt = typo_dict.get(cur)
            
        if not nxt or nxt == cur:
            break
        cur = nxt
    return cur

def standardize_marks(text):
    """Regex sửa dấu sơ bộ theo ngữ cảnh"""
    text = re.sub(r'\bbi\b', 'bị', text)
    text = re.sub(r'\btien\b', 'tiền', text)
    text = re.sub(r'\bhen\b', 'hẹn', text)
    return text

def clean_text(text):
    if not isinstance(text, str) or not text.strip():
        return ""

    # 1. Lower + NFC
    text = text.lower()
    text = unicodedata.normalize("NFC", text)

    # 2. Sửa cụm từ lỗi (Phrase fixes)
    text = _apply_phrase_fixes(text)

    # 3. Bảo vệ cụm từ (Protected phrases)
    for original, protected in protected_phrases.items():
        if original in text:
            text = text.replace(original, protected)
            
    # 4. Sửa lỗi dấu sơ bộ (Logic cũ của tôi - Rất quan trọng)
    text = standardize_marks(text)

    # 5. Giảm ký tự lặp > 2 (lỗiiii -> lỗi)
    text = re.sub(r"([a-zđăâêôơưáàảãạằắẳẵặầấẩẫậéèẻẽẹềếểễệíìỉĩịóòỏõọồốổỗộờớởỡợúùủũụừứửữựýỳỷỹỵ])\1{2,}", r"\1", text)

    # 6. Tách từ & Map chain (Kết hợp Teencode + Typo)
    words = text.split()
    cleaned_words = []
    for word in words:
        # Tách suffix (ví dụ: "app," -> "app")
        m = re.match(r"^([\w_]+)(.*)$", word)
        if not m:
            cleaned_words.append(word)
            continue

        core_word, suffix = m.group(1), m.group(2)
        # Map bắc cầu
        core_word = _map_token_chain(core_word, max_hops=4)
        cleaned_words.append(core_word + suffix)

    text = " ".join(cleaned_words)

    # 7. Logic số + đơn vị (Regex context)
    text = re.sub(r"(\d+)\s*tr\b", r"\1 triệu", text)
    text = re.sub(r"(\d+)\s*k\b", r"\1 nghìn", text)
    text = re.sub(r"\b0\s*sao\b", "0 sao", text)
    text = re.sub(r"\b1\s*sao\b", "1 sao", text)
    text = re.sub(r'(\d+)\s+ngay', r'\1 ngày', text) # Logic cũ: 2 ngay -> 2 ngày
    text = re.sub(r'(lần|cái|đi|rồi|nữa)\s+nửa', r'\1 nữa', text) # Logic cũ: lần nửa -> lần nữa

    # 8. Xóa ký tự rác (Whitelist)
    vietnamese_chars = r"a-záàảãạăằắẳẵặâầấẩẫậéèẻẽẹêềếểễệóòỏõọôồốổỗộơờớởỡợíìỉĩịúùủũụưừứửữựýỳỷỹỵđ"
    allowed_chars = r"0-9" + vietnamese_chars + r"\s_"
    text = re.sub(rf"[^{allowed_chars}]+", " ", text)

    # 9. Khôi phục cụm bảo vệ (z_fold -> z fold) & Dọn khoảng trắng
    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text).strip()

    return text

# ==============================================================================
# 5. CHẠY THỰC THI (LOGIC FILE CHUẨN CŨ)
# ==============================================================================
def process_file(input_path='data/raw_reviews.csv', output_path='data/cleaned_reviews.csv'):
    print(f"--> Bắt đầu xử lý file: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"Lỗi: Không tìm thấy file {input_path}")
        return

    try:
        # Đọc file (utf-8)
        df = pd.read_csv(input_path, encoding='cp1258')
        print(f"Đã đọc file thành công. Số dòng: {len(df)}")
        
        if 'content' not in df.columns:
            print("Lỗi: File CSV không có cột 'content'.")
            return

        print("Đang thực hiện clean_text...")
        df['cleaned_content'] = df['content'].astype(str).apply(clean_text)
        
        # LƯU FILE VỚI UTF-8-SIG (Logic cũ để fix lỗi font Excel)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"--> Hoàn tất! Đã lưu kết quả vào: {output_path} (Format: utf-8-sig)")
        
        # Preview
        print("\n--- 5 Dòng đầu tiên (Gốc vs Clean) ---")
        pd.set_option('display.max_colwidth', 100)
        print(df[['content', 'cleaned_content']].head(5))
        
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    process_file()
