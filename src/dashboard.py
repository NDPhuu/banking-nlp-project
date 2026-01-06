import pandas as pd
import streamlit as st
import plotly.express as px

SENTIMENT_MAP = {
    0: "Tiêu cực",
    1: "Trung tính",
    2: "Tích cực",
}

TOPIC_MAP = {
    0: "Khác / Chung",
    1: "Tài khoản & Bảo mật",
    2: "Giao dịch & Tài chính",
    3: "Trải nghiệm ứng dụng",
}

# Remap từ label cũ (0..5) -> label mới (0..3)
TOPIC_REMAP_OLD_TO_NEW = {
    0: 0,  # others -> others
    1: 1,  # account_identity -> account_security
    2: 2,  # transaction -> transaction_finance
    3: 3,  # performance -> app_experience
    4: 0,  # customer_service -> others
    5: 2,  # fees_pricing -> transaction_finance
}

# Bảng màu (nhiều màu, hợp nền tối)
COLOR_SEQ = [
    "#A78BFA",  # tím
    "#22D3EE",  # cyan
    "#34D399",  # xanh ngọc
    "#F472B6",  # hồng
    "#FBBF24",  # vàng
    "#60A5FA",  # xanh dương nhạt
    "#FB7185",  # đỏ hồng
]

# ====== Font sizes for charts (tùy chỉnh ở đây) ======
X_TICK_SIZE = 15
Y_TICK_SIZE = 14
LEGEND_SIZE = 14
TITLE_SIZE = 16


