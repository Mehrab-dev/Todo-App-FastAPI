from fastapi import FastAPI
from fastapi_swagger import patch_fastapi

from tasks.routes import router as tasks_routes
from users.routes import router as users_routes


app = FastAPI(docs_url=None,swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app,docs_url="/swagger/")

app.include_router(tasks_routes)
app.include_router(users_routes)