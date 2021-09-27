from pyrogram import emoji
from pyrogram.types import InlineKeyboardButton
from ChannelBot.database.channel_sql import get_channel_info


async def channel_settings(channel_id, bot):
    success, info = await get_channel_info(channel_id)
    if success:
        title = (await bot.get_chat(channel_id)).title
        text = f'**{title}** (`{channel_id}`) \n\n'
        buttons = info['buttons']
        caption = info['caption']
        position = info['position']
        webpage_preview = info['webpage_preview']
        sticker_id = info['sticker_id']
        edit_mode = info['edit_mode']
        if caption:
            text += f"**Caption** : Set \n\n"
        else:
            text += f'**Caption** : Not Set. \n\n'
        if position:
            text += f'**Caption Position** : {position.capitalize()} the previous caption\n\n'
        else:
            position = 'below'
            text += f'**Caption Position** : {position.capitalize()} the previous caption\n\n'
        if buttons:
            text += f"**Buttons** : Set \n\n"
        else:
            text += f'**Buttons** : Not Set. \n\n'
        if edit_mode:
            text += f'**Edit Mode** : {edit_mode.capitalize()} Messages\n\n'
        else:
            edit_mode = 'media'
            text += f'**Edit Mode** : {edit_mode.capitalize()} Messages\n\n'
        if sticker_id:
            text += f'**Sticker** : Set (Sent Above)\n\n'
        else:
            text += f'**Sticker** : Not Set \n\n'
        if webpage_preview:
            text += f'**Webpage Preview** : True \n\n'
        else:
            text += f'**Webpage Preview** : False \n\n'
            webpage_preview = 'False'
        markup = [
            [
                InlineKeyboardButton(f'{emoji.MEMO}Caption', callback_data=f'change+caption+{channel_id}'),
                InlineKeyboardButton(f'{emoji.LINK}Buttons', callback_data=f'change+buttons+{channel_id}')
            ],
            [InlineKeyboardButton(f'{emoji.LEAF_FLUTTERING_IN_WIND}Caption Mode : {position.capitalize()}', callback_data=f'change+position+{channel_id}+{position}')],
            [InlineKeyboardButton(f'{emoji.SUNSET}Sticker', callback_data=f'change+sticker+{channel_id}')],
            [InlineKeyboardButton(f'{emoji.PENCIL}Edit Mode : {edit_mode.capitalize()}', callback_data=f'change+edit_mode+{channel_id}+{edit_mode}')],
            [InlineKeyboardButton(f'{emoji.OPEN_BOOK}Webpage Preview : {webpage_preview}', callback_data=f'change+webpage_preview+{channel_id}+{webpage_preview}')],
            [InlineKeyboardButton(f'{emoji.WASTEBASKET}Remove Channel', callback_data=f'remove+{channel_id}')],
            [InlineKeyboardButton('<-- Back', callback_data='home+channels')]
        ]
    else:
        text = None
        markup = None
        sticker_id = None
    return text, markup, sticker_id
