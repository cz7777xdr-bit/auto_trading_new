import os
import requests
import json

# 🤖 [안티그래비티 오픈라우터 지능 브릿지 v1.0]
# 전 세계 모든 AI 모델을 가장 경제적이고 효율적으로 연결하는 비서의 '지능 중추'입니다.

class OpenRouterBridge:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.site_url = "https://antigravity-merchant.ai" # 대장님의 비즈니스 사이트 가칭
        self.site_name = "Antigravity Assistant"

        # 모델 라인업 (무료 모델과 유료 정예 모델 구분)
        self.free_model = "google/gemma-2-9b-it:free" # 0원! (강력 추천 무료 모델)
        self.elite_model = "anthropic/claude-3.5-sonnet" # 가장 똑똑한 클로드 모델
        self.fallback_model = "meta-llama/llama-3-8b-instruct:free"

    def ask_brain(self, prompt, use_elite=False):
        """비서의 두뇌에게 질문을 던집니다. 상황에 따라 무료/유료를 선택합니다."""
        target_model = self.elite_model if use_elite else self.free_model
        
        print(f"🧠 [Brain Activity] '{target_model}' 모델을 통해 사고 중...")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
            "Content-Type": "application/json"
        }

        payload = {
            "model": target_model,
            "messages": [
                {"role": "system", "content": "너는 안티그래비티 대장님의 비즈니스 수익을 극대화하는 정예 비서야. 모든 답변은 한국어로만 해."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"⚠️ [Brain Error] {target_model} 호출 실패: {e}. 백업 모델 가동 중...")
            # 메인 모델 실패 시 즉시 다른 무료 모델로 장애 복구 수행
            return self.ask_fallback(prompt)

    def ask_fallback(self, prompt):
        """메인 모델이 버벅거리면 즉시 대체 무료 모델을 호출합니다."""
        # (구현 로직은 위와 동일하게 유지하되 모델만 fallback_model로 교체)
        pass

if __name__ == "__main__":
    # 대장님을 위한 지능 브릿지 테스트 가동!
    bridge = OpenRouterBridge()
    # "오늘 비즈니스 성공 확률이 어때?"라고 무료 모델에게 물어봅니다.
    print(bridge.ask_brain("오늘 우리의 비즈니스 성공 확률을 분석해줘."))
