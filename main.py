from fastapi import FastAPI
import uvicorn

from routers import users, tasks, auth

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
