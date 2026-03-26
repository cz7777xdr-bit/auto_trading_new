// watcher.js – Cursor와 파이프라인 연동용 파일 감시 스크립트
import chokidar from 'chokidar';
import { exec } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ---------- 설정 ----------
// 감시할 파일 (사용자가 수정하거나 Cursor AI가 생성할 파일)
const WATCH_TARGET = 'generated_code.js'; 
const PIPELINE_SCRIPT = 'pipeline_omo.js';

console.log('👀 [Watcher] 켜짐. Cursor가 ' + WATCH_TARGET + ' 파일을 변경하면 자동으로 분석 파이프라인이 작동합니다.');

// ---------- 감시 로직 ----------
const watcher = chokidar.watch(path.resolve(__dirname, WATCH_TARGET), {
  persistent: true,
  ignoreInitial: true,
});

let isRunning = false;

watcher.on('change', (filePath) => {
  if (isRunning) return; // 중복 실행 방지
  
  console.log(`\n🔔 [Watcher] 파일 변경 감지: ${path.basename(filePath)}`);
  console.log('🚀 파이프라인(pipeline_omo.js) 실행을 시작합니다...');
  
  isRunning = true;
  
  exec(`node "${path.resolve(__dirname, PIPELINE_SCRIPT)}"`, (err, stdout, stderr) => {
    if (err) {
      console.error('❌ 파이프라인 실행 중 오류:', err.message);
    }
    
    if (stdout) console.log('✅ 출력:\n', stdout);
    if (stderr) console.log('⚠️ 경고:\n', stderr);
    
    isRunning = false;
    console.log('💤 [Watcher] 대기 중... 새로운 변경사항을 기다립니다.');
  });
});

watcher.on('error', (error) => console.error(`[Watcher] 오류: ${error}`));
