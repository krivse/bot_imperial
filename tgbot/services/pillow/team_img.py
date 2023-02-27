import os

from aioEasyPillow import Canvas, Editor, Font


async def show_table_player(data):
    """
    Динамическая обработка данных в изображении.
    Вставляет аватар и информацию из профиля игрока
    """
    for el in range(len(data)):
        editor = Editor(Canvas((370, 250), color=('#0d0c0a')))  # c2c2c2
        profile = Editor(data[el][16])
        logo = Editor(f'{os.path.dirname(os.path.abspath(__file__))}/media/logo/logo.png')
        await profile.resize((190, 190))
        await profile.rounded_corners(radius=2, offset=3)
        await logo.resize((450, 450))  # ((50, 50)) ((700, 700))
        await editor.paste(logo, (35, -50))  # (320, 0)) (35, -50)
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
        await editor.save(
            f'{os.path.dirname(os.path.abspath(__file__))}/media/player_card/{first_name}_{last_name}.png')
