#init.py
from database import engine
from models import Base
# * this is to make sure the tables are there at the start of the program
# * also it is asynchronous because the engine itself is
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)