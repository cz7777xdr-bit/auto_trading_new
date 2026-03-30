import os
import requests
import json
import random

# 🧠 [안티그래비티 멀티모달 초지능 센터 v1.0]
# 오픈라우터의 4가지 최정예 무료 모델을 [사령/병렬/보충/예비] 체계로 운영합니다.

class MultiModalBrain:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # 🛡️ 안티그래비티 지능 부대 편성 (OpenRouter FREE 모델 리스트)
        self.models = {
            "COMMANDER": "anthropic/claude-3-haiku:free",  # 1. 사령관 (Claude)
            "ADVISOR": "google/gemma-2-9b-it:free",        # 2. 병렬 (Gemma-2)
            "INSPECTOR": "meta-llama/llama-3-8b-instruct:free", # 3. 보충 (Llama-3)
            "RESERVE": "qwen/qwen-2-7b-instruct:free"       # 4. 예비 (Qwen-2)
        }

    def call_brain(self, prompt, role="COMMANDER"):
        """지정된 역할의 지능에게 명령을 내립니다."""
        target_model = self.models.get(role, self.models["COMMANDER"])
        
        print(f"📡 [Brain Link] '{role}'({target_model})에게 지능 전송 중...")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": target_model,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"⚠️ [Brain Fault] {role} 먹통! 즉시 'RESERVE' 예비군 투입.")
            return self.call_brain(prompt, role="RESERVE")

    def complex_thinking(self, task_prompt):
        """병렬/보충 지능을 모아 '교차 검토'를 수행합니다 (Ultimate Quality)."""
        print(f"🔥 [Complex Thinking] 멀티 지능 오케스트레이션 가동!")
        
        # 1. 사령관이 초안 작성
        draft = self.call_brain(task_prompt, "COMMANDER")
        
        # 2. 보충 관제사가 품질 검사 및 보강
        review_prompt = f"다음 대본의 품질을 검사하고 더 재미있게 수정해줘: {draft}"
        final_result = self.call_brain(review_prompt, "INSPECTOR")
        
        return final_result

if __name__ == "__main__":
    brain = MultiModalBrain()
    # 대장님을 위한 멀티 지능 테스트: "전 세계에서 가장 돈이 되는 전설 테마는?"
    result = brain.complex_thinking("숏츠로 만들었을 때 수익이 가장 잘 날 것 같은 전설 테마 3개를 추천해줘.")
    print(f"🏆 [Final Intelligence Outcome]:\n{result}")
