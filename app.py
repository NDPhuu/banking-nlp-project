import time
import pandas as pd
import streamlit as st

from src.dashboard import render_dashboard
from src.analyzer import BankingAnalyzer

st.set_page_config(page_title="Banking NLP Dashboard", layout="wide")

# =========================
# THEME / CSS
# =========================
st.markdown(
    """
    <style>
    /* ====== App background: dark glow gradient ====== */
    .stApp {
        background:
            radial-gradient(900px 520px at 18% 24%, rgba(168, 85, 247, 0.22), transparent 60%),
            radial-gradient(900px 520px at 75% 35%, rgba(34, 197, 94, 0.18), transparent 62%),
            radial-gradient(1100px 720px at 55% 82%, rgba(59, 130, 246, 0.22), transparent 62%),
            linear-gradient(180deg, #05060a 0%, #070914 55%, #05060a 100%);
        color: #E5E7EB;
    }

    /* font hệ thống */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text",
                     "Segoe UI", Roboto, Helvetica, Arial;
        color: #E5E7EB;
    }

    /* ====== Title ====== */
    h1 { letter-spacing: -0.6px; font-weight: 850; margin-bottom: 0.2rem; color: #F9FAFB; }
    .subtitle { color: rgba(229,231,235,0.72); margin-top: -6px; }

    /* ====== Tabs ====== */
    button[role="tab"] {
        font-weight: 750 !important;
        padding: 10px 16px !important;
        color: rgba(229,231,235,0.70) !important;
        border-radius: 12px !important;
    }
    button[role="tab"][aria-selected="true"] {
        color: #F9FAFB !important;
        border: 1px solid rgba(239, 68, 68, 0.55) !important;
        background: rgba(239, 68, 68, 0.12) !important;
    }

    /* ====== Buttons ====== */
    .stButton > button {
        border-radius: 14px !important;
        padding: 12px 16px !important;
        font-weight: 800 !important;
        border: 1px solid rgba(239, 68, 68, 0.45) !important;
        background: rgba(0,0,0,0.20) !important;
        color: #F9FAFB !important;
    }
    .stButton > button:hover {
        border-color: rgba(239, 68, 68, 0.85) !important;
        background: rgba(239, 68, 68, 0.12) !important;
    }

    /* ====== Inputs ====== */
    textarea {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.16) !important;
        background: rgba(3, 6, 18, 0.55) !important;
        color: #F9FAFB !important;
    }
    textarea::placeholder { color: rgba(249,250,251,0.55) !important; }

    /* label text */
    label, .stTextArea label, .stTextInput label {
        color: rgba(229,231,235,0.85) !important;
        font-weight: 650 !important;
    }

    /* ====== Cards ====== */
    .soft-card {
        background: rgba(3, 6, 18, 0.40);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 18px 18px 12px 18px;
        box-shadow: 0 18px 40px rgba(0,0,0,0.35);
    }

    /* ====== Dataframe container (giảm cảm giác nền trắng) ====== */
    div[data-testid="stDataFrame"] {
        background: rgba(3, 6, 18, 0.35);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 8px;
    }

    /* divider */
    hr { border-color: rgba(255,255,255,0.10) !important; }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def get_analyzer():
    return BankingAnalyzer()

# =========================
# HEADER (NO LOGO)
# =========================
st.title("Phân tích đánh giá App Ngân hàng số")
st.markdown('<div class="subtitle">Dashboard thống kê dữ liệu & kiểm thử mô hình NLP</div>', unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["Thống kê", "Kiểm thử câu văn"])

# =========================
# TAB 1: DASHBOARD
# =========================
with tab1:
    st.write("Dữ liệu đầu vào: file CSV đã gán nhãn")

    df = None
    try:
        df = pd.read_csv("data/raw_reviews.csv")
        st.success("Đã load dữ liệu từ data/raw_reviews.csv")
    except Exception:
        st.warning("Không tìm thấy file CSV. Vui lòng upload file.")
        uploaded = st.file_uploader("Upload CSV đã gán nhãn", type=["csv"])
        if uploaded is not None:
            df = pd.read_csv(uploaded)

    if df is None or df.empty:
        st.info("Chưa có dữ liệu để hiển thị.")
    else:
        render_dashboard(df)

# =========================
# TAB 2: TEST SENTENCE
# =========================
with tab2:
    st.markdown("### Nhập một câu đánh giá để kiểm thử mô hình")

    colL, colR = st.columns([4, 1])

    with colL:
        text = st.text_area(
            "Nội dung đánh giá",
            placeholder="Ví dụ: App hay lỗi đăng nhập, không nhận OTP...",
            height=140,
            label_visibility="visible",
        )

    with colR:
        st.write("")
        st.write("")
        run_btn = st.button("PHÂN TÍCH", use_container_width=True)

    if run_btn:
        if not text.strip():
            st.warning("Vui lòng nhập nội dung.")
        else:
            try:
                t0 = time.perf_counter()
                analyzer = get_analyzer()

                with st.spinner("Đang phân tích..."):
                    result = analyzer.analyze(text)

                elapsed = time.perf_counter() - t0
                st.success(f"Phân tích xong trong {elapsed:.2f} giây")
                st.caption(f"Text sau khi làm sạch: {result.get('text_clean','')}")

                left, right = st.columns(2)

                with left:
                    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
                    st.markdown("### Cảm xúc")
                    st.write(result.get("sentiment", ""))
                    st.progress(min(max(float(result.get("sentiment_score", 0.0)), 0.0), 1.0))
                    st.caption(f"Độ tin cậy: {float(result.get('sentiment_score', 0.0))*100:.2f}%")
                    st.markdown("</div>", unsafe_allow_html=True)

                with right:
                    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
                    st.markdown("### Chủ đề")
                    st.write(result.get("topic", ""))
                    st.progress(min(max(float(result.get("topic_score", 0.0)), 0.0), 1.0))
                    st.caption(f"Độ tin cậy: {float(result.get('topic_score', 0.0))*100:.2f}%")
                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error("Analyzer/Model đang lỗi khi chạy dự đoán.")
                st.code(str(e))
