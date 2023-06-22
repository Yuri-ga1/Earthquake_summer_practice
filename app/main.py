from pydantic import EmailStr, BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
import os, shutil
import os.path
from datetime import datetime as dt
from . import db_wiring

api = FastAPI()

    
@api.get("/")
async def index():
    return {"Message": "Hello everyone"}
    
@api.post("/create_user")
async def create_user(user_name: str,
                      user_mail: EmailStr):
    os.makedirs(f"app/users/{EmailStr}")
    return {"user_name": user_name,
            "user_mail": user_mail}

@api.post("/users/", response_model=db_wiring.UserOut)
def create_user(user: db_wiring.UserIn, db: db_wiring.Session = db_wiring.Depends(db_wiring.get_db)):
    db_user = db_wiring.get_user_by_email(db, email=user.email)
    if db_user:
        raise db_wiring.HTTPException(status_code=400, detail="Email already registered")
    os.makedirs(f"app/users/{user.email}")
    return db_wiring.create_user_db(db=db, user=user)

@api.post("/upload_files")
async def upload_files(user_mail: EmailStr, user_data: UploadFile):
    if not db_wiring.get_user_by_email:
        return RedirectResponse('/create_user')
    else:
        today = str(dt.now())[:-7].split()
        folder_name = today[0]
        if not os.path.exists(f"app/users/{user_mail}/{folder_name}"):
            os.makedirs(f"app/users/{user_mail}/{folder_name}")
        with open(f"app/users/{user_mail}/{folder_name}/{user_data.filename}", "wb") as buffer:
            shutil.copyfileobj(user_data.file, buffer)
    return {"Message": "Successfull"}



#class UserBase(BaseModel):
#    name: str
#    email: EmailStr
#
#class UserOut(UserBase):
#    pass
#
#class UserIn(UserBase):
#    password: str
#
#
#@api.post("/create_user_from_model", response_model=UserOut)
#async def create_user_from_model(user: UserIn):
#    return user