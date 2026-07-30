from fastapi import FastAPI
from app.users import router as users_router
from app.categories import router as categories_router
from app.expenses import router as expenses_router

app = FastAPI(title='Smartflow AI')

app.include_router(users_router)
app.include_router(categories_router)
app.include_router(expenses_router)