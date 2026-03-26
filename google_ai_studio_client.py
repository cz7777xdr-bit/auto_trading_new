# -*- coding: utf-8 -*-
"""
Google AI Studio(Gemini) API를 호출해 Cursor가 만든 코드를 실행하고 결과를 저장하는 스크립트

필수 패키지:
  - google-cloud-aiplatform
  - python-dotenv

.env 파일에 아래 변수들을 정의해 주세요.
  GOOGLE_APPLICATION_CREDENTIALS=./service_account.json   # 서비스 계정 JSON 경로
  PROJECT_ID=your-gcp-project-id
  REGION=us-central1
  MODEL_ID=gemini-1.5-pro   # 사용하고 싶은 Gemini 모델 ID
"""

import os
import json
from google.cloud import aiplatform
from dotenv import load_dotenv

# .env 로드
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
MODEL_ID = os.getenv("MODEL_ID")

if not all([PROJECT_ID, REGION, MODEL_ID]):
    raise EnvironmentError("PROJECT_ID, REGION, MODEL_ID 환경 변수가 설정되지 않았습니다.")


def init_model():
    """Vertex AI 모델 초기화"""
    aiplatform.init(project=PROJECT_ID, location=REGION)
    return aiplatform.Model(model_name=MODEL_ID)


def generate_content(prompt: str) -> str:
    """Gemini 모델에 프롬프트 전송하고 응답 문자열 반환"""
    model = init_model()
    response = model.predict(
        instances=[{"content": prompt}],
        parameters={"temperature": 0.2, "max_output_tokens": 2048},
    )
    # 응답 구조는 모델에 따라 다를 수 있음. 여기서는 가장 일반적인 형태를 가정.
    try:
        return response.predictions[0]["content"]
    except Exception as e:
        return f"[ERROR] 응답 파싱 실패: {e}\n전체 응답: {response}"


def main():
    # 실행할 파이썬 파일 경로 (Cursor가 만든 파일)
    code_path = os.path.abspath("my_module.py")
    if not os.path.isfile(code_path):
        print(f"[WARN] {code_path} 파일이 존재하지 않습니다. 먼저 cursor_generate.py 로 코드를 저장하세요.")
        return

    with open(code_path, "r", encoding="utf-8") as f:
        code = f.read()

    # Gemini에 전달할 프롬프트 구성
    prompt = f"""아래 파이썬 코드를 실행하고, 표준 출력과 에러 메시지를 반환해 주세요.
```python
{code}
```"""

    print("[INFO] Gemini에 코드 실행 요청 중...")
    result = generate_content(prompt)

    # 결과 저장
    out_path = os.path.abspath("result.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"[INFO] 실행 결과가 {out_path} 에 저장되었습니다.")

if __name__ == "__main__":
    main()
