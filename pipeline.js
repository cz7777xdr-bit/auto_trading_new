// pipeline.js – Cursor 출력 → Ollama 실행 → Discord 전송 파이프라인

require('dotenv').config(); // .env 로드
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs').promises;

// ---------- 설정 ----------
const CURSOR_SCRIPT = path.resolve(__dirname, 'cursor_generate.py'); // Python 헬퍼
const OLLAMA_CLIENT = path.resolve(__dirname, 'google_ai_studio_client.js'); // Ollama 호출 스크립트
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
    // 1️⃣ Cursor 로부터 받은 코드 (여기에 실제 코드 문자열을 넣으세요)
    const cursorCode = `// 여기서 Cursor 가 생성한 JavaScript 코드를 넣으세요\nconsole.log('Cursor 로부터 받은 코드 실행');`;
    const targetFile = 'generated_code.js';

    // 2️⃣ Python 스크립트 호출 → 파일 저장
    const cmdGenerate = `python "${CURSOR_SCRIPT}" ${targetFile} "${cursorCode.replace(/"/g, '\\"')}"`;
    console.log('🔧 cursor_generate.py 실행 중...');
    await execPromise(cmdGenerate, { cwd: __dirname });
    console.log('✅ 코드 파일 생성 완료');

    // 3️⃣ Ollama 클라이언트 실행 → result_ollama.txt 생성
    console.log('🚀 Ollama 클라이언트 실행 중...');
    await execPromise(`node "${OLLAMA_CLIENT}"`, { cwd: __dirname });
    console.log('✅ Ollama 결과 저장 완료');

    // 4️⃣ 결과 파일 읽기
    const result = await fs.readFile(RESULT_FILE, 'utf-8');
    console.log('📄 Ollama 결과:', result.trim());

    // 5️⃣ Discord Bot 실행 (result 를 인자로 전달)
    const cmdDiscord = `node "${DISCORD_BOT}" "${result.replace(/"/g, '\\"')}"`;
    console.log('💬 Discord Bot 호출 중...');
    await execPromise(cmdDiscord, { cwd: __dirname });
    console.log('✅ Discord 로 메시지 전송 완료');
  } catch (e) {
    console.error('❌ 파이프라인 오류:', e.error ? e.error.message : e);
    console.error('STDOUT:', e.stdout);
    console.error('STDERR:', e.stderr);
  }
})();
