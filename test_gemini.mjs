import fetch from 'node-fetch';
import { config } from 'dotenv';
config();
const key = process.env.GEMINI_API_KEY;
const model = process.env.GEMINI_MODEL;
async function test() {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: [{ text: "Hi" }] }] })
  });
  console.log(res.status, await res.json());
}
test();
