import asyncio

import aiohttp
from bs4 import BeautifulSoup

from tgbot.services.db.query import create_or_update_tournament_table


DIVISIONS = [
    '1Д', '2Д', '3Д',
    'ВД', 'ПД', 'ВТД', 'ТД', 'ЧД',
    'НОЧЬ',
    'ГРУППА А', 'ГРУППА Б', 'ГРУППА В',
    'ДИВИЗИОН 1', 'ДИВИЗИОН 2', 'ДИВИЗИОН 3', 'ПЛЭЙ-ОФФ',
    'ЮГ', 'СЕВЕР', 'ЦЕНТР', 'ВОСТОК', 'ЗАПАД',
]
FORMAT = [
    '5Х5', '6Х6', '7Х7', '8Х8', '11Х11'
]
LEAGUE = [
    'БМФЛЛ', 'ЖМФЛЛ', 'МЛФЛ', 'МФЛЛНР', 'ЭМФЛЛ', 'СУПЕРЛИГА'
]


async def tournament_statistics() -> None:
    """
    Еженедельный парсер результирующей таблицы по турниру
    Если таблица не пустая, то сначала происходит её отчистка,
    а после записываются новые данные в таблицу 'TournamentTable'.
    """
    async with aiohttp.ClientSession() as connect:
        url = 'https://bmfl.ru/table/bmfll-8x8-3d-2023/'

        async with connect.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            data = []

            table_caption = soup.find('title').text
            title = table_caption.strip('ТАБЛИЦА').strip(' — ОПЛ').upper()
            league = [i for i in table_caption.split() if i in LEAGUE].pop()
            division = [i for i in table_caption.split() if i in DIVISIONS].pop()
            format_ = [i for i in table_caption.split() if i in FORMAT].pop()
            organization = table_caption.split().pop(-1)
            period = table_caption.split().pop(-3)
            season = 'Зима' if len(period.split('/')) == 2 else 'Лето'

            table = soup.find('tbody').find_all('tr')
            for position in table:
                team = position.find('td', class_='data-name has-logo').text.strip()
                url_team = position.find('td', class_='data-name has-logo').find('a').get('href')
                logo_t = position.find(
                    'img', class_='attachment-sportspress-fit-icon size-sportspress-fit-icon wp-post-image').get('src')
                game = position.find('td', class_='data-p').text.strip()
                victory = position.find('td', class_='data-w').text.strip()
                draw = position.find('td', class_='data-d').text.strip()
                defeat = position.find('td', class_='data-l').text.strip()
                goal = position.find('td', class_='data-f').text.strip()
                missed = position.find('td', class_='data-a').text.strip()
                difference = position.find('td', class_='data-gd').text.strip()
                result = position.find('td', class_='data-pts').text.strip()

                logo_team = await (await connect.get(logo_t)).content.read()

                data.append([
                    team, game, victory,
                    draw, defeat, goal,
                    missed, difference,
                    result, url_team, logo_team,
                    title, league, division, format_,
                    season, organization, period
                ])

    async_session = getattr(tournament_statistics, 'session')
    session = async_session()
    await create_or_update_tournament_table(data, session)
