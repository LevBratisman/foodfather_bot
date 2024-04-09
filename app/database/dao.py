from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User


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