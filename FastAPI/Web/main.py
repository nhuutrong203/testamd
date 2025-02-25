import uvicorn
from fastapi import FastAPI
from src.data.init import create_tables
from src.web import explorer, creature, user
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

create_tables()

app.include_router(explorer.router, tags=["Explorer"])
app.include_router(creature.router, tags=["Creature"])
app.include_router(user.router,tags=["User"])

if __name__ == "__main__":
    # import uvicorn
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port = 8000)