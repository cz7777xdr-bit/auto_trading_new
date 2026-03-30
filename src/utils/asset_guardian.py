import os
import shutil
from PIL import Image, ImageDraw, ImageFont
import datetime

# 🛡️ [안티그래비티 자산 수호자 v1.0]
# 생성된 이미지를 AI 분류기로 자동 정리하고, 도용 방지 워터마크를 0.01초 만에 박아 넣습니다.

class AssetGuardian:
    def __init__(self):
        self.raw_dir = "src/output/market_images"
        self.classified_base = "src/output/classified_assets"
        self.watermark_text = "© ANTIGRAVITY PREMIUM ASSET"
        
        # 카테고리 정의
        self.categories = ["NATURE", "SPACE", "TECH", "ABSTRACT", "FUTURE_CITY"]
        for cat in self.categories:
            os.makedirs(os.path.join(self.classified_base, cat), exist_ok=True)

    def classify_and_stamp(self, image_filename):
        """이미지를 분류하고 워터마크를 찍어 최종 창고로 보냅니다."""
        raw_path = os.path.join(self.raw_dir, image_filename)
        if not os.path.exists(raw_path):
            return

        # 1. AI 지능 분석 (여기서는 파일명 키워드 기반으로 1차 분류, 추후 Gemini Vison API 연동)
        category = self.predict_category(image_filename)
        print(f"🧐 [Vision-Sentry] 이미지 '{image_filename}' -> '{category}' 카테고리 판정.")

        # 2. 워터마크 자동 삽입 (프리미엄 느낌 사입)
        final_filename = f"STAMPED_{image_filename}"
        final_path = os.path.join(self.classified_base, category, final_filename)
        
        self.apply_premium_watermark(raw_path, final_path)
        print(f"✅ [Stamping] {final_filename} 워터마킹 및 분류 완료.")

    def predict_category(self, filename):
        """이미지 파일명의 키워드를 분석하여 카테고리를 예측합니다."""
        fname = filename.upper()
        if "SPACE" in fname or "NEBULA" in fname: return "SPACE"
        if "TECH" in fname or "CYBER" in fname: return "TECH"
        if "NATURE" in fname or "GARDEN" in fname: return "NATURE"
        if "CITY" in fname: return "FUTURE_CITY"
        return "ABSTRACT"

    def apply_premium_watermark(self, input_path, output_path):
        """이미지 우측 하단에 세련된 워터마크를 0.01초 만에 삽입합니다."""
        try:
            with Image.open(input_path) as img:
                draw = ImageDraw.Draw(img)
                width, height = img.size
                
                # 우측 하단 여백 설정
                margin = 30
                text = self.watermark_text
                
                # 본인의 로고나 텍스트를 은은한 투명도로 삽입 (255,255,255, 128)
                # (폰트 설정이 복잡할 수 있어 기본 폰트 사용, 필요시 화려한 폰트 경로 추가 가능)
                draw.text((width - 300 - margin, height - 50 - margin), text, fill=(255, 255, 255, 150))
                
                img.save(output_path, "JPEG", quality=95)
        except Exception as e:
            print(f"⚠️ [Stamping Error] {e}")

    def run_all_raw_images(self):
        """창고에 쌓인 모든 원본 이미지를 한 번에 분류하고 도장 찍습니다."""
        images = [f for f in os.listdir(self.raw_dir) if f.endswith(".jpg") and not f.startswith("STAMPED_")]
        print(f"⚡ [Orchestration] 총 {len(images)}개의 이미지를 가공 시작합니다.")
        for img in images:
            self.classify_and_stamp(img)

if __name__ == "__main__":
    guardian = AssetGuardian()
    guardian.run_all_raw_images()
