import pandas as pd
from google_play_scraper import reviews, Sort
import os
import time
import random

# Định nghĩa các hằng số cấu hình 
APP_DICT_CONFIG = {
    # == VÍ ĐIỆN TỬ & NGÂN HÀNG SỐ ==
    'Momo': 'com.mservice.momotransfer',
    'ZaloPay': 'vn.com.vng.zalopay',
    'Viettel Money': 'com.bplus.vtpay',
    'Cake by VPBank': 'xyz.be.cake',
    'Timo Digital Bank': 'io.lifestyle.plus',
    'TNEX': 'vn.tnex.consumer',

    # == NGÂN HÀNG TRUYỀN THỐNG ==
    'Vietcombank': 'com.VCB',
    'MB Bank': 'com.mbmobile',
    'Techcombank Mobile': 'vn.com.techcombank.bb.app',
    'VPBank NEO': 'com.vnpay.vpbankonline',
    'BIDV SmartBanking': 'com.vnpay.bidv',
    'Agribank Plus': 'com.vnpay.Agribank3g',
    'VietinBank iPay': 'com.vietinbank.ipay',
    'ACB ONE': 'mobile.acb.com.vn',
    'TPBank Mobile': 'com.tpb.mb.gprsandroid',
    'Sacombank mBanking': 'src.com.sacombank',
    'VIB Mobile': 'com.vn.vib.mobileapp',
    'MSB mBank': 'vn.com.msb.smartBanking'
}

class BankingReviewScraper:
    """
    Class chịu trách nhiệm cào dữ liệu đánh giá từ Google Play Store
    cho danh sách các ứng dụng ngân hàng/tài chính.
    """
    def __init__(self, app_dict, count_per_app=300):
        self.app_dict = app_dict
        self.count_per_app = count_per_app
        self.all_reviews = []

    def _auto_label_sentiment(self, score):
        """
        Hàm nội bộ: Gán nhãn cảm xúc dựa trên điểm số (score).
        Logic: 1-2 sao (Tiêu cực-0), 3 sao (Trung tính-1), 4-5 sao (Tích cực-2).
        """
        if score <= 2:
            return 0
        elif score == 3:
            return 1
        else:
            return 2

    def scrape_data(self):
        """
        Thực hiện cào dữ liệu từ danh sách ứng dụng đã cấu hình.
        """
        print(f"BẮT ĐẦU CÀO DỮ LIỆU")
        print(f"Mục tiêu: {len(self.app_dict)} apps x {self.count_per_app} reviews.")
        print("=" * 60)

        for app_name, app_id in self.app_dict.items():
            print(f"Đang xử lý: {app_name} (ID: {app_id})...")
            try:
                result, _ = reviews(
                    app_id,
                    lang='vi',
                    country='vn',
                    sort=Sort.NEWEST,
                    count=self.count_per_app
                )
                
                if len(result) > 0:
                    for r in result:
                        r['app_name'] = app_name
                    self.all_reviews.extend(result)
                    print(f"   Thành công: Lấy được {len(result)} reviews.")
                else:
                    print(f"   Cảnh báo: 0 kết quả (Check mạng/App chặn).")

                time.sleep(random.randint(2, 4)) # Nghỉ ngẫu nhiên tránh spam request

            except Exception as e:
                print(f"   LỖI: {e}")
        
        print("=" * 60)
        print(f"HOÀN TẤT! Tổng số dòng thu được: {len(self.all_reviews)}")

    def save_to_csv(self, output_folder='data', filename='raw_reviews.csv'):
        """
        Xử lý dữ liệu thô, gán nhãn và lưu ra file CSV.
        """
        if len(self.all_reviews) == 0:
            print("Không có dữ liệu để lưu.")
            return

        df = pd.DataFrame(self.all_reviews)
        # Chọn các cột cần thiết
        df = df[['app_name', 'content', 'score', 'at']]

        # Áp dụng gán nhãn
        df['label_sentiment'] = df['score'].apply(self._auto_label_sentiment)
        df['label_topic'] = '' # Cột trống để gán nhãn topic sau này

        # Tạo thư mục nếu chưa có
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_path = os.path.join(output_folder, filename)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"File mới đã lưu tại: {output_path}")

# --- PHẦN CHẠY CHƯƠNG TRÌNH (MAIN) ---
if __name__ == "__main__":
    # Khởi tạo đối tượng Scraper
    scraper = BankingReviewScraper(APP_DICT_CONFIG, count_per_app=300)
    
    # Thực hiện cào dữ liệu
    scraper.scrape_data()
    
    # Lưu file
    scraper.save_to_csv()