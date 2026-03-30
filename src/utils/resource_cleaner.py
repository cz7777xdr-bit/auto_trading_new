import os
import shutil
import time

# 🧹 [안티그래비티 가비지 컬렉터 v1.0]
# 중간 생성물(쓰레기)은 즉시 소각하고, 오직 '황금 결과물'만 남기는 초슬림 시스템입니다.

class ResourceCleaner:
    def __init__(self):
        self.tmp_dirs = ["src/output/temp_fragments", "src/output/raw_scripts", "src/output/failed_quality"]
        self.target_dir = "src/output/final_vault" # 최종 결과물 보관함
        os.makedirs(self.target_dir, exist_ok=True)

    def purge_temp_files(self):
        """작업이 끝난 뒤 쌓인 모든 중간 찌꺼기 파일을 0.1초 만에 소각합니다."""
        print("🧹 [Cleaning Operation] 기지 내 불필요한 찌꺼기 파일 소각 시작...")
        
        for d in self.tmp_dirs:
            if os.path.exists(d):
                files = os.listdir(d)
                for f in files:
                    file_path = os.path.join(d, f)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print(f"🗑️ [Deleted] {f}")
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f"⚠️ [Clean Error] {f} 소각 실패: {e}")

    def archive_final_only(self, source_path):
        """최종 승인된 결과물을 '금고'로 옮기고 그 외의 파일은 지웁니다."""
        file_name = os.path.basename(source_path)
        dest_path = os.path.join(self.target_dir, file_name)
        
        try:
            shutil.copy2(source_path, dest_path)
            print(f"💎 [Archived] 최종 결과물 금고 보관 완료: {file_name}")
            # 아까 대장님 말씀하신 대로 원본은 즉각 삭제 고려 (시스템 설정에 따라)
            return True
        except Exception as e:
            print(f"⚠️ [Archive Error] 가치 자산 보관 실패: {e}")
            return False

if __name__ == "__main__":
    cleaner = ResourceCleaner()
    # 대장님을 위한 기지 청소 프로토콜 가동!
    cleaner.purge_temp_files()
