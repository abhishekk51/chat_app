"""Main app server"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from server.managers.mongo_db_manager import MongoDB

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
async def shutdown_event(background_tasks: BackgroundTasks):
    print("Shutting down")
    await MongoDB.close_connection()
    for task in background_tasks.tasks:
        print(task, 'taskkkkkkkkkkkkkk')
        task.cancel()


from server.urls import router as chat

app.include_router(chat, tags=['Chat'], prefix='/api/chat')


@app.get("/api/healthcheck")
def root():
    return {"message": "Working"}
