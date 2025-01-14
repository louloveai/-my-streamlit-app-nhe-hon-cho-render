import streamlit as st
from transformers import pipeline
import logging
import torch
import random
from deep_translator import GoogleTranslator
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MentalHealthApp:
    def __init__(self):
        self.setup_models()
        self.google_search = GoogleSearch()
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        # Thêm context memory
        self.context_memory = {
            "last_emotion": None,
            "conversation_topics": [],
            "therapy_progress": {}
        }

    def setup_models(self):
        """Khởi tạo các models AI"""
        try:
            self.analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            self.translator = GoogleTranslator(source='vi', target='en')
            
            # Thêm responses thông minh với kiến thức tâm lý
            self.responses = {
                "POSITIVE": [
                    "Thật tuyệt vời! Cảm xúc tích cực sẽ giúp tăng endorphin - hormone hạnh phúc trong cơ thể bạn.",
                    "Khi bạn vui, não bộ sẽ tiết ra serotonin. Hãy duy trì năng lượng tích cực này nhé!",
                    "Niềm vui của bạn là một phần quan trọng trong hành trình chữa lành. Hãy trân trọng khoảnh khắc này.",
                    "Tôi rất vui khi thấy năng lượng tích cực của bạn. Điều này rất tốt cho quá trình chữa lành.",
                    "Cảm xúc tích cực giúp giải phóng endorphin - hormone hạnh phúc trong cơ thể bạn.",
                    "Hãy giữ vững tinh thần này nhé! Mỗi khoảnh khắc tích cực đều rất quý giá."
                    "Tôi rất vui khi thấy bạn có trạng thái tích cực. Điều này rất tốt cho sức khỏe tinh thần."
                ],
                "NEGATIVE": [
                    "Tôi hiểu cảm giác đó. Đôi khi, chấp nhận cảm xúc tiêu cực cũng là một phần của quá trình chữa lành.",
                    "Hãy thử phương pháp thở sâu 4-7-8: Hít vào 4 giây, giữ 7 giây, và thở ra 8 giây. Điều này sẽ giúp bạn bình tĩnh hơn.",
                    "Bạn biết không, cảm xúc tiêu cực cũng là một phần tự nhiên của con người. Đừng quá khắt khe với bản thân.",
                    "Trong tâm lý học, chúng ta gọi đây là khoảnh khắc cần được lắng nghe và thấu hiểu. Bạn muốn chia sẻ thêm không?"
                ]
            }

            # Thêm từ điển chủ đề tâm lý
            self.therapy_topics = {
                "stress": {
                    "giải thích": "Stress kéo dài có thể ảnh hưởng đến cả thể chất và tinh thần",
                    "giải pháp": "Hãy thử các bài tập thư giãn đơn giản, thiền định 10 phút mỗi ngày"
                },
                "anxiety": {
                    "giải thích": "Lo âu là phản ứng tự nhiên của cơ thể trước các tình huống căng thẳng",
                    "giải pháp": "Thở sâu và thiền định có thể giúp ích, tập trung vào hiện tại"
                },
                "depression": {
                    "giải thích": "Trầm cảm là một tình trạng cần được quan tâm và điều trị",
                    "giải pháp": "Đừng ngần ngại tìm sự giúp đỡ từ chuyên gia, duy trì các hoạt động yêu thích"
                },
                "healing": {
                    "giải thích": "Chữa lành là một hành trình, không phải đích đến",
                    "giải pháp": "Mỗi bước nhỏ đều có ý nghĩa, hãy kiên nhẫn với bản thân"
                },
                "mất ngủ": {
                    "giải thích": "Mất ngủ ảnh hưởng đến chất lượng cuộc sống và sức khỏe tinh thần",
                    "giải pháp": "Thiết lập thói quen ngủ, tránh caffeine, thực hành thiền trước khi ngủ"
                },
                "cô đơn": {
                    "giải thích": "Cô đơn là cảm giác thiếu kết nối với người khác",
                    "giải pháp": "Tham gia các hoạt động xã hội, chia sẻ với bạn bè, tìm sở thích mới"
                },
                "tổn thương": {
                    "giải thích": "Tổn thương tâm lý cần thời gian để chữa lành",
                    "giải pháp": "Viết nhật ký, tham vấn chuyên gia, thực hành self-care mỗi ngày"
                }
            }

        except Exception as e:
            logging.error(f"❌ Model initialization error: {e}")

    def analyze_emotion(self, text):
        """Phân tích cảm xúc với DistilBERT"""
        try:
            english_text = self.translator.translate(text)
            result = self.analyzer(english_text)
            return result['label'].lower()
        except Exception as e:
            logging.error(f"Lỗi phân tích cảm xúc: {e}")
            return "neutral"

    def get_response(self, emotion, text):
        """Tạo phản hồi thông minh với khả năng search"""
        response = random.choice(self.responses[emotion])
        
        # Kiểm tra nếu cần search
        if any(keyword in text.lower() for keyword in ["tìm kiếm", "search", "tra cứu", "tìm hiểu"]):
            search_results = self.google_search.search_and_summarize(text)
            if search_results:
                response += "\n\nTôi đã tìm thấy một số thông tin liên quan:\n"
                for idx, result in enumerate(search_results, 1):
                    response += f"\n{idx}. {result}\n"
        
        # Thêm lời khuyên tâm lý nếu phù hợp
        for topic, advice in self.therapy_topics.items():
            if topic in text.lower():
                response += f"\n\n{advice['giải thích']}. {advice['giải pháp']}"
                
                # Chủ động search thêm thông tin
                search_query = f"cách điều trị {topic} tâm lý học"
                extra_info = self.google_search.search_and_summarize(search_query, num_results=1)
                if extra_info:
                    response += f"\n\nThông tin bổ sung: {extra_info[0]}"
                break
            
        return response

    def setup_streamlit(self):
        # Bỏ dark/light mode toggle, chỉ dùng dark theme
        st.markdown(
            """
            <style>
            /* Màu nền đen và chữ trắng */
            .stApp {
                background-color: black !important;
            }
            
            /* Màu chữ trắng cho tất cả text */
            .stApp, .stMarkdown, .stTextInput, p, h1, h2, h3 {
                color: white !important;
            }
            
            /* Màu chữ trắng cho input */
            .stTextInput > div > div > input {
                color: white !important;
            }
            
            /* Màu chữ trắng cho chat messages */
            .stChatMessage {
                color: white !important;
                background-color: rgba(255, 255, 255, 0.1) !important;
            }
            </style>
            """, unsafe_allow_html=True
        )
        st.title("🌿 AI Chữa Lành")

        if prompt := st.chat_input("Chia sẻ cảm xúc của bạn..."):
            emotion = self.analyze_emotion(prompt)
            response = self.get_response(emotion, prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    def update_context(self, emotion, text):
        """Cập nhật context của cuộc trò chuyện"""
        self.context_memory["last_emotion"] = emotion
        # Theo dõi chủ đề
        for topic in self.therapy_topics.keys():
            if topic in text.lower():
                self.context_memory["conversation_topics"].append(topic)
        # Cập nhật tiến trình
        self.context_memory["therapy_progress"][emotion] = \
            self.context_memory["therapy_progress"].get(emotion, 0) + 1

    def run(self):
        """Chạy ứng dụng Streamlit"""
        try:
            self.setup_streamlit()
        except Exception as e:
            logging.error(f"Runtime error: {e}")
            st.error("Có lỗi xảy ra, vui lòng thử lại sau.")

class GoogleSearch:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def search_and_summarize(self, query, num_results=3):
        """Tìm kiếm Google và tóm tắt kết quả"""
        try:
            results = []
            search_results = search(query, num_results=num_results)
            
            for url in search_results:
                try:
                    response = requests.get(url, headers=self.headers, timeout=5)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Lấy text từ các thẻ p
                    paragraphs = soup.find_all('p')
                    text = ' '.join([p.text for p in paragraphs])
                    
                    # Làm sạch text
                    text = re.sub(r'\s+', ' ', text).strip()
                    if text:
                        results.append(text[:500])  # Giới hạn độ dài
                except:
                    continue
                    
            return results
        except Exception as e:
            logging.error(f"Search error: {e}")
            return []

# Chạy ứng dụng
if __name__ == "__main__":
    app = MentalHealthApp()
    app.run()

