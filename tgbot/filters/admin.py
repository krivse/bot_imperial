import typing
from aiogram.types import PollAnswer, CallbackQuery
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from tgbot.config import Config
from tgbot.services.db.query import get_all_tournament_table, get_all_users


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False
        config: Config = obj.bot.get('config')

        if type(obj) == PollAnswer:
            user_id = obj.user.id
        else:
            user_id = obj.from_user.id

        member = await obj.bot.get_chat_member(
            config.tg_bot.group_ids,
            user_id
        )

        if (user_id in config.tg_bot.admin_ids) == self.is_admin:
            return True
        elif member.is_chat_admin() == self.is_admin:
            config.tg_bot.admin_ids.append(member['user']['id'])
            return True


class UserFilter(BoundFilter):
    key = 'mode'

    def __init__(self, mode: typing.Optional[str] = None):
        self.mode = mode

    async def check(self, call: CallbackQuery):
        if self.mode is None:
            return False

        data = ctx_data.get()
        session = data.get('session')
        users = await get_all_users(session)

        users_ = []
        if self.mode == 'edit_user':
            for name in users:
                users_.append(f'edit_{name[0]}_{name[1]}')
            if call.data in users_:
                return True
        elif self.mode == 'show_user':
            for name in users:
                users_.append(f'{name[0]}_{name[1]}')
            if call.data in users_:
                return True
        elif self.mode == 'delete_user':
            for name in users:
                users_.append(f'delete_{name[0]}_{name[1]}')
            if call.data in users_:
                return True
        elif self.mode == 'tournament_table':
            tournament_table = await get_all_tournament_table(session)
            for table in tournament_table:
                if call.data in table.replace(' ', '_'):
                    return True
