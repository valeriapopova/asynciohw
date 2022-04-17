import asyncio
import asyncpg
from config import *
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(f'postgresql+asyncpg://{DB_USER}:1@localhost:5432/{DB_NAME}', echo=True)
Base = declarative_base()


class People(Base):

    __tablename__ = 'people'

    id = sq.Column(sq.Integer, primary_key=True)
    birth_year = sq.Column(sq.String(30))
    eye_color = sq.Column(sq.String(30))
    films = sq.Column(sq.String)
    gender = sq.Column(sq.String(100))
    hair_color = sq.Column(sq.String(30))
    height = sq.Column(sq.Integer)
    homeworld = sq.Column(sq.String)
    mass = sq.Column(sq.Integer)
    name = sq.Column(sq.String(100))
    skin_color = sq.Column(sq.String(100))
    species = sq.Column(sq.String())
    starships = sq.Column(sq.String())
    vehicles = sq.Column(sq.String(100))


async def get_async_session(
        drop: bool = False, create: bool = False
):
    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(Base.metadata.drop_all)
        if create:
            print('create table')
            await conn.run_sync(Base.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


async def main():
    await get_async_session(True, True)

if __name__ == '__main__':
    asyncio.run(main())
