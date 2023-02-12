from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class CallbackMiddlware(BaseMiddleware):
    async def on_pre_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        """
        Убрать отображение часов при попыптке нажимать на кнопку
        Для предобработке поступающего запроса. Без необходимости прописывать его в хендлере.
        """
        pass
        await cq.answer()
    #
    # async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
    #     pass
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
import logging


# class CallbackMiddlware(BaseMiddleware):
#     # Ждём апдейт, прокидывание данных между цепочками можно сделать с помощью аргумента data
#     # Передаваемые данные соответсвуют типу апдейта, например, pre_process_update - process_update
#     # 1 point
#     async def on_pre_process_update(self, update: types.Update, data: dict):
#         logging.info('[----Новый апдейт----]')
#         logging.info('1. Pre Process Update')
#         logging.info('Следующая точка: Process Update')
#         data['middleware_data'] = 'Это пройдет до on_post_process_update'
#         # Можно на этом этапе в бд посмотреть список забаненных пользователей, что их передать,
#         # и не хранить данные в .env
#         banned_user_test = [123412, 4124124]
#         if update.message:
#             user = update.message.from_user.id
#         elif update.callback_query:
#             user = update.callback_query.from_user.id
#         else:
#             return
#         if user in banned_user_test:
#             raise CancelHandler()  # Прекращает обработка апдейта
#
#     # 2 point
#     async def on_process_update(self, updage:types.Update, data: dict):
#         logging.info(f'2. Process Update, {data}')
#         logging.info('Следующая точка: Pre Process Message')
#
#     # 3 point
#     async def on_pre_process_message(self, message: types.Message, data: dict):
#         # Данные в этом типе будут уже другие
#         logging.info(f'3. Pre Process Message, {data=}')
#         logging.info('Следующая точка: Filters')
#         data['middleware_data'] = 'Это пройдет в on_process_message'
#
#     # 4 point из папки filter
#
#     # 5 point
#     async def on_process_message(self, message: types.Message, data: dict):
#         logging.info(f'5. Procces Message')
#         logging.info(f'Следующая точка: Handler')
#         data['middleware_data'] = 'Это попадет в хендлер'
#         # Если я передам это ключ из middleware в хендлер,
#         # аргумент: middleware_data в ручную, то эти данные туда попадут.
#
#     # 6 point из папки handler
#     # 7
#     async def on_post_process_message(self, message: types.Message, data_from_filter: list, data: dict):
#         logging.info(f'7. Post Process Message, {data=}, {data_from_filter=}')
#         logging.info('Следующая точка: Post Process Update')
#
#     # 8
#     async def on_post_process_update(self, update: types.Update, data_from_handler: list, data: dict):
#         # Сюда можно передать апдейты из хендлера тоже
#         logging.info(f'8. Post Process Update, {data=}, {data_from_handler}')
#         logging.info(f'----------Выход----------')
#
#     async def on_pre_process_callback_query(self, cq: types.CallbackQuery, data: dict):
#         # Убрать отображение часов при попыптке нажимать на кнопку
#         # Для предобработке поступающего запроса. Без необходимости прописывать его в хендлере
#         await cq.answer()
