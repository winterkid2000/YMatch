from fastapi import FastAPI
from .database import Base, engine
from .api import ride, match

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(ride.router, prefix="/api")
app.include_router(match.router, prefix="/api")
