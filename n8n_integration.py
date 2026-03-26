# 파일: n8n_integration.py
# ------------------------------------------------- [n8n <-> Python 연동 스크립트]
import requests
import json
import os

def load_env_file(filepath=".env"):
    """매우 간단하게 .env 파일을 읽어 환경 변수로 설정합니다."""
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

# 설정 로딩
load_env_file()

# n8n 접속 정보 (환경 변수에서 가져오기)
N8N_BASE_URL = os.getenv("N8N_BASE_URL", "http://localhost:5678/api/v1")
N8N_API_KEY = os.getenv("N8N_API_KEY")

if not N8N_API_KEY:
    print("❌ 경고: N8N_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

headers = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}

def get_all_workflows():
    """모든 n8n 워크플로우 리스트를 가져옵니다."""
    url = f"{N8N_BASE_URL}/workflows"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        workflows = response.json().get('data', [])
        print(f"✅ 총 {len(workflows)}개의 워크플로우를 찾았습니다.")
        return workflows
    except Exception as e:
        print(f"❌ 워크플로우 조회 중 오류 발생: {e}")
        return []

def get_workflow_executions(workflow_id):
    """특정 워크플로우의 실행 결과(Executions)를 가져옵니다."""
    url = f"{N8N_BASE_URL}/executions?workflowId={workflow_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        executions = response.json().get('data', [])
        print(f"📈 워크플로우 ID {workflow_id}의 실행 기록을 {len(executions)}개 찾았습니다.")
        return executions
    except Exception as e:
        print(f"❌ 실행 상태 조회 중 오류 발생: {e}")
        return []

# ----------------- [메인 실행부 예시] -----------------
if __name__ == "__main__":
    print("--- n8n 작업 상태 수집 시작 ---")
    workflows = get_all_workflows()
    if workflows:
        for wf in workflows:
            status = '활성' if wf.get('active', False) else '비활성'
            print(f"- [ID: {wf['id']}] 이름: {wf['name']} (상태: {status})")
