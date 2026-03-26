# 파일: create_ollama_shortcut.ps1
# -------------------------------------------------
# Ollama 실행 파일 위치 (install_ollama.ps1 에서 지정한 경로와 동일)
$ollamaExe = "$env:USERPROFILE\OneDrive\바탕 화면\Ollama\ollama.exe"

# 바탕 화면 경로 (OneDrive 바탕 화면)
$desktopPath = "$env:USERPROFILE\OneDrive\바탕 화면"

# 바로 가기 파일 전체 경로
$shortcutPath = Join-Path $desktopPath "Ollama.lnk"

# WScript.Shell COM 객체 사용해서 바로 가기 생성
$ws = New-Object -ComObject WScript.Shell
$shortcut = $ws.CreateShortcut($shortcutPath)

# 실행 파일 지정
$shortcut.TargetPath = $ollamaExe

# 아이콘도 실행 파일 자체 사용
$shortcut.IconLocation = $ollamaExe

# (선택) 바로 가기 실행 시 자동으로 serve 모드로 실행하고 싶다면:
# $shortcut.Arguments = "serve"

$shortcut.Description = "Ollama 로컬 LLM 실행기"
$shortcut.Save()

Write-Host "바탕 화면에 Ollama 바로 가기가 생성되었습니다: $shortcutPath"
