import aiohttp
from bs4 import BeautifulSoup

from sqlalchemy import insert, select, delete, func

from tgbot.services.db.models import Team


def team_scheduler(scheduler: object, instance_sess):
    """Создание задачи для таблицы команды."""
    setattr(team_table, 'session', instance_sess)
    scheduler.add_job(
        team_table,
        trigger='cron', day_of_week='wed', hour='12'
    )


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
            # number = position.find('td', class_="data-rank").text
            gamer = position.find('td', class_='data-name has-photo').text
            url_photo = position.find('td', class_='data-name has-photo').find('a').get('href')
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

            data.append([
                gamer, role, games, goals,
                penalty, assist, goalpen,
                autogoals, yellowcards,
                redcards, vrt, prg, url_photo
            ])
            await connect.close()

    async_session = getattr(team_table, 'session')
    session = async_session()

    result_ = (await session.execute(
        select(func.count(Team.id)).select_from(Team))).all()[0][0]
    if result_ < 1:
        await record_to_database(data, session)
    else:
        statement = delete(Team)
        await session.execute(statement)
        await session.commit()
        await record_to_database(data, session)


async def record_to_database(data, session):
    """Запись в БД."""
    for record in data:
        stmt = (
            insert(Team).values(
                gamer=record[0],
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
                url_photo=record[12])
        )
        await session.execute(stmt)
    await session.commit()
    await session.close()
