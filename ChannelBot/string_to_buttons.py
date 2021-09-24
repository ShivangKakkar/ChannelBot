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
            text = data[0]
            while text.startswith(" "):
                text = text[1:]
            while text.endswith(" "):
                text = text[:-1]
            url = data[1]
            while url.startswith(" "):
                url = url[1:]
            while url.endswith(" "):
                url = url[:-1]
            row_buttons.append(InlineKeyboardButton(text, url=url))
        buttons.append(row_buttons)
    return buttons
