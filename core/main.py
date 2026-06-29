from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi_swagger import patch_fastapi
from starlette.exceptions import HTTPException as StarletteHTTPException

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


""" exception handler for get method """
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exp):
    error_handler = {
        "error": True,
        "status_code": exp.status_code,
        "detail": str(exp.detail)
    }
    return JSONResponse(status_code=exp.status_code, content=error_handler)


""" exception handler for post method """
@app.exception_handler(RequestValidationError)
async def http_validation_exception_handler(request, exp):
    error_handler = {
        "error": True,
        "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
        "detaul": "there was a problem with your form request .!",
        "content": exp.errors()
    }
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content=error_handler)


@app.post("/public")
def public_route():
    return {"message":"this is a public route"}

# @app.post("/private")
# def private_route(user:UserModel = Depends(get_authenticated_user)):
#     return {"message":"this is a private route"}

@app.post("/private")
def private_route(user = Depends(get_authenticated_user)):
    return {"message":"this is a private route"}