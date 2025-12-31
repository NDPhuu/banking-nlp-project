import streamlit as st
import pandas as pd
import time
from src.analyzer import BankingAnalyzer
from src.dashboard import render_dashboard

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Banking Social Listening",
    page_icon="🏦",
    layout="wide"
)

# --- CSS TÙY CHỈNH CHO ĐẸP ---
st.markdown("""
<style>
    .main-header {font-size: 30px; font-weight: bold; color: #1E88E5;}
    .metric-card {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #1E88E5;}
</style>
""", unsafe_allow_html=True)

# --- LOAD MODEL (CACHE ĐỂ KHÔNG LOAD LẠI) ---
@st.cache_resource
def load_engine():
    # Hiển thị spinner xoay xoay lúc đang load
    with st.spinner("⏳ Đang khởi động (Load PhoBERT)... Vui lòng chờ khoảng 30s..."):
        try:
            analyzer = BankingAnalyzer()
            return analyzer
        except Exception as e:
            st.error(f"❌ Lỗi load model: {e}")
            return None

# --- LOAD DỮ LIỆU CSV (CACHE) ---
@st.cache_data
def load_data():
    try:
        # Đọc file CSV (Giả sử file này đã được gán nhãn xong xuôi để vẽ chart)
        # Nếu chưa có file labeled, bạn có thể dùng tạm file raw để test UI
        df = pd.read_csv("data/raw_reviews.csv",encoding="utf-8-sig") 
        return df
    except FileNotFoundError:
        return None

# --- KHỞI TẠO ---
analyzer = load_engine()
df = load_data()

# --- GIAO DIỆN CHÍNH ---
st.markdown('<p class="main-header">🏦 HỆ THỐNG LẮNG NGHE & PHÂN TÍCH APP NGÂN HÀNG</p>', unsafe_allow_html=True)
st.markdown("---")

# TẠO TAB
tab1, tab2, tab3 = st.tabs(["📊 Báo cáo Tổng quan", "🤖 Demo (Real-time)", "🕷️ Dữ liệu thô"])

# === TAB 1: DASHBOARD ===
with tab1:
    if df is not None:
        render_dashboard(df)
    else:
        st.warning("⚠️ Chưa tìm thấy file dữ liệu 'data/raw_reviews.csv'. Hãy chạy scraper.py trước!")

# === TAB 2: DEMO ===
with tab2:
    st.header("Kiểm thử Mô hình")
    st.write("Nhập một câu đánh giá bất kỳ để xem mô hình phân tích Chủ đề và Cảm xúc.")

    col_input, col_btn = st.columns([4, 1])
    with col_input:
        user_text = st.text_area("Nhập nội dung review:", height=100, placeholder="Ví dụ: App chuyển tiền nhanh nhưng giao diện hơi rối...")
    with col_btn:
        st.write("") # Spacer
        st.write("")
        analyze_btn = st.button("🔍 Phân tích ngay", type="primary", use_container_width=True)

    if analyze_btn and user_text:
        if analyzer:
            start_time = time.time()
            result = analyzer.predict(user_text)
            end_time = time.time()

            # Hiển thị kết quả
            st.success(f"✅ Phân tích xong trong {end_time - start_time:.2f} giây!")
            
            st.caption(f"Text sau khi làm sạch: {result['text_clean']}")

            # Hiển thị 2 cột kết quả
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.subheader("🎭 Cảm xúc")
                st.markdown(f"**{result['sentiment_label']}**")
                st.progress(result['sentiment_score'])
                st.caption(f"Độ tin cậy: {result['sentiment_score']:.2%}")
                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.subheader("🏷️ Chủ đề")
                st.markdown(f"**{result['topic_label']}**")
                st.progress(result['topic_score'])
                st.caption(f"Độ tin cậy: {result['topic_score']:.2%}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Model chưa được load thành công. Kiểm tra lại thư mục models/")

# === TAB 3: DỮ LIỆU ===
with tab3:
    st.subheader("Dữ liệu đánh giá thô")
    if df is not None:
        st.dataframe(df)
    else:
        st.info("Chưa có dữ liệu.")