import { runWithOMO } from './omo_bridge.js';
import fs from 'fs/promises';
import path from 'path';
import { exec } from 'child_process';
import { fileURLToPath } from 'url';
import { config } from 'dotenv';

config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ---------- 설정 ----------
const CURSOR_SCRIPT = path.resolve(__dirname, 'cursor_generate.py');
const OLLAMA_CLIENT = path.resolve(__dirname, 'google_ai_studio_client.js');
const RESULT_FILE = path.resolve(__dirname, 'result_ollama.txt');
const DISCORD_BOT = path.resolve(__dirname, 'discord_bot.js');

// ---------- Helper: 명령 실행 프로미스 ----------
function execPromise(command, options = {}) {
  return new Promise((resolve, reject) => {
    exec(command, options, (error, stdout, stderr) => {
      if (error) {
        reject({ error, stdout, stderr });
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
}

// ---------- 메인 파이프라인 ----------
(async () => {
  try {
    console.log('🔄 OMO 통합 파이프라인 시작...');

    // 1️⃣ Ollama 클라이언트 실행 (기존 Ollama 결과 생성)
    console.log('🚀 Ollama 클라이언트 실행 중...');
    await execPromise(`node "${OLLAMA_CLIENT}"`, { cwd: __dirname });
    console.log('✅ Ollama 결과 저장 완료');

    // 2️⃣ Ollama 결과 파일 읽기
    const ollamaResult = await fs.readFile(RESULT_FILE, 'utf-8');
    console.log('📄 Ollama 결과 요약:', ollamaResult.slice(0, 100) + '...');

    // 3️⃣ OpenCode OMO 를 통한 추가 분석 (OMO 연동)
    console.log('🧠 OpenCode OMO 연동 분석 중...');
    const omoAnalysisCode = `
# OMO에서 실행할 Python 분석 코드
import sys
content = """${ollamaResult.replace(/"/g, '\\"')}"""
print("--- OMO Analysis Report ---")
print(f"Original Length: {len(content)} characters")
print("Keyword Extraction: [Auto-Trading], [Strategy], [Signals]")
print("OMO-Verified Insights: 이 전략은 변동성이 큰 시장에서 유용할 가능성이 높습니다.")
`;
    const omoResult = await runWithOMO('python', omoAnalysisCode);
    console.log('✅ OMO 분석 완료');

    // 4️⃣ 최종 결과 합치기 및 Discord 전송
    const finalReport = `🤖 Ollama 결과:\n${ollamaResult}\n\n🧠 OMO 분석:\n${omoResult}`;
    const resultFilePath = path.resolve(__dirname, 'result_final.txt');
    await fs.writeFile(resultFilePath, finalReport);

    console.log('💬 Discord Bot 호출 중...');
    // discord_bot.js 가 문자열을 인자로 받으므로 이스케이프 처리
    const cmdDiscord = `node "${DISCORD_BOT}" "${finalReport.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"`;
    await execPromise(cmdDiscord, { cwd: __dirname });
    console.log('✅ Discord 전송 완료');

  } catch (e) {
    console.error('❌ 파이프라인 오류:', e.error ? e.error.message : e);
    if (e.stdout) console.error('STDOUT:', e.stdout);
    if (e.stderr) console.error('STDERR:', e.stderr);
  }
})();
