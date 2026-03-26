// pipeline_gemini.js – Google AI Studio (Gemini) 기반 통합 파이프라인
import { askGemini } from './gemini_bridge.mjs';
import { runWithOMO } from './omo_bridge.mjs';
import fs from 'fs/promises';
import path from 'path';
import { exec } from 'child_process';
import { fileURLToPath } from 'url';
import { config } from 'dotenv';

config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ---------- 설정 ----------
const GENERATED_CODE_PATH = path.resolve(__dirname, 'generated_code.js');
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
    console.log('🔄 Gemini 통합 파이프라인 시작...');

    // 1️⃣ 생성된 코드 읽기
    const code = await fs.readFile(GENERATED_CODE_PATH, 'utf-8');
    console.log(`✅ ${path.basename(GENERATED_CODE_PATH)} 로부터 코드 로드 완료`);

    // 2️⃣ Gemini (AI Studio) 로 분석
    console.log('🚀 Gemini 로 분석 중 (Google AI Studio)...');
    const geminiPrompt = `아래 JavaScript 코드를 분석하고 결과를 한국어로 알려줘:\n\n\`\`\`js\n${code}\n\`\`\``;
    const geminiResult = await askGemini(geminiPrompt);
    console.log('✅ Gemini 분석 완료');

    // 3️⃣ OpenCode OMO 로 분석 검증 (OMO 연동)
    let omoResult = 'OMO 분석 스킵됨 (설정 필요)';
    if (process.env.OMO_TOKEN && process.env.OMO_TOKEN !== 'YOUR_OMO_API_TOKEN') {
      try {
        console.log('🧠 OMO 로 추가 심층 분석 중...');
        const omoCode = `
import sys
content = """${geminiResult.replace(/"/g, '\\"')}"""
print("--- OMO Depth Analysis ---")
print(content)
print("--------------------------")
`;
        omoResult = await runWithOMO('python', omoCode);
        console.log('✅ OMO 분석 완료');
      } catch (err) {
        console.warn('⚠️ OMO 호출 실패:', err.message);
      }
    } else {
      console.log('ℹ️ OMO_TOKEN이 설정되지 않아 클라우드 심층 분석을 건너뜁니다.');
    }

    // 4️⃣ 최종 리포트 및 Discord 전송
    const finalReport = `💎 Gemini 결과:\n${geminiResult}\n\n🧠 OMO 분석:\n${omoResult}`;
    const resultFilePath = path.resolve(__dirname, 'result_final_gemini.txt');
    await fs.writeFile(resultFilePath, finalReport);

    console.log('💬 Discord Bot 호출 중...');
    const cmdDiscord = `node "${DISCORD_BOT}" "${finalReport.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"`;
    await execPromise(cmdDiscord, { cwd: __dirname });
    console.log('✅ Discord 전송 완료');

  } catch (e) {
    console.error('❌ Gemini 파이프라인 오류:', e.message);
  }
})();
