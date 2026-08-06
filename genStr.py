from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

print("╔══「 🔑 LAYA SESSION GENERATOR 」══╗")
print("  Generating Pyrogram String Session")
print("╚══════════════════════════════════╝\n")

with Client(":memory:", api_id=API_ID, api_hash=API_HASH) as app:
    session = app.export_session_string()
    print("\n╔══「 ✅ YOUR SESSION STRING 」══╗")
    print(session)
    print("╚══════════════════════════════════╝")
    print("\n⚠️  Copy the above string and paste it in .env as SESSION='...'")
