import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# n8n 웹훅 설정
# 테스트 시: http://localhost:5678/webhook-test/discord-trigger
# 운영 시: http://localhost:5678/webhook/discord-trigger
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook-test/discord-trigger")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# 봇 권한 설정
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용을 읽기 위해 필요

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    # 봇 본인의 메시지는 무시
    if message.author == bot.user:
        return

    # n8n 웹훅으로 데이터 전송
    payload = {
        "author": str(message.author),
        "content": message.content,
        "channel_id": str(message.channel.id),
        "guild": str(message.guild.name) if message.guild else "DM",
        "timestamp": str(message.created_at)
    }

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print(f"Successfully sent to n8n: {message.content}")
        else:
            print(f"Failed to send to n8n. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending to n8n: {e}")

    await bot.process_commands(message)

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN is missing in .env file")
    else:
        bot.run(DISCORD_TOKEN)
