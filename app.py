mlit as st
from transformers import pipeline
import logging
import torch
import random
from googletrans import GoogleTranslator

class MentalHealthApp:
    def __init__(self):
        self.setup_models()
        self.setup_memory()

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
                "stress": "Stress kéo dài có thể ảnh hưởng đến cả thể chất và tinh thần. Hãy thử các bài tập thư giãn đơn giản.",
                "anxiety": "Lo âu là phản ứng tự nhiên của cơ thể trước các tình huống căng thẳng. Thở sâu và thiền định có thể giúp ích.",
                "depression": "Trầm cảm là một tình trạng cần được quan tâm và điều trị. Đừng ngần ngại tìm sự giúp đỡ từ chuyên gia.",
                "healing": "Chữa lành là một hành trình, không phải đích đến. Mỗi bước nhỏ đều có ý nghĩa."
            }

        except Exception as e:
            logging.error(f"❌ Model initialization error: {e}")

    def setup_memory(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []

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
        """Tạo phản hồi thông minh dựa trên cảm xúc và nội dung"""
        response = random.choice(self.responses[emotion])
        
        # Phân tích nội dung và thêm lời khuyên tâm lý nếu phù hợp
        for topic, advice in self.therapy_topics.items():
            if topic in text.lower():
                response += f"\n\n{advice}"
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

# Chạy ứng dụng
if __name__ == "__main__":
    app = MentalHealthApp()
    app.run()