def _inject_dashboard_css():
    st.markdown(
        """
        <style>
        .dash-title {
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: -0.3px;
            color: #F3F4F6;
            margin: 0.2rem 0 1rem 0;
        }

        .kpi-wrap {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin-bottom: 14px;
        }
        .kpi {
            background: rgba(17, 24, 39, 0.55);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 16px;
            padding: 14px 16px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.30);
            backdrop-filter: blur(10px);
        }
        .kpi-label {
            font-size: 0.92rem;
            color: rgba(229,231,235,0.75);
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 2rem;
            font-weight: 800;
            color: #F9FAFB;
            line-height: 1;
        }

        .tbl-wrap {
            background: rgba(17, 24, 39, 0.55);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 16px;
            padding: 12px 12px 6px 12px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.30);
            backdrop-filter: blur(10px);
            overflow-x: auto;
        }
        table.dark-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
            color: #E5E7EB;
        }
        table.dark-table thead th {
            text-align: left;
            font-weight: 700;
            color: #F3F4F6;
            border-bottom: 1px solid rgba(255,255,255,0.10);
            padding: 10px 10px;
            background: rgba(255,255,255,0.03);
        }
        table.dark-table tbody td {
            border-bottom: 1px solid rgba(255,255,255,0.06);
            padding: 10px 10px;
            color: rgba(229,231,235,0.90);
        }
        table.dark-table tbody tr:hover td {
            background: rgba(255,255,255,0.04);
        }

        .section-h {
            font-size: 1.15rem;
            font-weight: 800;
            color: #F3F4F6;
            margin: 1.0rem 0 0.6rem 0;
            letter-spacing: -0.2px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _to_dark_table(df: pd.DataFrame) -> str:
    html = df.to_html(index=False, escape=False)
    html = html.replace('<table border="1" class="dataframe">', '<table class="dark-table">')
    return f'<div class="tbl-wrap">{html}</div>'


def _style_fig(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB"),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            title="",
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB", size=LEGEND_SIZE),
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="#E5E7EB", size=X_TICK_SIZE),
            title_font=dict(color="#E5E7EB", size=TITLE_SIZE),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            tickfont=dict(color="#E5E7EB", size=Y_TICK_SIZE),
            title_font=dict(color="#E5E7EB", size=TITLE_SIZE),
        ),
    )
    fig.update_traces(marker_line_width=0)
    return fig


def render_dashboard(df: pd.DataFrame):
    _inject_dashboard_css()

    st.markdown('<div class="dash-title">Thống kê dữ liệu đánh giá đã gán nhãn</div>', unsafe_allow_html=True)

    if df is None or df.empty:
        st.warning("Chưa có dữ liệu để hiển thị.")
        return

    # ===== KPI cards =====
    total_reviews = len(df)
    num_apps = df["app_name"].nunique() if "app_name" in df.columns else None

    # Số chủ đề phải tính theo label đã remap (ra 4)
    if "label_topic" in df.columns:
        topic_series_remap = df["label_topic"].map(lambda x: TOPIC_REMAP_OLD_TO_NEW.get(x, x))
        num_topics = topic_series_remap.nunique()
    else:
        topic_series_remap = None
        num_topics = None

    st.markdown(
        f"""
        <div class="kpi-wrap">
            <div class="kpi">
                <div class="kpi-label">Tổng số đánh giá</div>
                <div class="kpi-value">{total_reviews}</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">Số app</div>
                <div class="kpi-value">{num_apps if num_apps is not None else "-"}</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">Số chủ đề</div>
                <div class="kpi-value">{num_topics if num_topics is not None else "-"}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ===== Sentiment =====
    st.markdown('<div class="section-h">Phân bố cảm xúc</div>', unsafe_allow_html=True)

    if "label_sentiment" not in df.columns:
        st.warning("Thiếu cột label_sentiment trong dữ liệu.")
    else:
        sentiment_counts = df["label_sentiment"].value_counts().sort_index()
        sentiment_df = pd.DataFrame(
            {
                "Cảm xúc": [SENTIMENT_MAP.get(int(i), str(i)) for i in sentiment_counts.index],
                "Số lượng": sentiment_counts.values,
            }
        )

        st.markdown(_to_dark_table(sentiment_df), unsafe_allow_html=True)

        fig_sent = px.bar(
            sentiment_df,
            x="Cảm xúc",
            y="Số lượng",
            color="Cảm xúc",
            color_discrete_sequence=COLOR_SEQ,
        )
        fig_sent.update_layout(xaxis_title="", yaxis_title="")
        st.plotly_chart(_style_fig(fig_sent), use_container_width=True)

    st.divider()

    # ===== Topic =====
    st.markdown('<div class="section-h">Phân bố chủ đề</div>', unsafe_allow_html=True)

    if "label_topic" not in df.columns:
        st.warning("Thiếu cột label_topic trong dữ liệu.")
    else:
        # dùng series remap đã tính ở KPI nếu có, tránh tính lại
        if topic_series_remap is None:
            topic_series_remap = df["label_topic"].map(lambda x: TOPIC_REMAP_OLD_TO_NEW.get(x, x))

        topic_counts = topic_series_remap.value_counts().sort_index()

        topic_df = pd.DataFrame(
            {
                "Chủ đề": [TOPIC_MAP.get(int(i), str(i)) for i in topic_counts.index],
                "Số lượng": topic_counts.values,
            }
        )

        st.markdown(_to_dark_table(topic_df), unsafe_allow_html=True)

        fig_topic = px.bar(
            topic_df,
            x="Chủ đề",
            y="Số lượng",
            color="Chủ đề",
            color_discrete_sequence=COLOR_SEQ,
        )
        fig_topic.update_layout(xaxis_title="", yaxis_title="")
        fig_topic.update_xaxes(tickangle=-30)
        st.plotly_chart(_style_fig(fig_topic), use_container_width=True)

    st.divider()

    # ===== Preview =====
    st.markdown('<div class="section-h">Xem nhanh dữ liệu</div>', unsafe_allow_html=True)

    preview = df.head(20).copy()

    if "label_sentiment" in preview.columns:
        preview["label_sentiment"] = preview["label_sentiment"].map(lambda x: SENTIMENT_MAP.get(x, x))

    if "label_topic" in preview.columns:
        preview["label_topic"] = preview["label_topic"].map(
            lambda x: TOPIC_MAP.get(TOPIC_REMAP_OLD_TO_NEW.get(x, x), x)
        )

    st.markdown(_to_dark_table(preview), unsafe_allow_html=True)
