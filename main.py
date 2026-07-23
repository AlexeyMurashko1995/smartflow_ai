from fastapi import FastAPI
from app.users import router

app = FastAPI(title='Smartflow AI')

app.include_router(router)