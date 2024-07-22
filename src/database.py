from sqlalchemy.ext.asyncio import create_async_engine, async_session
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from config import settings
import asyncio

engine = create_engine(
	url=settings.DATABASE_URL_psycopg,
	echo=True, # для отображения запросов в консоли
	pool_size=5, # задает количество подключений к бд
	max_overflow=10, # задает максимальное количество подключений к бд
) # подключение к бд всегда происходит через engine

# engin имеет два метода для создания транзакций connect() и begin()
# если необходимо что бы после завершения работы автоматически
# применялась функция commit() нужно использовать метод begin()
with engine.connect() as conn:
	# sqlalchemy работает с запросами только через функцию text 
	res = conn.execute(text("SELECT VERSION()"))
	print(f"{res.first()[0]}") 

# асинхронное подключение к бд
async_engine = create_async_engine(
	url=settings.DATABASE_URL_asyncpg,
	echo=False,
	pool_size=5, # задает количество подключений к бд
	max_overflow=10,
)
# асинхронный код можно писать только в асинхронной функции
async def get_execute():
	async with async_engine.connect() as conn:
		res = await conn.execute(text("SELECT VERSION()"))
		print(res.first())


asyncio.run(get_execute())