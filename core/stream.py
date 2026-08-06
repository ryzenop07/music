"""
Music Player, Telegram Voice Chat Bot
Copyright (c) 2021-present Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import os
from config import config
from core.song import Song
from pyrogram import Client
from yt_dlp import YoutubeDL
from pytgcalls import PyTgCalls
from core.funcs import generate_cover
from core.groups import get_group, set_title
from pytgcalls.types.stream import MediaStream
from pyrogram.raw.types import InputPeerChannel
from pytgcalls.types import AudioQuality, VideoQuality
from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls.exceptions import NoActiveGroupCall  # noqa


safone = {}
ydl_opts = {
    "quiet": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
}
app = Client(
    "MusicPlayerUB",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION,
    in_memory=True,
)
ytdl = YoutubeDL(ydl_opts)
pytgcalls = PyTgCalls(app)


async def start_stream(song: Song, lang):
    chat = song.request_msg.chat
    chat_id = chat.id
    if safone.get(chat_id) is not None:
        try:
            await safone[chat_id].delete()
        except BaseException:
            pass
    infomsg = await app.send_message(chat_id, lang["downloading"])
    await _ensure_vc(chat_id)
    await pytgcalls.play(chat_id, get_quality(song))
    await set_title(chat_id, song.title, client=app)
    thumb = await generate_cover(song.title, chat.title, chat_id, song.thumb)
    requested_by = (
        song.requested_by.mention
        if song.requested_by
        else (song.request_msg.sender_chat.title if song.request_msg.sender_chat else "Unknown")
    )
    safone[chat_id] = await app.send_photo(
        chat_id,
        photo=thumb,
        caption=lang["playing"] % (
            song.title, song.source, song.duration, chat_id, requested_by,
        ),
    )
    await infomsg.delete()
    if os.path.exists(thumb):
        os.remove(thumb)


async def _ensure_vc(chat_id: int):
    try:
        peer = await app.resolve_peer(chat_id)
        await app.invoke(
            CreateGroupCall(
                peer=InputPeerChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash,
                ),
                random_id=app.rnd_id() // 9000000000,
            )
        )
    except Exception:
        pass


def get_quality(song: Song) -> MediaStream:
    group = get_group(song.request_msg.chat.id)
    if group["stream_mode"] == "video":
        if config.QUALITY.lower() == "high":
            return MediaStream(
                song.remote,
                AudioQuality.HIGH,
                VideoQuality.FHD_1080p,
                headers=song.headers,
            )
        elif config.QUALITY.lower() == "medium":
            return MediaStream(
                song.remote,
                AudioQuality.MEDIUM,
                VideoQuality.HD_720p,
                headers=song.headers,
            )
        elif config.QUALITY.lower() == "low":
            return MediaStream(
                song.remote,
                AudioQuality.LOW,
                VideoQuality.SD_480p,
                headers=song.headers,
            )
        else:
            print("WARNING: Invalid Quality Specified. Defaulting to High!")
            return MediaStream(
                song.remote,
                AudioQuality.HIGH,
                VideoQuality.FHD_1080p,
                headers=song.headers,
            )
    else:
        if config.QUALITY.lower() == "high":
            return MediaStream(
                song.remote,
                AudioQuality.HIGH,
                video_flags=MediaStream.Flags.IGNORE,
                headers=song.headers,
            )
        elif config.QUALITY.lower() == "medium":
            return MediaStream(
                song.remote,
                AudioQuality.MEDIUM,
                video_flags=MediaStream.Flags.IGNORE,
                headers=song.headers,
            )
        elif config.QUALITY.lower() == "low":
            return MediaStream(
                song.remote,
                AudioQuality.LOW,
                video_flags=MediaStream.Flags.IGNORE,
                headers=song.headers,
            )
        else:
            print("WARNING: Invalid Quality Specified. Defaulting to High!")
            return MediaStream(
                song.remote,
                AudioQuality.HIGH,
                video_flags=MediaStream.Flags.IGNORE,
                headers=song.headers,
            )
