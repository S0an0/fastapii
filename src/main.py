from fastapi import FastAPI
import uvicorn
from src.api import UserRouters , TaskRouters, AssociationTU,AuthRouters
from src.database import engine, Base
import asyncio

app = FastAPI()

app.include_router(UserRouters)
app.include_router(TaskRouters)
app.include_router(AssociationTU)
app.include_router(AuthRouters)

async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("database create")
    return

if __name__=="__main__":
    asyncio.run(setup_database())
    
    uvicorn.run(
        "src.main:app",
        reload = True
        )

