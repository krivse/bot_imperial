import aiohttp
from bs4 import BeautifulSoup
from aiocsv import AsyncWriter
import aiofiles
import os


async def tournament_statistics():
    """Еженедельный парсер результирующей таблицы по турниру."""
    async with aiohttp.ClientSession() as session:
        url = 'https://bmfl.ru/table/gmfll-5x5-vtd-2022-2023/'
        response = await session.get(url)
        soup = BeautifulSoup(await response.text(), 'lxml')
        data = []
        table = soup.find('tbody').find_all('tr')

        for position in table:
            number = position.find('td', class_="data-rank").text
            team = position.find('td', class_='data-name has-logo').text
            url_team = position.find('td', class_='data-name has-logo').find('a').get('href')
            game = position.find('td', class_='data-p').text
            victory = position.find('td', class_='data-w').text
            draw = position.find('td', class_='data-d').text
            defeat = position.find('td', class_='data-l').text
            goals = position.find('td', class_='data-f').text
            missed = position.find('td', class_='data-a').text
            plus_minus = position.find('td', class_='data-gd').text
            result = position.find('td', class_='data-pts').text

            data.append([
                number, team, game,
                victory, draw, defeat, goals,
                missed, plus_minus, result, url_team
            ])

    async with aiofiles.open(
            f'{os.path.dirname(os.path.abspath(__file__))}/data_pars/table_data.csv',
            'w', encoding='utf-8') as file:
        header = ['№', 'Команда', 'И', 'В', 'Н', 'П', 'Г', 'Пр', '+/-', 'О', 'Ссылка']
        writer = AsyncWriter(file)
        await writer.writerow(header)
        await writer.writerows(data)
