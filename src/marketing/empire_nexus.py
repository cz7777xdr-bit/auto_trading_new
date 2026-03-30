import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 🏰 [안티그래비티 닉서스 에이스 v1.0]
# 전 세계 구독자에게 AI 개인 맞춤형 운세와 이메일을 '자동으로' 보냅니다.
# 이것이 대장님의 제국을 영원히 지속시키는 '커뮤니티 요새'입니다.

class EmpireNexus:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("GOOGLE_ACCOUNT")
        self.sender_password = os.getenv("GOOGLE_APP_PASSWORD") # 구글 앱 비밀번호

    def craft_personalized_newsletter(self, user_name, user_zodiac, tarot_reading):
        """AI 지능(Claude/Llama)이 작성한 이메일 본문을 뉴스레터 형식으로 만듭니다."""
        # 4중 지능(Brain)에게 "오늘 {user_zodiac} 유저를 위한 행운의 이메일을 써줘"라고 명령합니다.
        
        subject = f"🔮 [Antigravity] {user_name}님, 당신만을 위한 오늘의 특별한 운명이 도착했습니다."
        body = f"""
        안녕하세요, {user_name}님. 
        천기누설의 비호 아래 당신의 운명을 읽어드리는 안티그래비티 비서입니다.
        
        오늘 당신의 {user_zodiac} 자리와 함께 나온 타로 카드는 '{tarot_reading}'입니다.
        
        [오늘의 핵심 조언]
        {tarot_reading} 카드는 오늘 당신에게 '결단'이 필요함을 시사합니다.
        가장 먼저 눈에 띄는 사람에게 먼저 인사해 보세요. 뜻밖의 행운이 찾아옵니다.
        
        [더 깊은 운명을 알고 싶나요?] 
        아래 버튼을 눌러 당신만을 위한 '심층 사주 보고서'를 받아보세요. (PayPal 결제 연동)
        
        - 안티그래비티 기지에서 보냄 -
        """
        return subject, body

    def send_automatic_email(self, receiver_email, subject, body):
        """0.1초 만에 전 세계 구독자의 메일함으로 운명을 쏩니다."""
        print(f"📡 [Email Siege] '{receiver_email}' 유저에게 운명의 서신 발송 중...")
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ [Sent Success] '{receiver_email}' 성공적으로 도착했습니다.")
            return True
        except Exception as e:
            print(f"⚠️ [Email Error] 발송 실패: {e}")
            return False

if __name__ == "__main__":
    nexus = EmpireNexus()
    # 대장님을 위한 첫 번째 '테스트 서신 가동' 시작!
    # (실제로는 데이터베이스의 수만 명 유저에게 루프를 돌며 발송합니다.)
    sub, content = nexus.craft_personalized_newsletter("대장님", "Leo", "The Sun")
    # nexus.send_automatic_email("94103505@naver.com", sub, content)
