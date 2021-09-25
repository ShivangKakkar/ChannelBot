import asyncio.exceptions

from pyrogram import Client, filters
from pyrogram.errors import ButtonUrlInvalid
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from ChannelBot.database.channel_sql import get_channel_info, get_sticker
from ChannelBot.database.channel_sql import remove_channel as crc
from ChannelBot.database.channel_sql import (
    set_buttons,
    set_caption,
    set_edit_mode,
    set_position,
    set_sticker,
    toggle_webpage_preview,
)
from ChannelBot.database.users_sql import remove_channel as urc
from ChannelBot.manage import manage_channels
from ChannelBot.settings import channel_settings
from ChannelBot.string_to_buttons import string_to_buttons
from Data import Data


# Callbacks
@Client.on_callback_query()
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    user = await bot.get_me()
    user_id = callback_query.from_user.id
    mention = user["mention"]
    query = callback_query.data.lower()
    if query.startswith("home"):
        if query == "home":
            chat_id = callback_query.from_user.id
            message_id = callback_query.message.message_id
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=Data.START.format(callback_query.from_user.mention,
                                       mention),
                reply_markup=InlineKeyboardMarkup(Data.buttons),
            )
            await callback_query.answer()
        elif query == "home+channels":
            success, buttons, text = await manage_channels(user_id, bot)
            if success:
                await callback_query.edit_message_text(
                    text, reply_markup=InlineKeyboardMarkup(buttons))
                await callback_query.answer()
            else:
                await callback_query.edit_message_text(text)
                await callback_query.answer()
        elif query.startswith("home+"):
            channel_id = int(query.split("+")[-1])
            text, markup, sticker_id = await channel_settings(channel_id, bot)
            if text:
                await callback_query.edit_message_text(
                    text,
                    reply_markup=InlineKeyboardMarkup(markup),
                    disable_web_page_preview=True,
                )
                await callback_query.answer()
    elif query == "about":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.ABOUT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
        await callback_query.answer()
    elif query == "help":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="**Here's How to use me**\n" + Data.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
        await callback_query.answer()
    elif query.startswith("settings"):
        channel_id = int(query.split("+")[1])
        text, markup, sticker_id = await channel_settings(channel_id, bot)
        if sticker_id:
            await callback_query.message.reply_sticker(sticker_id)
        if text:
            await callback_query.message.delete()
            await callback_query.message.reply(
                text,
                reply_markup=InlineKeyboardMarkup(markup),
                disable_web_page_preview=True,
            )
        else:
            await callback_query.answer(
                "Channel Not Found. Please add again !", show_alert=True)
            await crc(channel_id)
            await urc(user_id, channel_id)
            await callback_query.message.delete()
    elif query.startswith("change"):
        change = query.split("+")[1]
        channel_id = int(query.split("+")[2])
        success, info = await get_channel_info(channel_id)
        if success:
            buttons = info["buttons"]
            caption = info["caption"]
            # position = info['position']
            # webpage_preview = info['webpage_preview']
            sticker_id = info["sticker_id"]
            if change == "caption":
                if caption:
                    buttons = [
                        [
                            InlineKeyboardButton(
                                "Change Caption",
                                callback_data=f"add+{change}+{channel_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Remove Caption",
                                callback_data=f"remove+{change}+{channel_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "<- Back to Channel Settings",
                                callback_data=f"home+{channel_id}",
                            )
                        ],
                    ]
                    await callback_query.edit_message_text(
                        f"Current Caption is : `{caption}` \n\nUse below buttons to change or remove it.",
                        reply_markup=InlineKeyboardMarkup(buttons),
                    )
                    await callback_query.answer()
                else:
                    buttons = [
                        [
                            InlineKeyboardButton(
                                "Add Caption",
                                callback_data=f"add+{change}+{channel_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "<-- Back to Channel Settings",
                                callback_data=f"home+{channel_id}",
                            )
                        ],
                    ]
                    await callback_query.edit_message_text(
                        "No Caption set \n\nUse below button to add it.",
                        reply_markup=InlineKeyboardMarkup(buttons),
                    )
                    await callback_query.answer()
            elif change == "buttons":
                if buttons:
                    _buttons = [
                        [
                            InlineKeyboardButton(
                                "Change URL Buttons",
                                callback_data=f"add+{change}+{channel_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Remove URL Buttons",
                                callback_data=f"remove+{change}+{channel_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "<-- Back to Channel Settings",
                                callback_data=f"home+{channel_id}",
                            )
                        ],
                    ]
                    await callback_query.edit_message_text(
                        f"Current Buttons are : `{buttons}` \n\nUse below buttons to change or remove it.",
                        reply_markup=InlineKeyboardMarkup(_buttons),
                    )
                    await callback_query.answer()
                else:
                    _buttons = [
                        [
                            InlineKeyboardButton(
                                "Add Buttons",
                                callback_data=f"add+{change}+{channel_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "<-- Back to Channel Settings",
                                callback_data=f"home+{channel_id}",
                            )
                        ],
                    ]
                    await callback_query.edit_message_text(
                        "No Buttons set \n\nUse below button to add them.",
                        reply_markup=InlineKeyboardMarkup(_buttons),
                    )
                    await callback_query.answer()
            elif change == "position":
                current_position = query.split("+")[3]
                if current_position == "below":
                    new_position = "above"
                elif current_position == "above":
                    new_position = "replace"
                else:
                    new_position = "below"
                await set_position(channel_id, new_position)
                text, markup, __ = await channel_settings(channel_id, bot)
                if text:
                    await callback_query.edit_message_text(
                        text,
                        reply_markup=InlineKeyboardMarkup(markup),
                        disable_web_page_preview=True,
                    )
                    await callback_query.answer()
                else:
                    await callback_query.answer(
                        "Channel doesn't exist in database", show_alert=True)
                    await callback_query.message.delete()
            elif change == "edit_mode":
                current_edit_mode = query.split("+")[3]
                if current_edit_mode == "all":
                    new_edit_mode = "media"
                else:
                    new_edit_mode = "all"
                await set_edit_mode(channel_id, new_edit_mode)
                text, markup, __ = await channel_settings(channel_id, bot)
                if text:
                    await callback_query.edit_message_text(
                        text,
                        reply_markup=InlineKeyboardMarkup(markup),
                        disable_web_page_preview=True,
                    )
                    await callback_query.answer()
                else:
                    await callback_query.answer(
                        "Channel doesn't exist in database", show_alert=True)
                    await callback_query.message.delete()
            elif change == "sticker":
                if sticker_id:
                    buttons = [
                        [
                            InlineKeyboardButton(
                                "Show Current Sticker",
                                callback_data=f"show+{channel_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Change Sticker",
                                callback_data=f"add+{change}+{channel_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Remove Sticker",
                                callback_data=f"remove+{change}+{channel_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "<-- Back to Channel Settings",
                                callback_data=f"home+{channel_id}",
                            )
                        ],
                    ]
                    await callback_query.edit_message_text(
                        "A sticker is already set. See it by tapping 'Show Current Sticker' button \n\nUse below buttons to change or remove it.",
                        reply_markup=InlineKeyboardMarkup(buttons),
                    )
                    await callback_query.answer()
                else:
                    buttons = [
                        [
                            InlineKeyboardButton(
                                "Add Sticker",
                                callback_data=f"add+{change}+{channel_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "<-- Back to Channel Settings",
                                callback_data=f"home+{channel_id}",
                            )
                        ],
                    ]
                    await callback_query.edit_message_text(
                        "No Sticker set \n\nUse below button to add it.",
                        reply_markup=InlineKeyboardMarkup(buttons),
                    )
                    await callback_query.answer()
            elif change == "webpage_preview":
                current = query.split("+")[3]
                if current.lower() == "true":
                    new = False
                else:
                    new = True
                await toggle_webpage_preview(channel_id, new)
                text, markup, __ = await channel_settings(channel_id, bot)
                if text:
                    await callback_query.edit_message_text(
                        text,
                        reply_markup=InlineKeyboardMarkup(markup),
                        disable_web_page_preview=True,
                    )
                    await callback_query.answer()
                else:
                    await callback_query.answer(
                        "Channel doesn't exist in database", show_alert=True)
                    await callback_query.message.delete()
    elif query.startswith("add"):
        add = query.split("+")[1]
        channel_id = int(query.split("+")[2])
        try:
            if add == "caption":
                data = await bot.ask(
                    user_id,
                    "Please send the new caption or /cancel the process. Anything you send now will be set as caption so be careful !",
                    timeout=300,
                )
                if data.text.lower() == "/cancel":
                    await data.reply("Cancelled", quote=True)
                else:
                    await set_caption(channel_id, data.text.markdown)
                    await data.reply("Caption set successfully !", quote=True)
                    text, markup, sticker_id = await channel_settings(
                        channel_id, bot)
                    if sticker_id:
                        await callback_query.message.reply_sticker(sticker_id)
                    if text:
                        await callback_query.message.delete()
                        await callback_query.message.reply(
                            text,
                            reply_markup=InlineKeyboardMarkup(markup),
                            disable_web_page_preview=True,
                        )
                    else:
                        await callback_query.answer(
                            "Channel Not Found. Please add again !",
                            show_alert=True)
                        await crc(channel_id)
                        await urc(user_id, channel_id)
                        await callback_query.message.delete()
            elif add == "buttons":
                data = await bot.ask(
                    user_id,
                    "Please send the new buttons or /cancel the process.",
                    timeout=300,
                )
                # Explain how buttons
                while True:
                    if data.text == "/cancel":
                        await data.reply("Cancelled", quote=True)
                        break
                    if "-" not in data.text:
                        data = await bot.ask(
                            user_id,
                            "Wrong Format for Buttons! Please try again.",
                            timeout=300,
                        )
                    else:
                        given_buttons = await string_to_buttons(data.text)
                        try:
                            await data.reply(
                                "How they will look !",
                                reply_markup=InlineKeyboardMarkup(
                                    given_buttons),
                            )
                            await set_buttons(channel_id, data.text)
                            await data.reply("Buttons set successfully !",
                                             quote=True)
                            text, markup, sticker_id = await channel_settings(
                                channel_id, bot)
                            if sticker_id:
                                await callback_query.message.reply_sticker(
                                    sticker_id)
                            if text:
                                await callback_query.message.delete()
                                await callback_query.message.reply(
                                    text,
                                    reply_markup=InlineKeyboardMarkup(markup),
                                    disable_web_page_preview=True,
                                )
                            else:
                                await callback_query.answer(
                                    "Channel Not Found. Please add again !",
                                    show_alert=True,
                                )
                                await crc(channel_id)
                                await urc(user_id, channel_id)
                                await callback_query.message.delete()
                            break
                        except ButtonUrlInvalid:
                            data = await bot.ask(
                                user_id,
                                "Wrong Format for Buttons! Please try again.",
                                timeout=300,
                            )
            elif add == "sticker":
                data = await bot.ask(
                    user_id,
                    "Please send a sticker.",
                    timeout=300,
                    filters=filters.sticker,
                )
                await set_sticker(channel_id, data.sticker.file_id)
                await data.reply("Sticker set successfully !", quote=True)
                text, markup, sticker_id = await channel_settings(
                    channel_id, bot)
                if sticker_id:
                    await callback_query.message.reply_sticker(sticker_id)
                if text:
                    await callback_query.message.delete()
                    await callback_query.message.reply(
                        text,
                        reply_markup=InlineKeyboardMarkup(markup),
                        disable_web_page_preview=True,
                    )
                else:
                    await callback_query.answer(
                        "Channel Not Found. Please add again !",
                        show_alert=True)
                    await crc(channel_id)
                    await urc(user_id, channel_id)
                    await callback_query.message.delete()
            else:
                # Won't happen
                pass
        except asyncio.exceptions.TimeoutError:
            pass
    elif query.startswith("remove"):
        args = query.split("+")
        if len(args) == 2:
            channel_id = int(args[1])
            await crc(channel_id)
            await urc(user_id, channel_id)
            await callback_query.answer("Removed Channel Successfully",
                                        show_alert=True)
            success, buttons, text = await manage_channels(user_id, bot)
            if success:
                await callback_query.edit_message_text(
                    text, reply_markup=InlineKeyboardMarkup(buttons))
                await callback_query.answer()
            else:
                await callback_query.edit_message_text("No Channels Found")
                await callback_query.answer()
        else:
            remove = args[1]
            channel_id = int(args[2])
            if remove == "caption":
                await set_caption(channel_id, None)
                await callback_query.answer("Caption removed successfully !",
                                            show_alert=True)
                text, markup, sticker_id = await channel_settings(
                    channel_id, bot)
                if sticker_id:
                    await callback_query.message.reply_sticker(sticker_id)
                if text:
                    await callback_query.edit_message_text(
                        text,
                        reply_markup=InlineKeyboardMarkup(markup),
                        disable_web_page_preview=True,
                    )
                    await callback_query.answer()
                else:
                    await callback_query.answer(
                        "Channel Not Found. Please add again !",
                        show_alert=True)
                    await crc(channel_id)
                    await urc(user_id, channel_id)
                    await callback_query.message.delete()
            elif remove == "buttons":
                await set_buttons(channel_id, None)
                await callback_query.answer("Buttons removed successfully !",
                                            show_alert=True)
                text, markup, sticker_id = await channel_settings(
                    channel_id, bot)
                if sticker_id:
                    await callback_query.message.reply_sticker(sticker_id)
                if text:
                    await callback_query.edit_message_text(
                        text,
                        reply_markup=InlineKeyboardMarkup(markup),
                        disable_web_page_preview=True,
                    )
                    await callback_query.answer()
                else:
                    await callback_query.answer(
                        "Channel Not Found. Please add again !",
                        show_alert=True)
                    await crc(channel_id)
                    await urc(user_id, channel_id)
                    await callback_query.message.delete()
            elif remove == "sticker":
                await set_sticker(channel_id, None)
                await callback_query.answer("Sticker removed successfully !",
                                            show_alert=True)
                text, markup, sticker_id = await channel_settings(
                    channel_id, bot)
                if sticker_id:
                    await callback_query.message.reply_sticker(sticker_id)
                if text:
                    await callback_query.edit_message_text(
                        text,
                        reply_markup=InlineKeyboardMarkup(markup),
                        disable_web_page_preview=True,
                    )
                    await callback_query.answer()
                else:
                    await callback_query.answer(
                        "Channel Not Found. Please add again !",
                        show_alert=True)
                    await crc(channel_id)
                    await urc(user_id, channel_id)
                    await callback_query.message.delete()
            else:
                # Won't happen
                pass
    elif query.startswith("show"):
        channel_id = int(query.split("+")[1])
        sticker_id = await get_sticker(channel_id)
        if sticker_id:
            sticker = await callback_query.message.reply_sticker(sticker_id)
            await sticker.reply("This is the current sticker", quote=True)
        else:
            await callback_query.answer("Channel Not Found.", show_alert=True)
            await callback_query.message.delete()
