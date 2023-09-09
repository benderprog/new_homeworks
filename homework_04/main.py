"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio
import models
from jsonplaceholder_requests import fetch_posts, fetch_users



async def async_main():
    await models.create_tables()
    users_data, posts_data = await asyncio.gather(
        fetch_users(),
        fetch_posts(),
    )
    await models.add_users_(users_data)
    await models.add_posts_(posts_data)


def main():
    asyncio.run(async_main())

if __name__ == '__main__':
    main()