from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import query, schema, feedback
import os

app = FastAPI(title="SageQuery API", version="1.0.0")

origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(schema.router, prefix="/schema", tags=["Schema"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])

@app.get("/")
def root():
    return {"message": "Welcome to SageQuery API"} 