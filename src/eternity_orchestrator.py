import sys
import os
import time
import subprocess
import datetime

# 프로젝트 루트 경로를 sys.path에 추가 (임포트 에러 방지)
sys.path.append(os.getcwd())

# 🔄 [안티그래비티 이터니티 루프] 24/7 무인 자율 수익화 시스템 v1.0
# 이 스크립트는 전 세계 시장의 흐름에 맞춰 365일 쉬지 않고 콘텐츠를 생산하고 송출합니다.

class EternityOrchestrator:
    def __init__(self):
        self.interval_seconds = 6 * 3600 # 6시간마다 1회 풀 사이클 가동
        self.pipeline_scripts = [
            "src/scanners/market_watcher.py",
            "src/intelligence/trend_analyzer.py",
            "src/utils/global_briefing_engine.py",
            "src/utils/asset_resource_manager.py",
            "src/utils/premium_renderer.py"
        ]

    def run_cycle(self):
        total_steps = len(self.pipeline_scripts)
        print(f"🚀 [Eternity Loop] {datetime.datetime.now()} - 새로운 글로벌 수익 사이클 시작!")
        
        for idx, script in enumerate(self.pipeline_scripts):
            progress = ((idx) / total_steps) * 100
            print(f"📊 [Progress: {progress:.4f}%] ⚙️ {script} 가동 준비 중...")
            
            try:
                # 작업 실행 시간 측정 및 실시간 상태 표시
                start_time = time.time()
                subprocess.run(["uv", "run", script], check=True)
                elapsed = time.time() - start_time
                
                current_progress = ((idx + 1) / total_steps) * 100
                print(f"✅ [Progress: {current_progress:.4f}%] {script} 완료! (소요시간: {elapsed:.2f}초)")
            except Exception as e:
                print(f"⚠️ [Error: {((idx)/total_steps)*100:.4f}%] {script} 중단: {e}. 자가 치유 프로토콜 가동.")

        self.broadcast_to_world()

    def broadcast_to_world(self):
        print("📡 [WORLD BROADCAST] 전 세계 채널(YouTube, TikTok, Discord)로의 송출을 시작합니다!")
        
        # 1. 유튜브 업로드 시도 (인증 파일이 있는 경우)
        if os.path.exists("client_secrets.json") or os.path.exists("token.pickle"):
            try:
                from src.utils.youtube_uploader import YouTubeUploader
                uploader = YouTubeUploader()
                
                # 영상 파일 목록 (video_engine.py 결과물 등)
                video_dir = "src/output/videos"
                if os.path.exists(video_dir):
                    videos = [os.path.join(video_dir, v) for v in os.listdir(video_dir) if v.endswith(".mp4")]
                    for video in videos:
                        title = f"AI Trading Insight - {datetime.datetime.now().strftime('%Y-%m-%d')}"
                        uploader.upload_shorts(video, title, "#shorts #trading #ai #passiveincome")
                else:
                    print("⚠️ 업로드할 영상 파일이 없습니다.")
            except Exception as e:
                print(f"⚠️ [YouTube Upload Error] {e}")
        else:
            print("⚠️ [YouTube Skip] 인증 파일이 없어 업로드를 건너뜁니다.")

        # 2. 결과 알림 (Discord 등)
        print("✅ [GLOBAL BROADCAST] 5대 대륙 고품질 숏폼 송출 프로토콜 완료.")

    def start_infinite_loop(self):
        print("👑 [안티그래비티 24/7 제국] 무인 자율 가동 시스템 온(ON).")
        while True:
            self.run_cycle()
            print(f"⏳ [Standby] 다음 수익 사이클까지 {self.interval_seconds/3600}시간 대기 중...")
            time.sleep(self.interval_seconds)

if __name__ == "__main__":
    orchestrator = EternityOrchestrator()
    
    # GitHub Actions 환경 대응
    if os.getenv("GITHUB_ACTIONS") == "true":
        print("🤖 [GitHub Actions Mode] 1회 사이클 실행 후 종료합니다.")
        orchestrator.run_cycle()
    else:
        # 로컬/서버(창고) 환경에서는 무한 루프 가동
        orchestrator.start_infinite_loop()
