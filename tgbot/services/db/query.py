from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import insert, select, func, update, desc, delete
from sqlalchemy.sql import and_, null

from tgbot.services.db.models import About, Poll, Rule, Player, Tournament, TournamentTable, User, UserPoll
from tgbot.services.pillow.team_img import show_table_player
from tgbot.services.pillow.tournament_img import show_table_tournament


async def statistics_publish(session, type_ru='Игра', time_start='02-04-2023', time_end='04-04-2023'):
    result = (await session.execute(
        select(
            User.first_name, User.last_name, User.middle_name, User.role, Poll.time_created, Poll.type
        ).join(
            UserPoll
        ).join(
            Poll
        ).join(
            Player
        ).where(
            and_(
                Poll.type == type_ru)  # , UserPoll.time_created <= time_start, UserPoll.time_created >= time_end)
        ))).all()

    print(result)


# НА УДАЛЕНИЕ
async def clear_tournament_table_5x5(session):
    result = (await session.execute(
        select(
            func.count(
                Tournament.id)
        ).select_from(
            Tournament
        ))).all()[0][0]
    if result > 0:
        await session.execute(delete(Tournament))
        await session.commit()
        return 'Таблица по турниру сброшена'
    else:
        return 'Таблица была сброшена раньше!'


async def get_all_tournament_table(session):
    result = (await session.execute(
        select(
            Tournament.name
        ))).fetchall()
    print(result)

    return result[0]


async def get_tournament_table(session, tournament_id):
    result = (await session.execute(
        select(
            Tournament.name,
            TournamentTable.team, TournamentTable.game, TournamentTable.victory,
            TournamentTable.draw, TournamentTable.defeat, TournamentTable.goal,
            TournamentTable.missed, TournamentTable.difference, TournamentTable.result
        ).join(
            TournamentTable
        ).where(
            TournamentTable.tournament_id == tournament_id
        ))).all()

    await session.close()

    return result


async def get_all_users_for_show_table_player(session):
    result = (await session.execute(
        select(
            User.first_name, User.last_name, User.birthday,
            User.age, User.role, User.current_club, User.avatar,
            Player.game, Player.goal, Player.penalty, Player.assist,
            Player.goalpen, Player.autogoal, Player.yellowcard,
            Player.redcard, Player.vrt, Player.prg
        ).join(
            Player
        ))).all()

    return result


async def get_telegram_id(session, telegram_id):
    result = (await session.execute(
        select(
            User.telegram_id, User.first_name, User.last_name, User.phone
        ).where(
            User.telegram_id == telegram_id
        ))).fetchone()
    return result


async def get_phone(session, phone):
    result = (await session.execute(
        select(
            User.phone, User.first_name, User.last_name
        ).where(
            User.phone == phone
        ))).fetchone()
    return result


async def get_user(session, user):
    result = (await session.execute(
        select(
            User.first_name, User.last_name, User.birthday,
            User.age, User.role, User.current_club, User.avatar,
            Player.game, Player.goal, Player.penalty, Player.assist,
            Player.goalpen, Player.autogoal, Player.yellowcard,
            Player.redcard, Player.vrt, Player.prg
        ).join(
            Player
        ).where(
            User.id == user
        ).union(
            select(
                User.first_name, User.last_name,
                User.birthday, User.age,
                User.role, User.current_club,
                User.avatar,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0
            ).where(
                User.id == user
            )
        ))).fetchone()

    return [result]


async def add_user(session, telegram_id, first_name, last_name, middle_name, birthday, phone, role, photo):
    """Создание нового пользователя."""
    user = (await session.execute(
        select(
            User.first_name,
            User.last_name
        ).filter(
            User.telegram_id == telegram_id)
    )).first()

    if user is None:
        new_user = User(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            birthday=birthday,
            age=time_difference(birthday),
            phone=int(phone),
            role=role,
            avatar=photo
        )
        session.add(new_user)
        # await session.flush()
        # new_player = Player(
        #     user_id=new_user.id,
        #     role=role,
        #     avatar=photo
        # )
        # session.add(new_player)
        await session.commit()
        return f'{new_user.last_name} {new_user.first_name} добавлен в команду Империал!', new_user.id
    else:
        return [f'Пользователь с таким telegram-ID уже записан под именем: {user[1]} {user[0]}']


