from fastapi import FastAPI
from routers import auth, forecasting

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(forecasting.router, prefix="/forecast", tags=["Forecast"])
