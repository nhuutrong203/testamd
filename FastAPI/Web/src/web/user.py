from os import access
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.data.schemas import UserInput, UserOutput
import src.service.user as service
from error import Duplicate, Missing
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter(prefix="/user")


# make a post to /user/token
# (from containing  a username and password)
# and return access token
oauth2_dep = OAuth2PasswordBearer(tokenUrl = "user/token")

def unauthed():
    raise HTTPException(status_code = 401, detail="Incorrect username or password",
                        headers={"WWW-Authenticate": "Bearer"},)

@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get username and password from 0Auth form, return access token"""
    user = service.auth_user(form_data.username, form_data.password)
    if not user or  type(user) is Missing:
        unauthed()
    expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.username}, expires = expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/token")

def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Return the current access token """
    return {"token": token}

### - previous CRUD stuff
@router.get("")
@router.get("/")
def get_all() -> list[UserOutput]:
    return service.get_all()

@router.get("/{name}")
def get_one(name) -> UserOutput:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(user: UserInput) -> UserOutput:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch("/{user_id}")
def modify(user_id: str, user: UserInput) -> UserOutput:
    try:
        return service.modify(user_id, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{user_id}", status_code=204)
def delete(user_id: str):
    try:
        return service.delete(user_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