async def edit_user(session, db_first_name, db_last_name,
                    e_first_name=None,
                    e_last_name=None,
                    e_middle_name=None,
                    e_birthday=None,
                    e_avatar=None,
                    e_role=None,
                    e_telegram_id=None,
                    e_current_club=None,
                    e_phone=None):
    """Частичное обновление пользователя."""
    user = (await session.execute(
        select(
            User
        ).where(
            and_(
                User.first_name == db_first_name,
                User.last_name == db_last_name)
        ))
            ).scalar_one()

    # player = (await session.execute(select(
    #     Player).where(
    #     Player.user_id == user.id)
    # )).scalar_one()

    if e_first_name is not None:
        user.first_name = e_first_name
    elif e_last_name is not None:
        user.last_name = e_last_name
    elif e_middle_name is not None:
        user.middle_name = e_middle_name
    elif e_birthday is not None:
        user.birthday = e_birthday
        user.age = time_difference(e_birthday)
    elif e_avatar is not None:
        user.avatar = e_avatar
    elif e_role is not None:
        user.role = e_role
    elif e_telegram_id is not None:
        user.telegram_id = e_telegram_id
    elif e_phone is not None:
        user.phone = int(e_phone)
    elif e_current_club is not None:
        user.current_club = e_current_club

    await session.commit()

    return user


async def delete_user(session, first_name, last_name):
    await session.execute(
        delete(
            User
        ).where(
            and_(
                User.first_name == first_name,
                User.last_name == last_name
            )
        )
    )
    await session.commit()


async def get_all_users(session):
    """Получение всего списка игроков."""
    result = (await session.execute(
        select(
            User.first_name,
            User.last_name,
            User.middle_name,
            User.birthday,
            User.phone,
            User.telegram_id
        )
    )).all()

    return result


async def create_poll(session_pool, type_ru, message):
    """Регистрация нового опроса."""
    async with session_pool() as session:
        result = Poll(
            type=type_ru,
            poll_id=int(message)
        )

        session.add(result)
        await session.commit()


async def delete_user_poll(session, id_):
    """Удалить запись о голосовании пользователя."""
    await session.execute(
        delete(
            UserPoll
        ).where(
            UserPoll.id == id_[0]))
    await session.commit()


async def exists_polls_users(session, poll_id, user_id):
    """Проверить участия пользователя в опросе."""
    result = (await session.execute(
        select(
            UserPoll.id
        ).where(
            and_(
                UserPoll.poll_id == poll_id,
                UserPoll.user_id == user_id[0])
        ))).first()
    return result


async def create_users_poll(session, user_id, poll_id, option):
    """Проголосовать."""
    stmt = UserPoll(
        user_id=user_id[0],
        poll_id=poll_id,
        answer=option
    )
    session.add(stmt)
    await session.commit()


async def get_poll_id_to_create_a_poll(session, poll_id):
    """Получить poll_id для создания опроса."""
    result = (await session.get(Poll, int(poll_id))).poll_id

    return result


async def get_user_id_to_create_a_poll(session, user_id):
    """Получить user_id для создания опроса."""
    result = (await session.execute(
        select(
            User.id
        ).where(
            User.telegram_id == user_id
        ))).first()

    return result


async def add_a_new_entry_to_about(session, message):
    """Добавить новую запись в таблицу about."""
    result = insert(About).values(text=message)

    await session.execute(result)
    await session.commit()


async def add_a_new_entry_to_rules(session, message):
    """Добавить новую запись в таблицу rules."""
    result = insert(Rule).values(text=message)

    await session.execute(result)
    await session.commit()


async def get_about(session):
    """Получить последнюю запись из таблицы About."""
    result = (await session.execute(
        select(
            About.text
        ).order_by(
            desc(About.id)
        ))).fetchone()
    return result


async def get_rules(session):
    """Получить последнюю запись из таблицы Rules."""
    result = (await session.execute(
        select(
            Rule.text
        ).order_by(
            desc(Rule.id)
        ))).fetchone()

    return result


