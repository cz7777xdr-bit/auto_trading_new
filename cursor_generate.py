# -*- coding: utf-8 -*-
"""
Cursor가 생성한 코드를 지정된 파일에 저장하는 헬퍼 스크립트
사용법: python cursor_generate.py <파일명> <코드 문자열>
예시: python cursor_generate.py my_module.py "def hello():\n    print('안녕')"
"""

import sys
import os

def main():
    if len(sys.argv) != 3:
        print("Usage: python cursor_generate.py <filename> <code>")
        sys.exit(1)

    filename, code = sys.argv[1], sys.argv[2]
    out_path = os.path.abspath(os.path.join(os.getcwd(), filename))

    # 파일이 이미 존재하면 덮어쓰기 전 확인 (필요 시 수정)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"[INFO] 코드가 저장되었습니다: {out_path}")

if __name__ == "__main__":
    main()
