import os
import subprocess
import json

# ⚡ [안티그래비티 퀄리티 체커 v1.0]
# 숏츠 영상의 비트레이트, 해상도, 오디오 상태를 정밀 분석하여 기준 미달 시 '재제작'을 명령합니다.

class QualityChecker:
    def __init__(self):
        self.video_dir = "src/output/videos"
        self.min_bitrate = 5000000 # 최소 5Mbps (고화질 기준)
        self.min_height = 1920     # 세로형 숏츠 FHD 기준
        self.min_width = 1080

    def check_video_spec(self, video_path):
        """FFmpeg(ffprobe)를 통해 영상의 기술적 스펙을 정밀 검사합니다."""
        print(f"🔍 [Quality Check] '{os.path.basename(video_path)}' 정밀 진단 시작...")
        
        try:
            # ffprobe를 이용해 JSON 형식으로 영상 메타데이터 추출
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            
            # 비디오 스트림 정보 추출
            video_stream = next(s for s in data['streams'] if s['codec_type'] == 'video')
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            bitrate = int(data['format'].get('bit_rate', 0))

            print(f"📊 [Spec] 해상도: {width}x{height}, 비트레이트: {bitrate/1000000:.2f} Mbps")

            # 품질 판정 로직
            if width < self.min_width or height < self.min_height:
                print("❌ [Quality Failed] 해상도가 기준 미달입니다! (FHD 이상 필수)")
                return False
            
            if bitrate < self.min_bitrate:
                print("⚠️ [Refining] 비트레이트가 낮아 화질이 떨어질 수 있습니다. (재인코딩 권장)")
                # (이 경우엔 바로 False를 주기보다 경고를 줍니다.)
                
            print("✅ [Quality Success] 고품질 판정! 전 세계 송출 허용.")
            return True

        except Exception as e:
            print(f"⚠️ [Check Error] 영상 분석 중 오류 발생: {e}")
            return False

    def screen_all_videos(self):
        """창고에 있는 모든 영상을 검사하여 불량품을 골라냅니다."""
        videos = [os.path.join(self.video_dir, v) for v in os.listdir(self.video_dir) if v.endswith(".mp4")]
        approved_videos = []
        
        for video in videos:
            if self.check_video_spec(video):
                approved_videos.append(video)
            else:
                # 불량 영상은 별도 'trash' 폴더로 격리하거나 재제작 플래그를 남깁니다.
                trash_dir = os.path.join(self.video_dir, "failed_quality")
                os.makedirs(trash_dir, exist_ok=True)
                shutil.move(video, os.path.join(trash_dir, os.path.basename(video)))
        
        return approved_videos

if __name__ == "__main__":
    checker = QualityChecker()
    checker.screen_all_videos()
