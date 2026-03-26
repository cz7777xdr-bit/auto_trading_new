// Discord Bot – result_ollama.txt 를 Discord 채널에 전송
require('dotenv').config(); // .env 에 DISCORD_TOKEN, DISCORD_CHANNEL_ID 필요
const { Client, GatewayIntentBits } = require('discord.js');
const fs = require('fs').promises;
const path = require('path');

const TOKEN = process.env.DISCORD_TOKEN;
const CHANNEL_ID = process.env.DISCORD_CHANNEL_ID;

if (!TOKEN || !CHANNEL_ID) {
  console.error('DISCORD_TOKEN 혹은 DISCORD_CHANNEL_ID 가 .env 에 설정되지 않았습니다.');
  process.exit(1);
}

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] });

client.once('ready', async () => {
  console.log(`✅ Discord 로그인 성공: ${client.user.tag}`);
  const resultPath = path.resolve(__dirname, 'result_ollama.txt');
  const content = await fs.readFile(resultPath, 'utf-8');
  const channel = await client.channels.fetch(CHANNEL_ID);
  await channel.send(`🖥️ Ollama 실행 결과:\n\`\`\`
${content.trim()}
\`\`\``);
  console.log('✅ 결과를 Discord 채널에 전송했습니다.');
  client.destroy();
});

client.login(TOKEN).catch(err => {
  console.error('Discord 로그인 실패:', err);
  process.exit(1);
});
