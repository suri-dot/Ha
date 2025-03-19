import discord from discord.ext import commands import yt_dlp import os from collections import defaultdict

intents = discord.Intents.default() intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = [] # 플레이리스트 play_count = defaultdict(int) # 노래 들은 횟수 기록

@bot.event async def on_ready(): print(f"Logged in as {bot.user}")

@bot.command(name='재생') async def play(ctx, url: str): voice_channel = ctx.author.voice.channel if not voice_channel: await ctx.send("음성 채널에 먼저 들어가세요!") return

vc = await voice_channel.connect()

# 노래 제목 가져오기
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False) # 다운로드 하지 않고 정보만 가져옴
    title = info.get('title', None) # 노래 제목
    queue.append(title) # 플레이리스트에 노래 제목 추가
    play_count[title] += 1 # 노래 들은 횟수 증가

await ctx.send(f"플레이리스트에 추가된 노래: {title} (들음 횟수: {play_count[title]})")

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'song.mp3',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

vc.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("재생 완료"))
await ctx.send("음악을 재생합니다!")

@bot.command(name='일시정지') async def pause(ctx): if ctx.voice_client.is_playing(): ctx.voice_client.pause() await ctx.send("음악을 일시정지했습니다.") else: await ctx.send("현재 재생 중인 음악이 없습니다.")

@bot.command(name='다시재생') async def resume(ctx): if ctx.voice_client.is_paused(): ctx.voice_client.resume() await ctx.send("음악을 다시 재생합니다.") else: await ctx.send("현재 음악이 일시정지 상태가 아닙니다.")

@bot.command(name='플레이리스트') async def queue_cmd(ctx): if queue: await ctx.send("현재 플레이리스트:\n" + "\n".join(queue)) else: await ctx.send("플레이리스트가 비어 있습니다.")

@bot.command(name='종료') async def stop(ctx): if ctx.voice_client: await ctx.voice_client.disconnect() await ctx.send("음성 채널에서 나갔습니다.") else: await ctx.send("봇이 음성 채널에 없습니다.")

TOKEN = "MTM1MTQ5NzE3OTQxNTcxMTc0NA.GydUXw.lDf6F6AextDXSqwGgG9ENA9i1z3QB9O_690zp0" bot.run(TOKEN)
