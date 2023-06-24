from pydantic import EmailStr, BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
import os, shutil
import os.path
from datetime import datetime as dt
from datetime import date as d
from . import db_wiring

api = FastAPI()

#Schema FastAPI
class UserOut(BaseModel):
    email: EmailStr
    class Config:
        orm_mode = True
class UserIn(UserOut):
    password: str
    
class Paths(BaseModel):
    email: EmailStr
    date_upload: d
    

    class Config:
        orm_mode = True

class PathsDates(Paths):
    path: str
    date_eq_start: dt
    date_eq_end: dt

@api.post("/users/", response_model=UserOut)
def create_user(user: UserIn, db: db_wiring.Session = db_wiring.Depends(db_wiring.get_db)):
    db_user = db_wiring.get_user_by_email(db, email=user.email)
    if db_user:
        raise db_wiring.HTTPException(status_code=400, detail="Email already registered")
    os.makedirs(f"app/users/{user.email}")
    return db_wiring.create_user_db(db=db, user=user)


@api.post("/upload_files")
async def upload_files(email: EmailStr, date_eq_start: dt, date_eq_end: dt, file: UploadFile, db: db_wiring.Session = db_wiring.Depends(db_wiring.get_db)):
    if not db_wiring.get_user_by_email(db=db, email=email):
      return RedirectResponse("/users/")
    today = str(dt.now())[:-7].split()
    folder_name = today[0]
    if not os.path.exists(f"app/users/{email}/{folder_name}"):
        os.makedirs(f"app/users/{email}/{folder_name}")
    with open(f"app/users/{email}/{folder_name}/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        db_wiring.create_path_db(db=db, email=email, path=f"app/users/{email}/{folder_name}/{file.filename}", date_upload = folder_name, date_eq_start=date_eq_start, date_eq_end=date_eq_end)
    return {"Message": "Successfull"}

@api.get("/get_files/{email}/{date}")
async def get_files_by_date(email:EmailStr,date: d, db: db_wiring.Session = db_wiring.Depends(db_wiring.get_db)):
    return db_wiring.get_data_by_date(db=db, email=email, date=date)
@api.get("/get_last_upload/{email}")
async def get_last_upload(email:EmailStr, db: db_wiring.Session = db_wiring.Depends(db_wiring.get_db)):
    return db_wiring.get_last_data(db=db, email=email)
    
