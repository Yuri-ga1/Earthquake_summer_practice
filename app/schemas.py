from pydantic import EmailStr, BaseModel
from datetime import datetime as dt

class UserOut(BaseModel):
    email: EmailStr
    class Config:
        orm_mode = True
class UserIn(UserOut):
    password: str
class UserToken(UserIn):
    token: str
    
class Paths(BaseModel):
    email: EmailStr
    date_eq_start: dt
    date_eq_end: dt

    class Config:
        orm_mode = True