import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.preprocess import clean_text
import os

class BankingAnalyzer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"⚙️ Đang khởi tạo Analyzer trên thiết bị: {self.device}")

        # --- 1. LOAD MODEL TOPIC (CHỦ ĐỀ) ---
        path_topic = "models/topic/"
        if os.path.exists(path_topic):
            print("⏳ Đang load Topic Model...")
            self.tokenizer_topic = AutoTokenizer.from_pretrained(path_topic)
            self.model_topic = AutoModelForSequenceClassification.from_pretrained(path_topic)
            self.model_topic.to(self.device)
            self.model_topic.eval()
        else:
            raise FileNotFoundError(f"❌ Lỗi: Không tìm thấy thư mục {path_topic}")

        # --- 2. LOAD MODEL SENTIMENT (CẢM XÚC) ---
        path_sent = "models/sentiment/"
        if os.path.exists(path_sent):
            print("⏳ Đang load Sentiment Model...")
            self.tokenizer_sent = AutoTokenizer.from_pretrained(path_sent)
            self.model_sent = AutoModelForSequenceClassification.from_pretrained(path_sent)
            self.model_sent.to(self.device)
            self.model_sent.eval()
        else:
            raise FileNotFoundError(f"❌ Lỗi: Không tìm thấy thư mục {path_sent}")

        # --- 3. ĐỊNH NGHĨA NHÃN (MAPPING) ---
        # Nhãn Topic (4 loại - Như đã chốt)
        self.topic_map = {
            0: "Khác / Chung chung",
            1: "Tài khoản & Bảo mật",
            2: "Giao dịch & Tài chính",
            3: "Trải nghiệm (Lag/UI)"
        }

        # Nhãn Sentiment (3 loại - Theo code train của Cường)
        self.sent_map = {
            0: "Tiêu cực",
            1: "Trung tính",
            2: "Tích cực"
        }
        print("✅ Đã load xong cả 2 Model!")

    def predict(self, raw_text):
        # 1. Làm sạch text
        clean_content = clean_text(raw_text)
        
        # 2. Hàm phụ để chạy model (tránh viết lặp lại)
        def get_prediction(text, tokenizer, model):
            inputs = tokenizer(
                text, return_tensors="pt", truncation=True, max_length=128, padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            conf, idx = torch.max(probs, dim=1)
            return idx.item(), conf.item()

        # 3. Chạy Model Topic
        topic_id, topic_score = get_prediction(clean_content, self.tokenizer_topic, self.model_topic)

        # 4. Chạy Model Sentiment
        sent_id, sent_score = get_prediction(clean_content, self.tokenizer_sent, self.model_sent)

        # 5. Trả về kết quả gộp
        return {
            "text_clean": clean_content,
            
            # Kết quả Topic
            "topic_label": self.topic_map.get(topic_id, "Không xác định"),
            "topic_score": round(topic_score, 4),
            
            # Kết quả Sentiment
            "sentiment_label": self.sent_map.get(sent_id, "Không xác định"),
            "sentiment_score": round(sent_score, 4)
        }