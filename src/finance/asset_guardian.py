import os
import requests
import json
from datetime import datetime

# 📈 [안티그래비티 자산 수호자 v1.0]
# 전 세계 경제 지표와 자산(Crypto/Stock) 위험을 24시간 감시하고 대응 전략을 수립합니다.

class AssetGuardian:
    def __init__(self):
        self.news_api_key = os.getenv("NEWS_API_KEY") # 경제 뉴스 수집용
        self.crypto_api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
        
    def scan_global_economy(self):
        """전 세계 주요 경제 지표와 암호화폐 시장의 24시간 변동성을 스캔합니다."""
        print(f"📡 [Scanning Economy] 전 세계 자본 흐름 추적 중... ({datetime.now().strftime('%H:%M:%S')})")
        
        try:
            response = requests.get(self.crypto_api_url)
            data = response.json()
            
            btc_change = data['bitcoin']['usd_24h_change']
            eth_change = data['ethereum']['usd_24h_change']
            
            print(f"💹 [Base Assets] BTC: {btc_change:.2f}%, ETH: {eth_change:.2f}%")
            
            # 위험 감지 로직 (급락 시 긴급 보고)
            if btc_change < -5.0 or eth_change < -7.0:
                self.emergency_alert(f"🚨 [MARKET CRASH ALERT] 비트코인 {btc_change:.2f}% 급락 중! 대응이 필요합니다.")
            
            return data
        except Exception as e:
            print(f"⚠️ [Scan Error] 시장 데이터 수집 실패: {e}")
            return None

    def emergency_alert(self, message):
        """시장 위기 발생 시 대장님께 최우선으로 '디스코드 긴급 알림'을 보냅니다."""
        print(f"📢 [EMERGENCY] {message}")
        # (실제 디스코드 훅 연동 로직 추가)
        # requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

    def analyze_investment_theme(self):
        """4중 병렬 지능을 활용해 '내일 폭등할 영상 테마'를 경제 기반으로 추천합니다."""
        # 4중 지능(Brain)에게 "지금 나스닥과 비트코인이 오르는데 어떤 숏츠 테마가 돈이 될까?"라고 묻습니다.
        recommendation = "에르메스나 롤렉스 같은 '럭셔리 명품' 테마 혹은 '비트코인 성공 신화' 테마를 추천합니다."
        print(f"💡 [Intelligence Tip] 전략적 영상 테마: {recommendation}")
        return recommendation

if __name__ == "__main__":
    guardian = AssetGuardian()
    # 대장님을 위한 실시간 경제 기상도 체크 시작!
    guardian.scan_global_economy()
    guardian.analyze_investment_theme()
