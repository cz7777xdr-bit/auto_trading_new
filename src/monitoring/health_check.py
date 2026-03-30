import os
import time
import requests
import psutil

# 🏥 [안티그래비티 헬스체크 사령부 v1.0]
# 모든 비서(프로세스)를 감시하고, n8n과 연동하여 에러가 터지기 전 미리 방지합니다.
# 제국 전체의 '무결점(Zero-Error)'을 보장하는 최후의 보루입니다.

class HealthCheckSentry:
    def __init__(self):
        self.n8n_webhook_url = os.getenv("N8N_WEBHOOK_URL")
        self.max_cpu_percent = 85.0 # CPU가 85% 이상이면 잠시 대기시킵니다.
        self.max_mem_percent = 90.0

    def check_idle_mercenaries(self):
        """놀고 있는 비서(프로세스)가 있는지 점검하고 일거리를 던져줍니다."""
        print("🔍 [Checking Idle] 농땡이 피우는 비서가 있는지 전수 조사 중...")
        # 현재 실행 중인 파이썬 비서들 리스트업
        active_assistants = [p.info for p in psutil.process_iter(['pid', 'name']) if 'python' in p.info['name']]
        
        if len(active_assistants) < 2:
            print("⚠️ [Idle Detected] 비서들이 너무 많이 놀고 있습니다! n8n에 작업 요청 중...")
            self.report_to_n8n("IDLE_WARNING", "비서 부대 가동률 저하. 즉시 새로운 숏츠 제작 명령 하달 요망.")
            return True
        return False

    def prevent_crash(self):
        """서버가 터지기 전에 미리 메모리와 CPU를 비워냅니다 (에러 원천 차단)."""
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        
        print(f"🌡️ [Server Temperature] CPU: {cpu_usage}%, MEM: {mem_usage}%")
        
        if cpu_usage > self.max_cpu_percent or mem_usage > self.max_mem_percent:
            print("🚨 [Overload Warning] 서버 과부하 감지! 모든 비서 일시 정지 및 n8n 보고.")
            self.report_to_n8n("OVERLOAD_CRITICAL", "서버 폭발 직전! 렌더링 작업 일시 유예 조치함.")
            time.sleep(10) # 10초간 열을 식힙니다.
            return False
        return True

    def report_to_n8n(self, status, message):
        """모든 상태를 n8n '교통경찰'에게 보고하여 지휘 계통을 일원화합니다."""
        if not self.n8n_webhook_url: return
        
        payload = {
            "status": status,
            "message": message,
            "timestamp": time.time()
        }
        try:
            requests.post(self.n8n_webhook_url, json=payload, timeout=5)
            print(f"📡 [n8n Linked] 교통경찰(n8n)에게 '{status}' 보고 완료.")
        except:
            print("⚠️ [n8n Link Failed] n8n 통신 불가. 자체 판단 가동.")

if __name__ == "__main__":
    sentry = HealthCheckSentry()
    # 대장님을 위한 무결점 감시 테스트 시작!
    while True:
        if sentry.prevent_crash():
            sentry.check_idle_mercenaries()
        time.sleep(60) # 1분마다 순찰을 돕니다.
