import os

from aioEasyPillow import Canvas, Editor, Font


async def show_table_tournament(data):
    """Динамическая обработка данных в изображении."""
    dynamic_string = len(data)
    editor = Editor(Canvas((1310, 37 * dynamic_string), color=('#0d0c0a')))  # #c2c2c2
    logo = Editor(f'{os.path.dirname(os.path.abspath(__file__))}/media/logo/logo.png')
    await logo.resize((1500, 1500))  # (1300, 1300)
    await editor.paste(logo, (-100, -350))  # (10, -140)

    font_cap = Font.montserrat('bold', size=18)
    font = Font.montserrat('italic', size=18)
    header = ['Команда', 'Игры', 'Победы', 'Ничьи', 'Проигрыши', 'Голы', 'Пропущенные', 'Разница', 'Очки']

    await editor.text((50, 20), text=header[0], color=('#bea268'), font=font_cap)
    await editor.text((225, 20), text=header[1], color=('#bea268'), font=font_cap)
    await editor.text((340, 20), text=header[2], color=('#bea268'), font=font_cap)
    await editor.text((480, 20), text=header[3], color=('#bea268'), font=font_cap)
    await editor.text((600, 20), text=header[4], color=('#bea268'), font=font_cap)
    await editor.text((780, 20), text=header[5], color=('#bea268'), font=font_cap)
    await editor.text((890, 20), text=header[6], color=('#bea268'), font=font_cap)
    await editor.text((1090, 20), text=header[7], color=('#bea268'), font=font_cap)
    await editor.text((1230, 20), text=header[8], color=('#bea268'), font=font_cap)
    await editor.rectangle((5, 50), 1300, 0, outline='#bea268', stroke_width=2)
    count = 0
    for ind in range(len(data)):
        count += 30
        await editor.text((20, count + 30), text=data[ind][0], color=('#bea268'), font=font)
        await editor.text((240, count + 30), text=data[ind][1], color=('#bea268'), font=font)
        await editor.text((370, count + 30), text=data[ind][2], color=('#bea268'), font=font)
        await editor.text((505, count + 30), text=data[ind][3], color=('#bea268'), font=font)
        await editor.text((655, count + 30), text=data[ind][4], color=('#bea268'), font=font)
        await editor.text((790, count + 30), text=data[ind][5], color=('#bea268'), font=font)
        await editor.text((950, count + 30), text=data[ind][6], color=('#bea268'), font=font)
        await editor.text((1120, count + 30), text=data[ind][7], color=('#bea268'), font=font)
        await editor.text((1245, count + 30), text=data[ind][8], color=('#bea268'), font=font)

        await editor.rectangle((5, count + 50), 1300, 0, outline='#bea268', stroke_width=1)

    await editor.rectangle((190, 20), 0, 34 * dynamic_string, outline='#bea268', stroke_width=1)
    await editor.rectangle((310, 20), 0, 34 * dynamic_string, outline='#bea268', stroke_width=1)
    await editor.rectangle((450, 20), 0, 34 * dynamic_string, outline='#bea268', stroke_width=1)
    await editor.rectangle((570, 20), 0, 34 * dynamic_string, outline='#bea268', stroke_width=1)
    await editor.rectangle((750, 20), 0, 34 * dynamic_string, outline='#bea268', stroke_width=1)
    await editor.rectangle((860, 20), 0, 34 * dynamic_string, outline='#bea268', stroke_width=1)
    await editor.rectangle((1060, 20), 0, 34 * dynamic_string, outline='#bea268', stroke_width=1)
    await editor.rectangle((1200, 20), 0, 34 * dynamic_string, outline='#bea268', stroke_width=1)

    await editor.save(f'{os.path.dirname(os.path.abspath(__file__))}/media/statistics_tournament/.png')
