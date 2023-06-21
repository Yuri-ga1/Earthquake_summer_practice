from pydantic import EmailStr, BaseModel
from fastapi import FastAPI

api = FastAPI()

    
@api.get("/")
async def index():
    return {"Message": "Hello everyone"}

@api.get("/hello")
async def hello(user_name: str | None = None):
    if user_name:
        return {"Message": f"Hello {user_name}"}
    else:
        return {"Message": "Hello anonymous"}
    
@api.post("/create_user")
async def create_user(user_name: str,
                      user_mail: EmailStr):
    return {"user_name": user_name,
            "user_mail": user_mail}


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserOut(UserBase):
    pass

class UserIn(UserBase):
    password: str


@api.post("/create_user_from_model", response_model=UserOut)
async def create_user_from_model(user: UserIn):
    return user

