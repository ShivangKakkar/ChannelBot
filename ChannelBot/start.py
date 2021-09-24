from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup


# Start Message
@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot, msg):
	user = await bot.get_me()
	mention = user["mention"]
	await bot.send_message(
		msg.chat.id,
		Data.START.format(msg.from_user.mention, mention),
		reply_markup=InlineKeyboardMarkup(Data.buttons)
	)
	await bot.send_message(
		msg.chat.id,
		'Use below buttons to interact with me',
		reply_markup=ReplyKeyboardMarkup(
			[
				['+ Add Channels +'],
				['Manage Channels'],
				['Report a Problem']
			],
			one_time_keyboard=True,
			resize_keyboard=True
		)
	)
