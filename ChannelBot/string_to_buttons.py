# Database string buttons to pyro buttons
from pyrogram.types import InlineKeyboardButton


async def string_to_buttons(string):
    buttons = []
    rows = string.split('\n')
    for row in rows:
        row_buttons = []
        r_b = row.split("|")
        for b in r_b:
            data = b.split('-')
            text = data[0].strip()
            url = data[1].strip()
            row_buttons.append(InlineKeyboardButton(text, url=url))
        buttons.append(row_buttons)
    return buttons
