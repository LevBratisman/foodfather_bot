from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Review, User


async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    user_name: str | None = None,
):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    
    if result.first() is None:
        session.add(User(user_id=user_id, 
                         user_name=user_name))
        await session.commit()
        
        
async def get_all_users_id(session: AsyncSession):
    query = select(User.user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_id_by_user_id(session: AsyncSession, user_id: int):
    query = select(User.id).where(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def get_all_reviews(session: AsyncSession):
    query = select(Review)
    result = await session.execute(query)
    return result.scalars().all() 


async def get_reviews_by_limit(session: AsyncSession, limit: int):
    query = select(Review).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def add_review(session: AsyncSession, user_id: int, text: str):
    session.add(Review(user_id=user_id, text=text))
    await session.commit()