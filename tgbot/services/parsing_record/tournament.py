import aiohttp
from bs4 import BeautifulSoup

from sqlalchemy import insert, select, delete, func

from tgbot.services.db.models import TournamentTable

def tournament_scheduler(scheduler: object, instance_sess):
    """Создание задачи для турнирной таблицы."""
    setattr(tournament_statistics, 'session', instance_sess)
    scheduler.add_job(
        tournament_statistics,
        # trigger='cron', day_of_week='wed', hour='12'
    )


async def tournament_statistics():
    """
    Еженедельный парсер результирующей таблицы по турниру
    Если таблица не пустая, то сначала происходит её отчистка,
    а после записываются новые данные в таблицу 'TournamentTable'.
    """
    async with aiohttp.ClientSession() as connect:
        url = 'https://bmfl.ru/table/gmfll-5x5-vtd-2022-2023/'
        response = await connect.get(url)
        soup = BeautifulSoup(await response.text(), 'lxml')
        data = []
        table = soup.find('tbody').find_all('tr')

        for position in table:
            team = position.find('td', class_='data-name has-logo').text
            url_team = position.find('td', class_='data-name has-logo').find('a').get('href')
            game = position.find('td', class_='data-p').text
            victory = position.find('td', class_='data-w').text
            draw = position.find('td', class_='data-d').text
            defeat = position.find('td', class_='data-l').text
            goals = position.find('td', class_='data-f').text
            missed = position.find('td', class_='data-a').text
            difference = position.find('td', class_='data-gd').text
            result = position.find('td', class_='data-pts').text

            data.append([
                team, game, victory, draw,
                defeat, goals, missed,
                difference, result, url_team
            ])
            await connect.close()
        print(data)

    async_session = getattr(tournament_statistics, 'session')
    session = async_session()

    result_ = (await session.execute(
        select(func.count(TournamentTable.id)).select_from(TournamentTable))).all()[0][0]
    if result_ < 1:
        await record_to_database(data, session)
    else:
        statement = delete(TournamentTable)
        await session.execute(statement)
        await session.commit()
        await record_to_database(data, session)


async def record_to_database(data, session):
    """Запись в БД."""
    for record in data:
        stmt = (
            insert(TournamentTable).values(
                team=record[0],
                games=int(record[1]),
                victory=int(record[2]),
                draw=int(record[3]),
                defeat=int(record[4]),
                goals=int(record[5]),
                missed=int(record[6]),
                difference=int(record[7]),
                result=int(record[8]),
                url=record[9])
        )
        await session.execute(stmt)
    await session.commit()
    await session.close()
