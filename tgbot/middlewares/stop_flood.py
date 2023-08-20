from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, Update
from aiogram.dispatcher.handler import CancelHandler


class CheckFlood(BaseMiddleware):
    async def on_pre_process_update(self, update: Update, data: dict):
        if isinstance(update.message, Message) and update.message.chat.type in ["group", "supergroup"]:
            commands = [
                '/start',
                '/team',
                '/about',
                '/rules',
                '/tournament_table',
            ]
            admin_commands = [
                'user_manager',
                '/users',
                '/change_about',
                '/change_rules',
                '/task_scheduler'
            ]
            text = update.message.text.split('@')[0]
            if text not in commands and update.message.from_user.id not in update.bot.get('config').tg_bot.admin_ids:
                await update.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
                await update.bot.send_message(
                    chat_id=update.message.from_user.id,
                    text='В групповом чате разрешено использование только команд')
                # Прекращение обработки апдейта
                raise CancelHandler()
            elif text in admin_commands and update.message.from_user.id in update.bot.get('config').tg_bot.admin_ids:
                await update.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
                await update.bot.send_message(
                    chat_id=update.message.from_user.id,
                    text='В групповом чате разрешено использование только общих команд')
                raise CancelHandler()

    async def on_process_message(self, message: Message, data: dict):
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
