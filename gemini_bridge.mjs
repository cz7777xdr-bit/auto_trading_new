// gemini_bridge.js – Google AI Studio (Gemini) API 연동 브릿지
import fetch from 'node-fetch';
import { config } from 'dotenv';

config();

const API_KEY = process.env.GEMINI_API_KEY;
const MODEL = process.env.GEMINI_MODEL || 'gemini-1.5-flash';
const ENDPOINT = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}`;

/**
 * Google AI Studio (Gemini) API를 호출합니다.
 * @param {string} prompt - 보낼 텍스트 프롬프트
 * @returns {Promise<string>} - Gemini의 응답 텍스트
 */
export async function askGemini(prompt) {
    if (!API_KEY || API_KEY === 'YOUR_GEMINI_API_KEY') {
        throw new Error('GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.');
    }

    const payload = {
        contents: [{
            parts: [{ text: prompt }]
        }]
    };

    try {
        const response = await fetch(ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(`Gemini API 오류: ${error.error.message || response.statusText}`);
        }

        const data = await response.json();
        return data.candidates[0].content.parts[0].text;
    } catch (err) {
        console.error('❌ Gemini 연동 실패:', err.message);
        throw err;
    }
}

// 직접 실행 테스트
if (import.meta.url === `file://${process.argv[1]}`) {
    askGemini('안녕! 너는 누구니? 한글로 대답해줘.')
        .then(res => console.log('Gemini 응답:', res))
        .catch(err => console.error('테스트 실패:', err));
}
