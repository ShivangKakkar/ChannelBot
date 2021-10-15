import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.errors.exceptions import FloodWait
from ChannelBot.database.channel_sql import (
    get_caption,
    get_position,
    get_buttons,
    get_webpage_preview,
    get_sticker,
    get_edit_mode
)
from ChannelBot.string_to_buttons import string_to_buttons


# def all_channels():
#     channels = SESSION.query(Channel).all()
#     channels_ids = [channel.channel_id for channel in channels]
#     SESSION.close()
#     return channels_ids


@Client.on_message(filters.channel & ~filters.edited & ~filters.forwarded)
async def modify(_, msg: Message):
    channel_id = msg.chat.id
    caption = await get_caption(channel_id)
    sticker = await get_sticker(channel_id)
    edit_mode = await get_edit_mode(channel_id)
    if edit_mode == 'media' and not msg.media:
        return
    try:
        if caption:
            position = await get_position(channel_id)
            buttons = await get_buttons(channel_id)
            if buttons:
                buttons = await string_to_buttons(buttons)
            webpage_preview = await get_webpage_preview(channel_id)
            if position == 'above':
                if msg.caption:
                    caption += '\n\n' + msg.caption.markdown
                elif msg.text:
                    caption += '\n\n' + msg.text.markdown
            elif position == 'below':
                if msg.caption:
                    caption = msg.caption.markdown + '\n\n' + caption
                elif msg.text:
                    caption = msg.text.markdown + '\n\n' + caption
            if webpage_preview:
                disable_webpage_preview = False
            else:
                disable_webpage_preview = True
            if buttons:
                await msg.edit_text(
                    caption,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    disable_web_page_preview=disable_webpage_preview,
                    parse_mode="markdown"
                )
            else:
                await msg.edit_text(
                    caption,
                    disable_web_page_preview=disable_webpage_preview,
                    parse_mode="markdown"
                )
        if sticker:
            await msg.reply_sticker(sticker, quote=False)
    except FloodWait as e:
        await asyncio.sleep(e.x)
