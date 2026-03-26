import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';
import { config } from 'dotenv';

config();

const OMO_ENDPOINT = process.env.OMO_ENDPOINT || 'https://api.opencode.com/omo/v1/run';
const OMO_TOKEN = process.env.OMO_TOKEN;

/**
 * OpenCode OMO API를 통해 코드를 실행합니다.
 * @param {string} language - 실행할 언어 (예: 'python', 'javascript')
 * @param {string} code - 실행할 소스 코드
 * @param {object} [inputs] - 코드에 전달할 추가 입력 (예: {"query": "주식"})
 * @returns {Promise<string>} - 실행 결과 (stdout)
 */
export async function runWithOMO(language, code, inputs = {}) {
  if (!OMO_TOKEN || OMO_TOKEN === 'YOUR_OMO_API_TOKEN') {
    throw new Error('OMO_TOKEN이 설정되지 않았습니다. .env 파일을 확인해주세요.');
  }

  const payload = {
    language,
    code,
    inputs
  };

  try {
    const response = await fetch(OMO_ENDPOINT, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OMO_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`OMO API 요청 실패: ${response.status} ${errorText}`);
    }

    const data = await response.json();
    
    // OMO API 응답 구조에 따라 수정이 필요할 수 있습니다.
    // 보통 { "stdout": "...", "stderr": "...", "exitCode": 0 } 형태라 가정합니다.
    if (data.stderr && !data.stdout) {
        return `Error: ${data.stderr}`;
    }
    
    return data.stdout || JSON.stringify(data, null, 2);
  } catch (error) {
    console.error('OMO 연동 오류:', error.message);
    throw error;
  }
}

// 직접 실행 시 테스트 코드
if (import.meta.url === `file://${path.resolve(process.argv[1]).replace(/\\/g, '/')}`) {
  const testCode = 'print("Hello from OMO!")';
  runWithOMO('python', testCode)
    .then(res => console.log('테스트 결과:', res))
    .catch(err => console.error('테스트 실패:', err));
}
