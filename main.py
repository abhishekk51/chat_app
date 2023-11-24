"""Main app server"""
import asyncio

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from server.managers.mongo_db_manager import MongoDB


class SharedState:
    async_tasks = list()


# Instance of the FastAPI app
app = FastAPI()

# Adding the CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print("Starting up")
    await MongoDB.get_connection()


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down.....")
    await MongoDB.close_connection()
    print('abannndddd')


from server.urls import router as chat

app.include_router(chat, tags=['Chat'], prefix='/api/chat')


@app.get("/api/healthcheck")
def root():
    return {"message": "Working"}
