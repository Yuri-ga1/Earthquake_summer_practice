from pydantic import EmailStr, BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
import os
from datetime import datetime as dt

api = FastAPI()

    
@api.get("/")
async def index():
    return {"Message": "Hello everyone"}
    
@api.post("/create_user")
async def create_user(user_name: str,
                      user_mail: EmailStr):
    os.mkdir(f"users/{EmailStr}")
    return {"user_name": user_name,
            "user_mail": user_mail}

@api.post("/upload_files")
async def upload_files(user_mail: EmailStr, user_data: UploadFile):
    if "if user doesn't exist":
        return RedirectResponse('/create_user')
    else:
        today = str(dt.now())[:-7].split()
        folder_name = today[0] + "_" + today[1]
        os.mkdir(f"./users/{EmailStr}/{folder_name}")
    with open(f"./users/{EmailStr}/{folder_name}/{user_data.filename}", "wb") as buffer:
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