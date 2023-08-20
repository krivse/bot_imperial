import asyncio
import logging

import aiohttp
from bs4 import BeautifulSoup

from tgbot.services.db.query import create_or_update_team_table


async def team_table() -> None:
    """
    Еженедельный парсер результирующей таблицы команды
    """
    async with aiohttp.ClientSession() as connect:
        url = 'https://bmfl.ru/team/%d0%b8%d0%bc%d0%bf%d0%b5%d1%80%d0%b8%d0%b0%d0%bb/'

        async with connect.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            data = []
            leagues = list({
                i.text.strip('Состав Империал').upper()
                for i in soup.find_all('h4', class_='sp-table-caption')
                if i.text.startswith('Состав Империал')
            })

            tbody = soup.find_all('tbody')
            for table in range(len(leagues)):
                for position in tbody[table].find_all('tr'):
                    try:
                        player = position.find('td', class_='data-name has-photo').text.strip()
                        url_profile = position.find('td', class_='data-name has-photo').find('a').get('href')
                        role = position.find('td', class_='data-position').text.strip()
                        game = position.find('td', class_='data-appearances').text.strip()
                        goal = position.find('td', class_='data-twofivefoureightfour').text.strip()
                        penalty = position.find('td', class_='data-penalties').text.strip()
                        assist = position.find('td', class_='data-assists').text.strip()
                        goalpen = position.find('td', class_='data-twoonetwosixeight').text.strip()
                        autogoal = position.find('td', class_='data-owngoals').text.strip()
                        yellowcard = position.find('td', class_='data-yellowcards').text.strip()
                        redcard = position.find('td', class_='data-redcards').text.strip()
                        vrt = position.find('td', class_='data-sevenninethreethreefive').text.strip()
                        prg = position.find('td', class_='data-sevenninethreethreefour').text.strip()

                        first_name, last_name, middle_name = player.split()[0], player.split()[1], player.split()[2]

                        async with connect.get(url_profile) as profile:
                            sp = BeautifulSoup(await profile.text(), 'lxml')
                            profile_ = sp.find('div', class_='sp-list-wrapper').find_all('dd')

                            current_club = (
                                'Империал'
                                if profile_[-4].text.strip() in ['НАП', 'ЗАЩ', 'ПЗЩ', 'ВРТ']
                                else profile_[-4].text.strip()
                            )

                            previous_clubs = (
                                '-'
                                if profile_[-3].text.strip() == 'Империал'
                                else profile_[-3].text.strip()
                            )
                            birthday = profile_[-2].text.strip()
                            photo = sp.find(
                                'img',
                                class_='attachment-sportspress-fit-medium size-sportspress-fit-medium wp-post-image'
                            ).get('src')
                            profile_photo = await (await connect.get(photo)).content.read()

                            data.append([
                                leagues[table], first_name, last_name, middle_name,
                                role, game, goal, penalty, assist, goalpen,
                                autogoal, yellowcard, redcard, vrt, prg,
                                current_club, previous_clubs, birthday, profile_photo
                            ])

                    except AttributeError as error:
                        logging.info('Возможные проблемы с доступностью элемента при скрапинге!')
                        logging.error('Исключение при скрапинге', error)

    async_session = getattr(team_table, 'session')
    session = async_session()

    await create_or_update_team_table(data, session)
