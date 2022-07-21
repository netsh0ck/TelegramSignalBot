from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ContentType, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions

import asyncio

TOKEN = 'TOKEN HERE'  # Get this from @Botfather
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=ContentType.NEW_CHAT_MEMBERS)
async def new_members(msg):
    members = msg.new_chat_members
    for member in members:
        tg_id = member.id
        name = member.first_name

        disable = ChatPermissions(
            can_send_messages=False,
            can_send_polls=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_change_info=False,
            can_add_web_page_previews=False,
        )
        await bot.restrict_chat_member(msg.chat.id, tg_id, permissions=disable)
        rk = InlineKeyboardMarkup()
        rightbutton = InlineKeyboardButton(text='Press me', callback_data=f'captcha_right+{tg_id}')
        rk.row(rightbutton)
        welcome = f'Welcome, [{name}](tg://user?id={tg_id})!' \
                  f'\n\nPlease press the button below within 60 seconds, otherwise you will be kicked'
        welcomemsg = await msg.answer(welcome, reply_markup=rk, parse_mode='Markdown')
        await remove(welcomemsg, member.id)


async def remove(message, member_id):
    print(1)
    await asyncio.sleep(60)
    try:
        await message.delete()
        await bot.kick_chat_member(message.chat.id, member_id)
        await bot.unban_chat_member(message.chat.id, member_id)
    except Exception:
        pass



@dp.callback_query_handler(lambda call: True)
async def callback_inline(call):
    if call.message:
        if 'captcha_right' in call.data:
            tg_id = call.data[call.data.index('+')+1:]

            if str(tg_id) == str(call.from_user.id):
                good_boy = ChatPermissions(can_send_messages=True,
                                           can_invite_users=True,
                                           can_send_media_messages=True,
                                           can_send_other_messages=True)
                await bot.restrict_chat_member(call.message.chat.id, call.from_user.id, permissions=good_boy)
                await bot.delete_message(call.message.chat.id, call.message.message_id)

            else:
                pass
        else:
            pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
