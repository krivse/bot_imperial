import os
import asyncio

from aioEasyPillow import Canvas, Editor, Font

data = [
    ['Барков Павел Сергеевич', 'ПЗЩ', '8', '1', '0', '0', '1', '0', '0', '0', '0', '0', 'Империал', 'Космос-Купавна, Посейдон, Работнички, Санта Круз', '14/02/1992', '31', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Барков_Павел.jpg'],
    ['Большаков Евгений Владимирович', 'ПЗЩ', '2', '1', '0', '0', '1', '0', '0', '0', '0', '0', 'Империал', 'Дрим Тим, Дрим Тим-2, Ямайка', '18/03/1997', '25', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Большаков_Евгений.jpg'],
    ['Бурцев Дмитрий Иванович', 'ПЗЩ', '1', '1', '0', '0', '1', '0', '0', '0', '0', '0', 'Империал', 'Арсенал Балашиха, Ураган, Феникс, Феникс-2', '22/02/1992', '31', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Бурцев_Дмитрий.jpg'],
    ['Васильев Виктор Викторович', 'ПЗЩ', '12', '0', '0', '0', '0', '0', '1', '0', '0', '0', 'Империал', 'Дружина Желдор, Олимпик, Работнички, Санта Круз', '13/05/1993', '29', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Васильев_Виктор.jpg'],
    ['Волков Денис Максимович', 'ПЗЩ', '7', '4', '0', '5', '9', '0', '1', '0', '0', '0', 'Империал', 'Спарта Желдор, Спарта Желдор-2', '19/06/2001', '21', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Волков_Денис.jpg'],
    ['Ковалевский Руслан Игоревич', 'ЗАЩ', '12', '5', '0', '3', '8', '0', '2', '0', '0', '0', 'Империал', 'АртМеталл, Здоровая Нация, Здоровая Нация-2, Здоровая Нация-3, Здоровый Регион СД, Сокол, Спарта Желдор, Феникс Железнодорожный, ЧМ', '10/10/1990', '32', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Ковалевский_Руслан.jpg'],
    ['Королев Константин Игоревич', 'НАП', '6', '3', '1', '2', '5', '0', '1', '0', '0', '0', 'Виктория, Империал', 'Спарта', '27/05/1993', '29', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Королев_Константин.jpg'],
    ['Красников Иван Сергеевич', 'ПЗЩ', '5', '0', '0', '1', '1', '0', '0', '1', '3', '8', 'Империал', 'Олимпик, Работнички', '25/07/1992', '30', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Красников_Иван.jpg'],
    ['Малеков Мансур Хаммятович', 'ПЗЩ', '11', '0', '0', '0', '0', '0', '1', '0', '0', '0', 'Империал', 'Сокол, Сокол ЖелДор', '15/02/1997', '26', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Малеков_Мансур.jpg'],
    ['Миюзов Борис Яковлевич', 'ЗАЩ', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'Империал', 'Восточный Легион, Здоровая Нация, Здоровая Нация-2, Здоровая Нация-3, Здоровый Регион СД, Столичный Легион, Феникс Железнодорожный', '01/05/1993', '29', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Миюзов_Борис.jpg'],
    ['Панин Роман Андреевич', 'ПЗЩ', '4', '0', '0', '0', '0', '0', '1', '0', '0', '0', 'Империал', 'Виктория', '14/02/2003', '20', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Панин_Роман.jpg'],
    ['Паньков Алексей Петрович', 'ЗАЩ', '8', '0', '0', '0', '0', '0', '0', '0', '8', '35', 'Империал', 'Восточный Легион, Здоровая Нация, Здоровая Нация-2, Здоровый Регион СД, Столичный, Столичный Легион', '09/08/1984', '38', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Паньков_Алексей.jpg'],
    ['Прокопенко Сергей Константинович', 'ПЗЩ', '5', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'Империал', '-', '09/08/1991', '31', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Прокопенко_Сергей.jpg'],
    ['Проничев Артур Андреевич', 'ЗАЩ', '4', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'Империал', '-', '15/10/1992', '30', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Проничев_Артур.jpg'],
    ['Савин Сергей Сергеевич', 'ПЗЩ', '7', '5', '0', '2', '7', '0', '0', '0', '0', '0', 'Империал', 'Здоровая Нация, Здоровая Нация-2, Здоровая Нация-3, Здоровый Регион СД, Феникс Железнодорожный', '16/10/1983', '39', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Савин_Сергей.jpg'],
    ['Суднов Дмитрий Игоревич', 'ВРТ', '11', '3', '0', '3', '6', '0', '2', '0', '2', '6', 'Империал, Сокол', 'Динамика, Динамика-2, Санта Круз, Сокол ЖелДор', '05/09/1995', '27', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Суднов_Дмитрий.jpg'],
    ['Супрунов Артём Андреевич', 'ПЗЩ', '10', '1', '0', '0', '1', '0', '0', '0', '0', '0', 'Империал', 'Дружина Желдор, Олимпик', '07/04/1992', '30', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Супрунов_Артём.jpg'],
    ['Сухарев Андрей Владимирович', 'ЗАЩ', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'Империал', '-', '24/08/1991', '31', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Сухарев_Андрей.jpg'],
    ['Февралев Андрей Сергеевич', 'ПЗЩ', '5', '0', '0', '0', '0', '0', '1', '0', '0', '0', 'Империал', 'Снеговик, Столичный', '20/11/1991', '31', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Февралев_Андрей.jpg'],
    ['Чайка Ярослав Юрьевич', 'НАП', '9', '1', '0', '0', '1', '0', '0', '0', '0', '0', 'Империал', '-', '05/01/1998', '25', '/Users/esvirk/PycharmProjects/bot_imperial/tgbot/services/pillow/media/player_card/avatar/Чайка_Ярослав.jpg']
]

# data.append([
#                     player, role, games, goals,
#                     penalty, assist, goalpen,
#                     autogoals, yellowcards,
#                     redcards, vrt, prg,
#                     current_club, previous_clubs,
#                     birthday, age, image.name
#                 ])


async def show_table_player(data):
    """
    Динамическая обработка данных в изображении.
    Вставляет аватар и информацию из профиля игрока
    """
    for el in range(len(data)):
        editor = Editor(Canvas((370, 250), color=('#0d0c0a')))  # c2c2c2
        profile = Editor(data[el][16])
        await profile.resize((190, 190))
        await editor.paste(profile)

        font_cap = Font.montserrat('bold', size=10)
        first_name, last_name = data[el][0].split()[0], data[el][0].split()[1]
        await editor.text(
                (200, 20), text=f'{first_name} {last_name}', color=('#bea268'), font=font_cap)
        font_info = Font.montserrat('italic', size=9)
        await editor.text(
            (200, 50), text=f'Позиция:', color=('#bea268'), font=font_info)  # 0C151C
        await editor.text(
            (300, 50), text=data[el][1], color=('#bea268'), font=font_info)
        await editor.text(
            (200, 70), text=f'Возраст:', color=('#bea268'), font=font_info)
        await editor.text(
            (300, 70), text=data[el][15], color=('#bea268'), font=font_info)
        await editor.text(
            (200, 90), text=f'Дата рождения:', color=('#bea268'), font=font_info)
        await editor.text(
            (300, 90), text=data[el][14], color=('#bea268'), font=font_info)
        await editor.text(
            (200, 110), text=f'Текущая команда:', color=('#bea268'), font=font_info)
        current_club = data[el][12].split(', ')
        count = 0
        for i in range(len(current_club)):
            await editor.text(
                 (300, count + 110), text=current_club[i], color=('#bea268'), font=font_info)
            count += 20

        await editor.text((20, 210), text='Игры', align='center', color=('#bea268'), font=font_info)
        await editor.text((20, 230), text=data[el][2], color=('#bea268'), align='center', font=font_info)

        await editor.text((60, 210), text='Голы', align='center', color=('#bea268'), font=font_info)
        await editor.text((60, 230), text=data[el][3], color=('#bea268'), align='center', font=font_info)

        await editor.text((110, 210), text='Пенальти', color=('#bea268'), align='center', font=font_info)
        await editor.text((110, 230), text=data[el][4], color=('#bea268'), align='center', font=font_info)

        await editor.text((170, 210), text='Помощь', color=('#bea268'), align='center', font=font_info)
        await editor.text((170, 230), text=data[el][5], color=('#bea268'), align='center', font=font_info)

        await editor.text((210, 210), text='АГ', color=('#bea268'), align='center', font=font_info)
        await editor.text((210, 230), text=data[el][6], color=('#bea268'), align='center', font=font_info)

        await editor.text((240, 210), text='ЖК', color=('#bea268'), align='center', font=font_info)
        await editor.text((240, 230), text=data[el][7], color=('#bea268'), align='center', font=font_info)

        await editor.text((270, 210), text='КК', color=('#bea268'), align='center', font=font_info)
        await editor.text((270, 230), text=data[el][8], color=('#bea268'), align='center', font=font_info)

        await editor.text((300, 210), text='Врт', color=('#bea268'), align='center', font=font_info)
        await editor.text((300, 230), text=data[el][9], color=('#bea268'), align='center', font=font_info)

        await editor.text((340, 210), text='Пр. голы', color=('#bea268'), align='center', font=font_info)
        await editor.text((340, 230), text=data[el][10], color=('#bea268'), align='center', font=font_info)

        await editor.rectangle((5, 222), 360, 0, outline='#bea268', stroke_width=1)

        await editor.rectangle((40, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((80, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((140, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((198, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((225, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((255, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((285, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((315, 205), 0, 35, outline='#bea268', stroke_width=1)
    # await editor.text(
    #     (200, count + 110), text='Бывшие команды:', color=('#0C151C'), font=font_info)
    # previous_clubs = data[0][13].split(', ')
    # for i in range(len(previous_clubs)):
    #     await editor.text(
    #         (300, count + 110), text=previous_clubs[i], color=('#0C151C'), font=font_info)
    #     count += 20
        await editor.show()
        await editor.save(f'{os.path.dirname(os.path.abspath(__file__))}/media/player_card/{first_name}_{last_name}.png')


# asyncio.run(show_table_player(data))
