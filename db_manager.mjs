// db_manager.mjs – SQLite3를 활용한 검색 결과 저장 및 관리 모듈
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import { config } from 'dotenv';
import path from 'path';

config();

const DB_PATH = process.env.DATABASE_PATH || './search_results.db';

export async function initDb() {
  const db = await open({
    filename: DB_PATH,
    driver: sqlite3.Database
  });

  await db.exec(`
    CREATE TABLE IF NOT EXISTS search_results (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      query TEXT,
      title TEXT,
      url TEXT,
      snippet TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  return db;
}

export async function saveResults(query, results) {
  const db = await initDb();
  for (const res of results) {
    await db.run(
      'INSERT INTO search_results (query, title, url, snippet) VALUES (?, ?, ?, ?)',
      [query, res.title, res.url, res.snippet]
    );
  }
  console.log(`💾 ${results.length}개의 결과를 SQLite(${DB_PATH})에 저장했습니다.`);
  await db.close();
}

export async function getRecentResults(limit = 10) {
    const db = await initDb();
    const rows = await db.all('SELECT * FROM search_results ORDER BY created_at DESC LIMIT ?', [limit]);
    await db.close();
    return rows;
}
