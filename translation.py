from deep_translator import GoogleTranslator

def translate_text(text, source_lang="vi", target_lang="en"):
    return GoogleTranslator(source=source_lang, target=target_lang).translate(text)

# Ví dụ chạy
if __name__ == "__main__":
    result = translate_text("Xin chào", source_lang="vi", target_lang="en")
    print(result)

def setup_models(self):
    # Thêm vào self.therapy_topics
    self.therapy_topics.update({
        "mất ngủ": {
            "giải thích": "Mất ngủ ảnh hưởng đến chất lượng cuộc sống",
            "giải pháp": "Thiết lập thói quen ngủ, tránh caffeine, thực hành thiền"
        },
        "cô đơn": {
            "giải thích": "Cô đơn là cảm giác thiếu kết nối với người khác",
            "giải pháp": "Tham gia các hoạt động xã hội, chia sẻ với bạn bè"
        },
        "tổn thương": {
            "giải thích": "Tổn thương tâm lý cần thời gian để chữa lành",
            "giải pháp": "Viết nhật ký, tham vấn chuyên gia, thực hành self-care"
        }
    })
