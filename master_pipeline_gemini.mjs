// master_pipeline_gemini.mjs – [검색 -> 저장 -> Gemini 분석 -> Discord 전송] 통합 파이프라인
import { searchWeb } from './brave_search.mjs';
import { saveResults, getRecentResults } from './db_manager.mjs';
import { askGemini } from './gemini_bridge.mjs';
import { runWithOMO } from './omo_bridge.mjs';
import { config } from 'dotenv';
import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DEFAULT_QUERY = process.env.DEFAULT_QUERY || '주식 자동매매 최신 트렌드';
const DISCORD_BOT = path.resolve(__dirname, 'discord_bot.js');

async function runMasterPipeline() {
  console.log('🚀 [마스터 파이프라인] 전체 분석 시작...');
  
  try {
    // 1️⃣ 웹 검색 (Brave Search)
    console.log(`🔎 "${DEFAULT_QUERY}" 에 대해 웹 검색 중...`);
    const searchData = await searchWeb(DEFAULT_QUERY, 5);
    console.log(`✅ ${searchData.length}개의 웹 검색 결과를 가져왔습니다.`);

    // 2️⃣ 데이터베이스 저장 (SQLite)
    await saveResults(DEFAULT_QUERY, searchData);
    console.log('✅ 검색 결과를 SQLite(search_results.db)에 저장했습니다.');

    // 3️⃣ Gemini 서버분석 (Google AI Studio)
    console.log('🚀 Gemini를 통한 심층 분석 중...');
    const searchContext = searchData.map(res => `- ${res.title}\n  (URL: ${res.url})\n  (Snippet: ${res.snippet})`).join('\n\n');
    const geminiPrompt = `아래의 웹 검색 결과를 요약하고 인공지능 주식 비서로서의 전략적 인사이트를 제시해줘:\n\n${searchContext}`;
    const analysisResult = await askGemini(geminiPrompt);
    console.log('✅ Gemini 분석 완료');

    // 4️⃣ OMO 추가 분석 (선택사항)
    let omoResult = '';
    if (process.env.OMO_TOKEN && process.env.OMO_TOKEN !== 'YOUR_OMO_API_TOKEN') {
        console.log('🧠 OMO 추가 심층 분석 중...');
        omoResult = await runWithOMO('python', `print("OMO Depth Analysis: ${DEFAULT_QUERY}")\nprint("""${analysisResult.replace(/"/g, '\\"')}""")`);
        console.log('✅ OMO 분석 완료');
    }

    // 5️⃣ 최종 리포트 및 Discord 전송
    const finalReport = `💎 [Gemini 전략 리포트]\n\n🔍 검색어: ${DEFAULT_QUERY}\n\n🤖 분석 결과:\n${analysisResult}\n\n${omoResult ? '🧠 OMO 분석:\n' + omoResult : ''}`;
    
    console.log('💬 Discord Bot 알림 전송 중...');
    const cmdDiscord = `node "${DISCORD_BOT}" "${finalReport.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"`;
    
    exec(cmdDiscord, (err, stdout, stderr) => {
        if (err) {
            console.error('❌ Discord 전송 실패:', err.message);
        } else {
            console.log('✅ Discord 알림 전송 완료!');
        }
    });

  } catch (err) {
    console.error('❌ 파이프라인 실행 중 오류:', err.message);
  }
}

// 직접 실행 시
runMasterPipeline();
