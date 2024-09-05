from fastapi import FastAPI

from routers import users_router

app = FastAPI()
app.include_router(users_router)


if __name__ == "__main__":
    from uvicorn import run
    run("main:app", host="0.0.0.0", port=8000)
