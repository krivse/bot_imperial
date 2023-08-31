from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.keyboards.other import cancel
from tgbot.misc.states import AboutState, RulesState
from tgbot.services.db.query import add_a_new_entry_to_about, add_a_new_entry_to_rules
from tgbot.services.set_commands import commands


async def change_about(message: Message, state: FSMContext):
    """Команда для редактирования описания."""
    msg = await message.bot.send_message(
        chat_id=message.from_id,
        text='Введите текст, который будет выводится;\n'
             'Для форматирования используйте '
             '<a href="https://core.telegram.org/bots/api#formatting-options">документацию</a>;\n'
             'Ниже приведены примеры использования тегов из документации:\n'
             f'{hcode("<b>bold</b>")} - <b>bold</b>\n'
             f'{hcode("<i>italic</i>")} - <i>italic</i>\n' 
             f'{hcode("<u>underline</u>")} - <u>underline</u>\n'
             f'{hcode("<s>strikethrough</s>")} - <s>strikethrough</s>\n'
             f'{hcode("<tg-spoiler>spoiler</tg-spoiler>")} - <tg-spoiler>spoiler</tg-spoiler>\n'
             f'{hcode("<b>bold <i>italic bold <s>italic bold strikethrough")} '
             f'- <b>bold <i>italic bold <s>italic bold strikethrough\n'
             f'{hcode("</s> <u>underline italic bold</u></i> bold</b>")} '
             f'- </s> <u>underline italic bold</u></i> bold</b>',
        reply_markup=cancel
    )
    await state.update_data(message_id_about=msg.message_id)
    await AboutState.text.set()


async def record_about(message: Message, session, state: FSMContext):
    """Запись новой информации о команде в БД."""
    message_id = await state.get_data()

    if message.text not in commands:
        await add_a_new_entry_to_about(session, message.text)
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message_id.get('message_id_about'),
        )
        await state.finish()
    else:
        cancel_id_message_about = await message.bot.send_message(
            chat_id=message.chat.id,
            text='Вы вводите текст, который cоответствует названию команды бота. '
                 'Попробуйте ещё раз..',
            reply_markup=cancel
        )
        await state.update_data(cancel_id_message_about=cancel_id_message_about.message_id)


async def change_rules(message: Message, state: FSMContext):
    """Команда для редактирования правил."""
    msg = await message.bot.send_message(
        chat_id=message.from_id,
        text='Введите текст, который будет выводится;\n'
             'Для форматирования используйте '
             '<a href="https://core.telegram.org/bots/api#formatting-options">документацию</a>;\n'
             'Ниже приведены примеры использования тегов из документации:\n'
             f'{hcode("<b>bold</b>")} - <b>bold</b>\n'
             f'{hcode("<i>italic</i>")} - <i>italic</i>\n' 
             f'{hcode("<u>underline</u>")} - <u>underline</u>\n'
             f'{hcode("<s>strikethrough</s>")} - <s>strikethrough</s>\n'
             f'{hcode("<tg-spoiler>spoiler</tg-spoiler>")} - <tg-spoiler>spoiler</tg-spoiler>\n'
             f'{hcode("<b>bold <i>italic bold <s>italic bold strikethrough")} '
             f'- <b>bold <i>italic bold <s>italic bold strikethrough\n'
             f'{hcode("</s> <u>underline italic bold</u></i> bold</b>")} '
             f'- </s> <u>underline italic bold</u></i> bold</b>',
        reply_markup=cancel
    )
    await state.update_data(message_id_rules=msg.message_id)
    await RulesState.text.set()


async def record_rules(message: Message, session, state: FSMContext):
    """Запись новой информации о правилах в БД."""
    message_id = await state.get_data()

    if message.text not in commands:
        await add_a_new_entry_to_rules(session, message.text)
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message_id.get('message_id_rules'))
        await state.finish()
    else:
        cancel_id_message_rules = await message.bot.send_message(
            chat_id=message.chat.id,
            text='Вы вводите текст, который cоответствует названию команды бота. '
                 'Попробуйте ещё раз..',
            reply_markup=cancel
        )
        await state.update_data(cancel_id_message_rules=cancel_id_message_rules.message_id)


async def cancel_about_or_rules(call: CallbackQuery, state: FSMContext):
    """Отмена редактирования описания / правил команды."""
    message = await state.get_data()

    if message.get('cancel_id_message_about'):
        await call.message.bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=message.get('cancel_id_message_about')
        )
        if message.get('message_id_about'):
            await call.message.bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=message.get('message_id_about')
            )
    elif message.get('message_id_about'):
        await call.message.bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=message.get('message_id_about')
        )
    elif message.get('cancel_id_message_rules'):
        await call.message.bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=message.get('cancel_id_message_rules')
        )
        if message.get('message_id_rules'):
            await call.message.bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=message.get('message_id_rules')
            )
    elif message.get('message_id_rules'):
        await call.message.bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=message.get('message_id_rules')
        )

    await state.finish()


def register_change_description_admin(dp: Dispatcher):
    dp.register_message_handler(change_about, Command('change_about'), is_admin=True)
    dp.register_message_handler(record_about, state=AboutState.text)
    dp.register_message_handler(change_rules, Command('change_rules'), is_admin=True)
    dp.register_message_handler(record_rules, state=RulesState.text)
    dp.register_callback_query_handler(cancel_about_or_rules, text='cancel_description', state='*')
