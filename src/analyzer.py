import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from src.preprocess import clean_text


class BankingAnalyzer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"⚙️ Đang khởi tạo Analyzer trên thiết bị: {self.device}")

        # --- 1) TOPIC MODEL ---
        self.path_topic = "models/topic/"
        if not os.path.exists(self.path_topic):
            raise FileNotFoundError(f"❌ Lỗi: Không tìm thấy thư mục {self.path_topic}")

        print("⏳ Đang load Topic Model...")
        self.tokenizer_topic = AutoTokenizer.from_pretrained(self.path_topic)
        self.model_topic = AutoModelForSequenceClassification.from_pretrained(self.path_topic)
        self.model_topic.to(self.device)
        self.model_topic.eval()

        # --- 2) SENTIMENT MODEL ---
        self.path_sent = "models/sentiment/"
        if not os.path.exists(self.path_sent):
            raise FileNotFoundError(f"❌ Lỗi: Không tìm thấy thư mục {self.path_sent}")

        print("⏳ Đang load Sentiment Model...")
        self.tokenizer_sent = AutoTokenizer.from_pretrained(self.path_sent)
        self.model_sent = AutoModelForSequenceClassification.from_pretrained(self.path_sent)
        self.model_sent.to(self.device)
        self.model_sent.eval()

        # --- 3) LABEL MAP ---
        self.topic_map = {
            0: "Khác / Chung chung",
            1: "Tài khoản & Bảo mật",
            2: "Giao dịch & Tài chính",
            3: "Trải nghiệm (Lag/UI)",
        }
        self.sent_map = {
            0: "Tiêu cực",
            1: "Trung tính",
            2: "Tích cực",
        }

        print("✅ Đã load xong cả 2 Model!")

    def _predict_one(self, text: str, tokenizer, model):
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=128,
            padding=True,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)

        conf, idx = torch.max(probs, dim=1)
        return idx.item(), conf.item()

    def predict(self, raw_text: str):
        clean_content = clean_text(raw_text)

        topic_id, topic_score = self._predict_one(clean_content, self.tokenizer_topic, self.model_topic)
        sent_id, sent_score = self._predict_one(clean_content, self.tokenizer_sent, self.model_sent)

        topic_label = self.topic_map.get(topic_id, "Không xác định")
        sent_label = self.sent_map.get(sent_id, "Không xác định")

        return {
            "text_clean": clean_content,

            # keys mà UI thường dùng
            "topic": topic_label,
            "topic_score": round(topic_score, 4),

            "sentiment": sent_label,
            "sentiment_score": round(sent_score, 4),

            # keys dự phòng
            "topic_label": topic_label,
            "sentiment_label": sent_label,
        }

    def analyze(self, raw_text: str):
        # alias để app.py gọi analyzer.analyze() luôn chạy
        return self.predict(raw_text)