async def create_or_update_tournament_table(data, session):
    """
    Запись или обновление данных в таблице Tournament.
    Вызов функции обработки изображений show_table_tournament.
    """
    tournament_id = (await session.execute(select(Tournament.id).filter(Tournament.name == data[0][11]))).scalar()
    # (await session.execute(select(func.count(Tournament.id)).select_from(Tournament))).all()[0][0]
    if tournament_id is None:
        new_tournament = Tournament(
            name=data[0][11],
            league=data[0][12],
            division=data[0][13],
            format=data[0][14],
            season=data[0][15],
            organization=data[0][16],
            period=data[0][17]
        )
        session.add(new_tournament)
        await session.flush()
        for team in data:
            new_t_table = TournamentTable(
                tournament_id=new_tournament.id,
                team=team[0],
                game=int(team[1]),
                victory=int(team[2]),
                draw=int(team[3]),
                defeat=int(team[4]),
                goal=int(team[5]),
                missed=int(team[6]),
                difference=int(team[7]),
                result=int(team[8]),
                url_team=team[9],
                logo_team=team[10],
            )
            session.add(new_t_table)
            tournament_id = new_t_table.tournament_id
    else:
        for team in data:
            stmt = update(
                TournamentTable
            ).where(
                TournamentTable.tournament_id == tournament_id,
                TournamentTable.team == team[0]
            ).values(
                game=int(team[1]),
                victory=int(team[2]),
                draw=int(team[3]),
                defeat=int(team[4]),
                goal=int(team[5]),
                missed=int(team[6]),
                difference=int(team[7]),
                result=int(team[8]),
            )
            await session.execute(stmt)

    await session.commit()
    await show_table_tournament(session, tournament_id)


async def create_or_update_team_table(data, session):
    """
    Запись или обновление данных в таблице Player.
    Вызов функции обработки изображений show_table_player.
    """
    for player in data:

        user = (await session.execute(
            select(
                User.id, Tournament.id
            ).where(
                User.first_name == player[2],
                User.last_name == player[1]
            ).join(
                Player, Player.user_id == User.id
            ).join(
                Tournament, Tournament.id == Player.tournament_id
            ).where(
                Tournament.name == player[0]
            ).join(
                TournamentTable, TournamentTable.tournament_id == Tournament.id
            ).where(
                TournamentTable.team == [i for i in player[15].split(', ') if i == 'Империал'].pop()
            ))).fetchone()

        if user is None:
            new_user = (await session.execute(
                select(
                    User.id
                ).where(
                    User.first_name == player[2],
                    User.last_name == player[1]
                ))).fetchone()

            tournament_id = (await session.execute(
                select(
                    Tournament.id
                ).where(
                    Tournament.name == player[0]
                ).join(
                    TournamentTable, TournamentTable.tournament_id == Tournament.id
                ).where(
                    TournamentTable.team == [i for i in player[15].split(', ') if i == 'Империал'].pop()
                ))).scalar()

            if new_user is None:
                new_user = User(
                    last_name=player[1],
                    first_name=player[2],
                    middle_name=player[3],
                    role=player[4],
                    current_club=player[15],
                    previous_clubs=player[16],
                    birthday=player[17],
                    age=time_difference(player[17]),
                    avatar=player[18]
                )
                session.add(new_user)
                await session.flush()

            new_player = Player(
                user_id=new_user.id,
                tournament_id=tournament_id,
                game=int(player[5]),
                goal=int(player[6]),
                penalty=int(player[7]),
                assist=int(player[8]),
                goalpen=int(player[9]),
                autogoal=int(player[10]),
                yellowcard=int(player[11]),
                redcard=int(player[12]),
                vrt=int(player[13]),
                prg=int(player[14]),
            )
            session.add(new_player)
        else:
            stmt = update(
                Player
            ).filter(
                Player.user_id == user[0]
            ).values(
                tournament_id=user[1],
                game=int(player[5]),
                goal=int(player[6]),
                penalty=int(player[7]),
                assist=int(player[8]),
                goalpen=int(player[9]),
                autogoal=int(player[10]),
                yellowcard=int(player[11]),
                redcard=int(player[12]),
                vrt=int(player[13]),
                prg=int(player[14]),
            )
            await session.execute(stmt)
        await session.commit()
    await show_table_player(session)


def time_difference(date):
    """Вычисление возраста игрока."""
    date_of_birth = datetime.strptime(date, '%d/%m/%Y').date()
    current_date = datetime.now().date()

    age = relativedelta(current_date, date_of_birth).years

    return age
