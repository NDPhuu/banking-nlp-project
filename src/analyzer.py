# src/analyzer.py
# Này là Class Demo để test UI của dự án (Mẫn)
class BankingAnalyzer:
    def __init__(self):
        pass # Chưa load model thật
    def predict(self, text):
        # Trả về kết quả giả định để test UI
        return {
            "sentiment_label": "Tiêu cực (Giả)",
            "sentiment_score": 0.99,
            "topic_label": "Lỗi Fake",
            "topic_score": 0.88
        }
