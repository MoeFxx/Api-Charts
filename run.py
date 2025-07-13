from fastapi import FastAPI

from price_svc.api import price_app
from chart_svc.app import chart_app

app = FastAPI(title="api")
app.include_router(price_app.router)
app.include_router(chart_app.router)

__all__ = ["app"]
