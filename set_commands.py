import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

COMMANDS = [
    ("start", "🎵 Start Laya Music Bot"),
    ("help", "📋 Show all commands"),
    ("ping", "🏓 Check if bot is alive"),
    ("play", "▶️ Play a song or YouTube link"),
    ("radio", "📻 Stream a live radio or URL"),
    ("playlist", "🎶 Play a YouTube playlist"),
    ("skip", "⏭ Skip to next song"),
    ("pause", "⏸ Pause current stream"),
    ("resume", "▶️ Resume paused stream"),
    ("mute", "🔇 Mute the stream"),
    ("unmute", "🔊 Unmute the stream"),
    ("stop", "⏹ Stop and leave voice chat"),
    ("loop", "🔁 Toggle loop mode"),
    ("queue", "📋 Show song queue"),
    ("shuffle", "🔀 Shuffle the queue"),
    ("mode", "🎬 Switch audio/video mode"),
    ("export", "💾 Export queue to file"),
    ("import", "📂 Import queue from file"),
    ("lang", "🌍 Set bot language"),
    ("admins", "👑 Toggle admins-only mode"),
    ("repo", "🔗 Show source code link"),
]


async def set_commands():
    import aiohttp
    commands_payload = [{"command": cmd, "description": desc} for cmd, desc in COMMANDS]
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"
    async with aiohttp.ClientSession() as session:
        resp = await session.post(url, json={"commands": commands_payload})
        data = await resp.json()
        if data.get("ok"):
            print("✅ Bot commands set successfully!")
            print(f"   Total: {len(COMMANDS)} commands registered")
        else:
            print(f"❌ Failed: {data}")


asyncio.run(set_commands())
