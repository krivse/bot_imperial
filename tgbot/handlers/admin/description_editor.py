from sqlalchemy import insert

from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from tgbot.misc.states import AboutState, RulesState
from tgbot.services.db.models import About, Rules
from tgbot.services.set_commands import commands


async def change_about(message: Message, state: FSMContext):
    """Команда для редактирования описания."""
    msg = await message.bot.send_message(
        chat_id=message.from_id,
        text='<i>Введите текст, который будет выводится;\n'
             'Для форматирования используйте '
             '<a href="https://core.telegram.org/bots/api#formatting-options">документацию</a>;\n'
             'Ниже приведены примеры использования тегов из документации:</i>\n'
             '  - <b>bold</b>\n'
             '  - <i>italic</i>\n'
             '  - <u>underline</u>\n'
             '  - <s>strikethrough</s>\n'
             '  - <tg-spoiler>spoiler</tg-spoiler>\n'
             '  - <b>bold <i>italic bold <s>italic bold strikethrough'
             '</s> <u>underline italic bold</u></i> bold</b>'
    )
    await state.update_data(message_id=msg.message_id)
    await AboutState.text.set()


async def record_about(message: Message, session, state: FSMContext):
    """Запись новой информации о команде в БД."""
    message_id = await state.get_data()
    if message.text not in commands:
        message_about = (
            insert(About).values(
                text=message.text
            )
        )
        await session.execute(message_about)
        await session.commit()
        await state.finish()
        await message.delete()
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message_id['message_id']
        )
    else:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text='Вы вводите текст, который cоответствует названию команды. '
                 'Попробуйте ещё раз.')
        await state.finish()


async def change_rules(message: Message, state: FSMContext):
    """Команда для редактирования правил."""
    msg = await message.bot.send_message(
        chat_id=message.from_id,
        parse_mode=ParseMode.HTML,
        text='<i>Введите текст, который будет выводится;\n'
             'Для форматирования используйте '
             '<a href="https://core.telegram.org/bots/api#formatting-options">документацию</a>;\n'
             'Ниже приведены примеры использования тегов из документации:</i>\n'
             '  - <b>bold</b>\n'
             '  - <i>italic</i>\n'
             '  - <u>underline</u>\n'
             '  - <s>strikethrough</s>\n'
             '  - <tg-spoiler>spoiler</tg-spoiler>\n'
             '  - <b>bold <i>italic bold <s>italic bold strikethrough'
             '</s> <u>underline italic bold</u></i> bold</b>'

    )
    await state.update_data(message_id=msg.message_id)
    await RulesState.text.set()


async def record_rules(message: Message, session, state: FSMContext):
    """Запись новой информации о правилах в БД."""
    message_id = await state.get_data()
    if message.text not in commands:
        message_about = (
            insert(Rules).values(
                text=message.text
            )
        )
        await session.execute(message_about)
        await session.commit()
        await state.finish()
        await message.delete()
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message_id['message_id'])
        await state.finish()
    else:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text='Вы вводите текст, который cоответствует названию команды. '
                 'Попробуйте ещё раз.')
        await state.finish()


def register_change_description(dp: Dispatcher):
    dp.register_message_handler(change_about, Command('change_about'), is_admin=True)
    dp.register_message_handler(record_about, state=AboutState.text, is_admin=True)
    dp.register_message_handler(change_rules, Command('change_rules'), is_admin=True)
    dp.register_message_handler(record_rules, state=RulesState.text, is_admin=True)
