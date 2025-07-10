from fastapi import FastAPI
from routes.email_routes import router as email_router
from routes.webhook_routes import router as webhook_router

app = FastAPI()

app.include_router(email_router)
app.include_router(webhook_router)
