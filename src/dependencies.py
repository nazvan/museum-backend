from db.config import async_session
from uuid import uuid4

async def get_session():
    async with async_session() as session:
        async with session.begin():
            yield session

def uuid():
    return str(uuid4())