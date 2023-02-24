import pathlib

import aiohttp
from bs4 import BeautifulSoup
import asyncio
import aiofiles

from sqlalchemy import insert, select, delete, func

from tgbot.services.db.models import Team
from tgbot.services.pillow.team_img import show_table_player


async def team_table():
    """
    Еженедельный парсер результирующей таблицы по команде
    Если таблица не пустая, то сначала происходит её отчистка,
    а после записываются новые данные в таблицу 'TournamentTable'.
    """
    async with aiohttp.ClientSession() as connect:
        url = 'https://bmfl.ru/team/%d0%b8%d0%bc%d0%bf%d0%b5%d1%80%d0%b8%d0%b0%d0%bb/'
        response = await connect.get(url)
        soup = BeautifulSoup(await response.text(), 'lxml')
        data = []
        table = soup.find('tbody').find_all('tr')
        for position in table:
            player = position.find('td', class_='data-name has-photo').text
            url_profile = position.find('td', class_='data-name has-photo').find('a').get('href')
            role = position.find('td', class_='data-position').text
            games = position.find('td', class_='data-appearances').text
            goals = position.find('td', class_='data-twofivefoureightfour').text
            penalty = position.find('td', class_='data-penalties').text
            assist = position.find('td', class_='data-assists').text
            goalpen = position.find('td', class_='data-twoonetwosixeight').text
            autogoals = position.find('td', class_='data-owngoals').text
            yellowcards = position.find('td', class_='data-yellowcards').text
            redcards = position.find('td', class_='data-redcards').text
            vrt = position.find('td', class_='data-sevenninethreethreefive').text
            prg = position.find('td', class_='data-sevenninethreethreefour').text

            profile = await connect.get(url_profile)
            sp = BeautifulSoup(await profile.text(), 'lxml')
            profile_ = sp.find('div', class_='sp-list-wrapper').find_all('dd')
            current_club = 'Империал' if profile_[-4].text in ['НАП', 'ЗАЩ', 'ПЗЩ', 'ВРТ'] else profile_[-4].text
            previous_clubs = '-' if profile_[-3].text == 'Империал' else profile_[-3].text
            birthday = profile_[-2].text
            age = profile_[-1].text
            photo = sp.find(
                 'img',
                class_='attachment-sportspress-fit-medium size-sportspress-fit-medium wp-post-image'
            ).get('src')
            profile_photo = await connect.get(photo)
            first_name, last_name = player.split()[0], player.split()[1]
            image = await aiofiles.open(
                pathlib.Path.cwd()/'tgbot/services/pillow/media/player_card/avatar/'
                f'{first_name}_{last_name }.jpg', mode='wb')
            await image.write(await profile_photo.read())
            await image.close()

            data.append([
                    player, role, games, goals,
                    penalty, assist, goalpen,
                    autogoals, yellowcards,
                    redcards, vrt, prg,
                    current_club, previous_clubs,
                    birthday, age, image.name
                ])
            profile.close()
            response.close()
        await connect.close()
    print(data)
    async_session = getattr(team_table, 'session')
    session = async_session()

    result_ = (await session.execute(
        select(func.count(Team.id)).select_from(Team))).all()[0][0]
    if result_ < 1:
        await record_to_database(data, session)
        await show_table_player(data)
    else:
        statement = delete(Team)
        await session.execute(statement)
        await session.commit()
        await record_to_database(data, session)
        await show_table_player(data)


async def record_to_database(data, session):
    """Запись в БД."""
    for record in data:
        stmt = (
            insert(Team).values(
                player=record[0],
                role=record[1],
                games=int(record[2]),
                goals=int(record[3]),
                penalty=int(record[4]),
                assist=int(record[5]),
                goalpen=int(record[6]),
                autogoals=int(record[7]),
                yellowcards=int(record[8]),
                redcards=int(record[9]),
                vrt=int(record[10]),
                prg=int(record[11]),
                current_club=record[12],
                previous_clubs=record[13],
                birthday=record[14],
                age=int(record[15])
            )
        )
        await session.execute(stmt)
    await session.commit()
    await session.close()
