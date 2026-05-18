from fastapi import FastAPI
from fastapi_swagger import patch_fastapi

from tasks.routes import router as tasks_routes


app = FastAPI(docs_url=None,swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app,docs_url="/swagger/")

app.include_router(tasks_routes)