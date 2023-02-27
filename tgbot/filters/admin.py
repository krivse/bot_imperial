import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False
        config: Config = obj.bot.get('config')

        member = await obj.bot.get_chat_member(config.tg_bot.group_ids, obj.from_user.id)

        if (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin:
            return True
        elif member.is_chat_admin() == self.is_admin:
            config.tg_bot.admin_ids.append(member['user']['id'])
            return True
