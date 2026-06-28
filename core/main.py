from fastapi import FastAPI, Depends
from fastapi_swagger import patch_fastapi

from tasks.routes import router as tasks_routes
from users.routes import router as users_routes
from users.models import UserModel
# from auth.basic_auth import get_authenticated_user
# from auth.token_auth import get_authenticated_user
from auth.jwt_auth import get_authenticated_user

app = FastAPI(docs_url=None,swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app,docs_url="/swagger/")

app.include_router(tasks_routes)
app.include_router(users_routes)

@app.post("/public")
def public_route():
    return {"message":"this is a public route"}

# @app.post("/private")
# def private_route(user:UserModel = Depends(get_authenticated_user)):
#     return {"message":"this is a private route"}

@app.post("/private")
def private_route(user = Depends(get_authenticated_user)):
    return {"message":"this is a private route"}