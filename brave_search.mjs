// brave_search.mjs – Brave Search API를 사용한 웹 검색 모듈
import fetch from 'node-fetch';
import { config } from 'dotenv';

config();

const API_KEY = process.env.BRAVE_API_KEY;

export async function searchWeb(query, count = 5) {
    if (!API_KEY || API_KEY === 'YOUR_BRAVE_API_KEY') {
        throw new Error('BRAVE_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.');
    }

    const url = `https://api.search.brave.com/res/v1/web/search?q=${encodeURIComponent(query)}&count=${count}`;
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'X-Subscription-Token': API_KEY,
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Brave Search API 오류: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        // 필요한 정보만 추출 (title, url, snippet)
        return data.web.results.map(res => ({
            title: res.title,
            url: res.url,
            snippet: res.description
        }));
    } catch (err) {
        console.error('❌ Brave Search 실패:', err.message);
        throw err;
    }
}

// 테스트용
if (import.meta.url === `file://${process.argv[1]}`) {
    searchWeb('주식 자동매매 최신 트렌드')
        .then(res => console.log('검색 결과:', res))
        .catch(console.error);
}
