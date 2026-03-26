// quota_checker.mjs – Gemini API 할당량 회복 자동 확인 및 파이프라인 트리거
import { askGemini } from './gemini_bridge.mjs';
import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const RETRY_INTERVAL = 30000; // 30초마다 확인
const PIPELINE_SCRIPT = 'master_pipeline_gemini.mjs';

async function checkAndRun() {
    console.log(`\n🔍 [${new Date().toLocaleTimeString()}] Gemini 할당량 회복 확인 중...`);

    try {
        // 아주 가벼운 테스트 프롬프트를 보내 할당량 확인
        const testResponse = await askGemini('Quota check. Reply with "OK".');
        
        if (testResponse && testResponse.includes('OK')) {
            console.log('✅ [성공] 할당량이 회복되었습니다! 파이프라인을 실행합니다.');
            triggerPipeline();
        } else {
            console.log('⚠️ [대기] API는 응답하나 할당량 상태가 불확실합니다. 30초 후 재시도합니다.');
            setTimeout(checkAndRun, RETRY_INTERVAL);
        }
    } catch (err) {
        if (err.message.includes('quota') || err.message.includes('429')) {
            console.log(`⏳ [대기] 여전히 할당량 초과 상태입니다. (에러: ${err.message.slice(0, 50)}...)`);
            console.log(`📅 30초 후에 다시 시도하겠습니다.`);
            setTimeout(checkAndRun, RETRY_INTERVAL);
        } else {
            console.error('❌ [오류] 알 수 없는 API 오류 발생:', err.message);
            console.log('30초 후 재시도하겠습니다.');
            setTimeout(checkAndRun, RETRY_INTERVAL);
        }
    }
}

function triggerPipeline() {
    console.log('🚀 파이프라인(pipeline_gemini.mjs) 실행 시작...');
    
    const child = exec(`node "${path.resolve(__dirname, PIPELINE_SCRIPT)}"`, (err, stdout, stderr) => {
        if (err) {
            console.error('❌ 파이프라인 실행 중 오류 발생:', err.message);
            return;
        }
        console.log('✅ 파이프라인 실행 완료!');
        if (stdout) console.log('STDOUT:\n', stdout);
        if (stderr) console.log('STDERR:\n', stderr);
        
        console.log('\n✨ 할당량 회복 및 작업 처리가 완료되었습니다. 종료합니다.');
        process.exit(0);
    });

    child.stdout.on('data', (data) => process.stdout.write(data));
    child.stderr.on('data', (data) => process.stderr.write(data));
}

// 시작
console.log('🚀 Gemini 할당량 자동 모니터링을 시작합니다. (간격: 30초)');
checkAndRun();
