const fs = require('fs').promises;
const path = require('path');

async function main() {
  if (process.argv.length !== 4) {
    console.error('Usage: node cursor_generate.js <filename> "<code>"');
    process.exit(1);
  }

  const [, , filename, code] = process.argv;
  const outPath = path.resolve(filename);

  try {
    await fs.writeFile(outPath, code, 'utf-8');
    console.log(`[INFO] 코드가 ${outPath} 에 저장되었습니다.`);
  } catch (err) {
    console.error('[ERROR] 파일 저장 중 오류 발생:', err);
    process.exit(1);
  }
}

main();
