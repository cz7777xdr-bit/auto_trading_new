// 파일: ollama_bridge.js
// ------------------------------------------------- [안티그래비티 <-> Ollama 연동 브릿지 (실시간 스트리밍 버전)]
const http = require('http');
const fs = require('fs');

/**
 * Ollama 로컬 API에 질문을 던지고 실시간으로 응답을 출력하는 함수
 * @param {string} prompt - Ollama에게 보낼 명령/질문
 * @param {string} model - 사용할 모델명 (기본값: qwen3)
 */
async function askOllamaStream(prompt, model = 'qwen3') {
    const data = JSON.stringify({
        model: model,
        prompt: prompt,
        stream: true // 실시간 스트리밍 활성화
    });

    const options = {
        hostname: '127.0.0.1', // localhost 대신 명시적으로 IPv4 사용
        port: 11434,
        path: '/api/generate',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(data)
        }
    };

    return new Promise((resolve, reject) => {
        const req = http.request(options, (res) => {
            res.on('data', (chunk) => {
                const lines = chunk.toString().split('\n');
                for (const line of lines) {
                    if (!line.trim()) continue;
                    try {
                        const parsed = JSON.parse(line);
                        if (parsed.response) {
                            process.stdout.write(parsed.response); // 실시간으로 터미널에 출력
                        }
                        if (parsed.done) {
                            console.log('\n--- [답변 완료] ---');
                            resolve();
                        }
                    } catch (e) {
                        // 불완전한 JSON 데이터는 무시 (다음 청크에서 합쳐짐)
                    }
                }
            });
        });

        req.on('error', (e) => reject('Ollama 연결 실패: ' + e.message));
        req.write(data);
        req.end();
    });
}

// ------------------------------------------------- [CLI 실행 부분]
const args = process.argv.slice(2);
let userPrompt = args[0];
const modelOverride = args[1] || 'qwen3';

// 파일 경로인 경우 내용을 읽어옴
if (userPrompt && fs.existsSync(userPrompt)) {
    try {
        userPrompt = fs.readFileSync(userPrompt, 'utf8');
    } catch (e) {
        console.error('파일 읽기 실패:', e.message);
        process.exit(1);
    }
}

if (!userPrompt) {
    console.error('사용법: node ollama_bridge.js "질문 내용 또는 파일경로" [모델명]');
    process.exit(1);
}

// 스트리밍 실행
askOllamaStream(userPrompt, modelOverride)
    .catch((err) => {
        console.error('\n오류 발생:', err);
        process.exit(1);
    });
