import io
import os

from aioEasyPillow import Canvas, Editor, Font
from PIL import Image


async def show_table_player(session, user=None):

    """Выборка данных об игроках и последующая обработка данных в изображении."""
    from tgbot.services.db.query import get_all_users_for_show_table_player, get_user

    if user is None:
        data = await get_all_users_for_show_table_player(session)
    else:
        data = await get_user(session, user)
    await session.close()

    for el in range(len(data)):
        editor = Editor(Canvas((412, 250), color=('#0d0c0a')))  # c2c2c2
        profile_photo_bytes = data[el][6]
        profile = Editor(Image.open(io.BytesIO(profile_photo_bytes)))
        logo = Editor(f'{os.path.dirname(os.path.abspath(__file__))}/media/logo/logo.png')
        await profile.resize((190, 190))
        await profile.rounded_corners(radius=2, offset=3)
        await logo.resize((450, 450))  # ((50, 50)) ((700, 700))
        await editor.paste(logo, (35, -50))  # (320, 0)) (35, -50)
        await editor.paste(profile)

        font_cap = Font.montserrat('bold', size=15)

        first_name, last_name = data[el][0], data[el][1]
        await editor.text(
            (200, 20), text=f'{first_name} {last_name}', color=('#bea268'), font=font_cap)
        font_info = Font.montserrat('regular', size=12)  # italic

        role = data[el][4]
        await editor.text(
            (200, 50), text=f'Позиция:', color=('#bea268'), font=font_info)  # 0C151C
        await editor.text(
            (318, 50), text=role, color=('#bea268'), font=font_info)

        age = str(data[el][3])
        await editor.text(
            (200, 70), text=f'Возраст:', color=('#bea268'), font=font_info)
        await editor.text(
            (318, 70), text=age, color=('#bea268'), font=font_info)

        birthday = data[el][2]
        await editor.text(
            (200, 90), text=f'Дата рождения:', color=('#bea268'), font=font_info)
        await editor.text(
            (318, 87), text=birthday, color=('#bea268'), font=font_info)

        current_club = data[el][5].split(', ')
        await editor.text(
            (200, 110), text=f'Текущая команда:', color=('#bea268'), font=font_info)
        count = 0
        for i in range(len(current_club)):
            await editor.text(
                (318, count + 110), text=current_club[i], color=('#bea268'), font=font_info)
            count += 20

        game = str(data[el][7])
        await editor.text((20, 210), text='Игры', align='center', color=('#bea268'), font=font_info)
        await editor.text((20, 230), text=game, color=('#bea268'), align='center', font=font_info)

        goal = str(data[el][8])
        await editor.text((60, 210), text='Голы', align='center', color=('#bea268'), font=font_info)
        await editor.text((60, 230), text=goal, color=('#bea268'), align='center', font=font_info)

        penalty = str(data[el][9])
        await editor.text((115, 210), text='Пенальти', color=('#bea268'), align='center', font=font_info)
        await editor.text((115, 230), text=penalty, color=('#bea268'), align='center', font=font_info)

        assist = str(data[el][10])
        await editor.text((179, 210), text='Помощь', color=('#bea268'), align='center', font=font_info)
        await editor.text((179, 230), text=assist, color=('#bea268'), align='center', font=font_info)

        goalpen = str(data[el][11])
        await editor.text((224, 210), text='Г+П', color=('#bea268'), align='center', font=font_info)
        await editor.text((224, 230), text=goalpen, color=('#bea268'), align='center', font=font_info)

        autogoal = str(data[el][12])
        await editor.text((252, 210), text='АГ', color=('#bea268'), align='center', font=font_info)
        await editor.text((252, 230), text=autogoal, color=('#bea268'), align='center', font=font_info)

        yellowcard = str(data[el][13])
        await editor.text((279, 210), text='ЖК', color=('#bea268'), align='center', font=font_info)
        await editor.text((279, 230), text=yellowcard, color=('#bea268'), align='center', font=font_info)

        redcard = str(data[el][14])
        await editor.text((306, 210), text='КК', color=('#bea268'), align='center', font=font_info)
        await editor.text((306, 230), text=redcard, color=('#bea268'), align='center', font=font_info)

        vrt = str(data[el][15])
        await editor.text((334, 210), text='Врт', color=('#bea268'), align='center', font=font_info)
        await editor.text((334, 230), text=vrt, color=('#bea268'), align='center', font=font_info)

        prg = str(data[el][16])
        await editor.text((381, 210), text='Пр. голы', color=('#bea268'), align='center', font=font_info)
        await editor.text((381, 230), text=prg, color=('#bea268'), align='center', font=font_info)

        await editor.rectangle((3, 222), 404, 0, outline='#bea268', stroke_width=1)

        await editor.rectangle((40, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((80, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((148, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((208, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((239, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((264, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((294, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((318, 205), 0, 35, outline='#bea268', stroke_width=1)
        await editor.rectangle((349, 205), 0, 35, outline='#bea268', stroke_width=1)
        # await editor.text(
        #     (200, count + 110), text='Бывшие команды:', color=('#0C151C'), font=font_info)
        # previous_clubs = data[0][13].split(', ')
        # for i in range(len(previous_clubs)):
        #     await editor.text(
        #         (300, count + 110), text=previous_clubs[i], color=('#0C151C'), font=font_info)
        #     count += 20
        await editor.save(
            f'{os.path.dirname(os.path.abspath(__file__))}/media/player_card/{first_name}_{last_name}.png')
