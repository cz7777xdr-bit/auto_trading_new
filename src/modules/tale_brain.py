import os
import requests
import json

# 📜 [안티그래비티 글로벌 전설 발굴 엔진 v1.0]
# 오픈라우터의 무료 클로드(Claude) 지능을 활용해 전 세계의 신비로운 이야기를 영상용 대본으로 변환합니다.

class TaleGenesisEngine:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        # 💡 대장님이 말씀하신 '가장 똑똑한 무료 지능' 사용 (Claude 또는 성능 좋은 무료 모델)
        self.brain_model = "anthropic/claude-3-haiku:free"
        
    def discover_rare_tale(self, region="Global"):
        """전 세계의 희귀하고 감동적인 전설을 발굴합니다."""
        prompt = f"""
        너는 전 세계의 신비로운 전설을 발굴하는 스토리텔러야. 
        '{region}' 지역의 잘 알려지지 않았지만 아주 흥미진진한 옛날 이야기를 하나 골라줘.
        조건:
        1. 숏츠 영상(60초 이내)용으로 각색할 것.
        2. 몰입감 있는 서술형 대본(Narration)을 작성할 것.
        3. 각 장면에 들어갈 이미지 생성용 프롬프트(DALL-E 스타일)도 3개 포함할 것.
        모든 답변은 한국어로 해줘.
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.brain_model,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            print(f"🧠 [Claude Brain] '{region}'의 전설을 발굴 중입니다 (무료 지능 가동)...")
            response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            tale_content = result['choices'][0]['message']['content']
            
            # 발굴된 전설을 문서화하여 저장
            save_path = f"src/intelligence/tales/tale_{region}_{os.urandom(4).hex()}.md"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(tale_content)
                
            print(f"✅ [Tale Found] 발굴 성공! 위치: {save_path}")
            return tale_content
        except Exception as e:
            print(f"⚠️ [Brain Error] 전설 발굴 실패: {e}")
            return None

if __name__ == "__main__":
    miner = TaleGenesisEngine()
    # 첫 번째 타겟: 신비로운 '북유럽'의 전설 사냥 시작!
    miner.discover_rare_tale("Nordic")
