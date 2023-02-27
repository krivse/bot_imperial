### Асинхронный (aiogram) Телеграм-бот для футбольного клуба "Империал", который будет автоматизицировать рутинные процессы, такие как создание голосований, оплата спортивных мероприятий, отображение статистики по играм, игрокам и др. 
#### Для работы используются только асинхронные библиотеки или модули: asyncpg, AsyncIOScheduler, aioredis, aioEasyPillow

#### Первый этап (завершен)
```
1. Созданы команды для администратора:
   - редактирование общих команд (c помощью БД): изменеие описания, правил;
   - планировщик событий на требуемый период, тип: "Голосования" (apscheduler, aigoram-calendar, redis):
     - Функциональность:
       - Создание, изменение, удаление;
       - 3 вида событий (Игра, Тренировка, Тренировка 2);
       - Поля для создания: описание, день, дата начала, дата конца;
       - Изменение происходит по принципу создания;
       - Удаление по типу выбранного события;
       - Ограничение на выбор при создании, изменении или удалении, если был затронут данный тип события;
2. Созданы пользовательские обработчики команд: описание, правила, статистика матчей, статистика игроков;
3. Парсер для сбора данных из турнирной таблицы (bs4, aiohtttp), хранятся в csv - позже в БД.
```
#### Второй этап
```
1. Подключена бд, созданы 2 таблицы (Турнирная таблица, Команда) проведеы миграции(PostgreSQL, Alembic);
2. Доработан парсер для таблицы "Турнирная таблица", реализована запись в бд;
3. Создан парсер для таблицы "Команда", реализована запись в бд;
4. Настроен мидлваре для передачи сессии бд в хендлеры и их закрытие после записи.
```
#### Третий этап
```
1. Парсер передает данные из парсера в pillow для генерации изображения с актуальной информацией об игроке, команды;
2. Команда /statistic отправляет пользователю изображение с общей статисткой о команде в турнире;
3. Команда /team отправляет пользователю изображение с статистикой об игроке.
```
#### Четвертый этап
```
1. Создание двух таблиц в бд: Описание, Правила;
2. Редактирование команд (Изменить описание, Изменить правила) с помощью бд;
3. Отладка команд бота.
4. Настройка dockerfile, docker-compose
```
#### Следующий этап
```
- Деплой на удалённый сервер (Docker);
- Тестовый запуск.
``` 

###### Ivan Krasnikov
