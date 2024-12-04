from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
app=FastAPI()
def add_cors_middleware(app: FastAPI):
    cors_origins = os.getenv('CORS_ORIGINS', '').split(',')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS"
        ],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
        ],
    )