# Ollama 설치 스크립트 (Windows PowerShell)
# 이 스크립트는 Ollama 최신 버전을 다운로드하고 설치합니다.
# 관리자 권한으로 실행해야 합니다.

# 1. 최신 설치 파일 URL 가져오기 (공식 GitHub 릴리즈 페이지)
$releaseApi = "https://api.github.com/repos/jmorganca/ollama/releases/latest"
$releaseInfo = Invoke-RestMethod -Uri $releaseApi -Headers @{'User-Agent'='PowerShell'}
$asset = $releaseInfo.assets | Where-Object { $_.name -like '*-windows-amd64.zip' }
if (-not $asset) {
    Write-Error "Ollama Windows용 설치 파일을 찾을 수 없습니다."
    exit 1
}
$downloadUrl = $asset.browser_download_url
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$zipPath = "$env:TEMP\ollama_$timestamp.zip"
Write-Host "다운로드 중: $downloadUrl"
# 기존 파일이 있으면 삭제 (잠금 방지)
Remove-Item -Path $zipPath -Force -ErrorAction SilentlyContinue
# curl 사용하여 다운로드 (네트워크 문제 회피)
$curlCmd = "curl -L -o \"$zipPath\" \"$downloadUrl\""
Write-Host "curl 로 다운로드 중: $downloadUrl"
Invoke-Expression $curlCmd

# 2. 압축 해제 및 실행 파일 복사
$extractPath = "$env:TEMP\ollama_extracted"
if (Test-Path $extractPath) { Remove-Item -Recurse -Force $extractPath }
Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force

# Ollama 실행 파일 위치 (ollama.exe)
$exePath = Join-Path $extractPath "ollama.exe"
if (-not (Test-Path $exePath)) {
    Write-Error "ollama.exe 파일을 찾을 수 없습니다."
    exit 1
}

# 3. 설치 디렉터리 확인 및 PATH 중복 체크
$installDir = "$env:USERPROFILE\OneDrive\바탕 화면\Ollama"
if (-not (Test-Path $installDir)) { 
    New-Item -ItemType Directory -Path $installDir -Force 
}
Copy-Item -Path $exePath -Destination $installDir -Force

# PATH에 중복 추가되지 않도록 체크 로직 적용
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$installDir*") {
    $newPath = $currentPath + ";$installDir"
    [System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    # 현재 세션 PATH에도 추가
    $env:Path += ";$installDir"
    Write-Host "PATH에 Ollama 경로를 추가했습니다." -ForegroundColor Green
} else {
    Write-Host "PATH에 이미 Ollama 경로가 존재합니다 (중복 제거)." -ForegroundColor Cyan
}

Write-Host "Ollama가 $installDir 에 설치되었습니다."
Write-Host "설치 확인: ollama --version"

# 4. 설치 완료 후 정리
Remove-Item -Path $zipPath -Force
Remove-Item -Recurse -Force $extractPath

# 5. Ollama 서비스 시작 (옵션)
# Start-Process -FilePath "$installDir\ollama.exe" -ArgumentList "serve" -NoNewWindow -PassThru

Write-Host "설치가 완료되었습니다. PowerShell을 재시작하거나 새 터미널을 열어 ollama 명령을 사용할 수 있습니다."
# 바탕 화면에 Ollama 바로 가기 생성
Write-Host "바탕 화면에 Ollama 바로 가기 생성 중..."
& "$PSScriptRoot\create_ollama_shortcut.ps1"
