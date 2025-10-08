from fastapi import FastAPI
import uvicorn

from app.routers import auth, users, tasks

app = FastAPI()

# Register API routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)


if __name__ == "__main__":
    # Run the FastAPI app with auto-reload enabled
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
