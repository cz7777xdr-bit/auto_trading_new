// Ollama 기반 로컬 LLM 호출 스크립트 (google_ai_studio_client.js 대체)

require('dotenv').config(); // .env 로드 (필요 시)
const fs = require('fs').promises;
const path = require('path');
// using global fetch (Node >=18 provides fetch)

// ---------- 설정 ----------
const GENERATED_CODE_PATH = path.resolve(__dirname, 'generated_code.js'); // Cursor 가 만든 코드 파일
const RESULT_PATH = path.resolve(__dirname, 'result_ollama.txt'); // 결과 저장 파일

const OLLAMA_HOST = process.env.OLLAMA_HOST || 'http://127.0.0.1:11434';
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || 'codegemma'; // 코드 실행에 최적화된 모델

// ---------- Ollama 요청 함수 ----------
async function callOllama(prompt) {
  const url = `${OLLAMA_HOST}/api/generate`;
  const body = {
    model: OLLAMA_MODEL,
    prompt: prompt,
    stream: false,
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`Ollama API 오류: ${response.status} ${response.statusText}\n${errText}`);
  }

  const data = await response.json();
  return data.response; // 순수 텍스트 결과 반환
}

// ---------- 메인 로직 ----------
(async () => {
  try {
    // 1️⃣ Cursor 가 만든 코드를 읽는다
    const code = await fs.readFile(GENERATED_CODE_PATH, 'utf-8');
    console.log(`✅ ${path.basename(GENERATED_CODE_PATH)} 로부터 코드 로드 완료`);

    // 2️⃣ Ollama 에 전달할 프롬프트 구성
    const prompt = `아래 JavaScript 코드를 Node.js 환경에서 실행하고, console.log 로 출력된 내용을 그대로 반환해줘.\n코드:\n\`\`\`js\n${code}\n\`\`\``;

    console.log('🔄 Ollama 로 코드 실행 요청 중...');
    const ollamaResult = await callOllama(prompt);
    console.log('✅ Ollama 로부터 응답 수신');

    // 3️⃣ 결과를 파일에 저장
    await fs.writeFile(RESULT_PATH, ollamaResult, 'utf-8');
    console.log(`🗒️ 결과가 ${path.basename(RESULT_PATH)} 에 저장되었습니다.`);
  } catch (err) {
    console.error('❌ 오류 발생:', err.message);
    await fs.writeFile(RESULT_PATH, `Error: ${err.stack}`, 'utf-8');
  }
})();
