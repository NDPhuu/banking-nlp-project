import streamlit as st
import pandas as pd
import plotly.express as px # Dùng Plotly cho đẹp (cần cài: poetry add plotly)

def render_dashboard(df):
    st.subheader("📈 Thống kê dữ liệu đánh giá")

    # Kiểm tra xem file CSV đã có cột nhãn chưa
    # Nếu chưa có (mới cào thô), ta sẽ vẽ biểu đồ dựa trên Score (Số sao) tạm
    has_label = 'label_topic' in df.columns

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Phân bố Điểm đánh giá (Sao)**")
        score_counts = df['score'].value_counts().reset_index()
        score_counts.columns = ['Số sao', 'Số lượng']
        fig_score = px.pie(score_counts, values='Số lượng', names='Số sao', hole=0.4)
        st.plotly_chart(fig_score, width = 'stretch')

    with col2:
        if has_label:
            st.write("**Phân bố Chủ đề (Topics)**")
            # Map số sang chữ để hiển thị cho đẹp
            topic_map = {
                0: "Khác / Chung chung",
                1: "Tài khoản & Bảo mật",
                2: "Giao dịch & Tài chính",
                3: "Trải nghiệm (Lag/UI)"
            }
            df['Topic Name'] = df['label_topic'].map(topic_map)
            topic_counts = df['Topic Name'].value_counts().reset_index()
            topic_counts.columns = ['Chủ đề', 'Số lượng']
            
            fig_topic = px.bar(topic_counts, x='Số lượng', y='Chủ đề', orientation='h', color='Số lượng')
            st.plotly_chart(fig_topic, width = 'stretch')
        else:
            st.info("⚠️ File CSV chưa có cột 'label_topic'. Hãy gán nhãn dữ liệu để xem biểu đồ Chủ đề.")
            st.write("**Xu hướng theo thời gian (Ngày)**")
            # Chuyển cột 'at' sang datetime
            df['at'] = pd.to_datetime(df['at'])
            daily_counts = df.groupby(df['at'].dt.date).size().reset_index(name='Số lượng')
            fig_line = px.line(daily_counts, x='at', y='Số lượng')
            st.plotly_chart(fig_line, width = 'stretch')

    # Metrics tổng quan
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Tổng số đánh giá", len(df))
    m2.metric("Điểm trung bình", f"{df['score'].mean():.2f} ⭐")
    m3.metric("Ngày mới nhất", pd.to_datetime(df['at'], dayfirst=True).max().strftime('%d/%m/%Y'))