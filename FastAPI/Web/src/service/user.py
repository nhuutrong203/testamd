from error import Missing
from src.data.schemas import UserInput,UserOutput,UserCreate
import src.data.user as data
from datetime import timedelta, datetime, timezone
from jose import jwt
from passlib.context import CryptContext    

SECRET_KEY = "keep-it-secret-keep-it-safe"
ALGORITM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hash:str) -> bool:
    """Hash <plain> and compare with <hash> from the database"""
    return pwd_context.verify(plain, hash)

def get_hash(plain:str) -> str:
    """Return the hash of the <plain> string"""
    return pwd_context.hash(plain)

def get_jwt_username(token:str) -> str | None:
    """Return username from JWT access <token>"""
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITM])
        if not (username := payload.get("sub")):
            return None
    except jwt.JWError:
        return None
    return username

def get_current_user(token:str) -> UserOutput | None:
    """Decade an 0Auth access <token> and return the User"""
    if not (username := get_jwt_username("token")):
            return None
    db_user = lookup_user(username)
    if type(db_user) is Missing:
        return db_user
    if (user:=  db_user):
        return user
    return None

def lookup_user(username: str) -> UserOutput | None:
    """Return a matching User from the database for <name>"""
    db_user = data.get_one(username)
    if type(db_user) is Missing:
        return db_user
    if (user := db_user):
        return user
    return None

def auth_user(username: str, plain:str) -> UserOutput | None:
    """Authenticate user <username> and <plain> password"""
    db_user = lookup_user(username)
    if type(db_user) is Missing:
        return db_user
    if not (user := db_user):
        return None
    if not verify_password(plain, user.hash):
        return None
    return user

def create_access_token(data: dict, expires: timedelta | None = None):
    """Return JWT access token"""
    src = data.copy()
    now = datetime.now(timezone.utc)
    if not expires:
        expires = timedelta(minutes=15)
    src.update({"exp": now + expires})
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITM)
    return encoded_jwt


def get_all() -> list[UserOutput]:
    return data.get_all()

def get_one(username: str) -> UserOutput | None:
    return data.get_one(username)

def create(user: UserInput) -> UserOutput:
    hash_pw = get_hash(user.password)
    createUser =  UserCreate(username = user.username, hash = hash_pw)
    return data.create(createUser)

def replace(user: UserInput) -> UserOutput:
    return data.modify(user)

def modify(user_id: str, user: UserInput) -> UserOutput:
    return data.modify(user_id, user)

def delete(user_id: str) -> bool:
    return data.delete(user_id)
