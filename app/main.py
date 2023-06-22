from pydantic import EmailStr, BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
import os, shutil
import os.path
from datetime import datetime as dt
from datetime import date as d
from . import db_wiring

api = FastAPI()

@api.post("/users/")
def create_user(email: EmailStr, password:str, db: db_wiring.Session = db_wiring.Depends(db_wiring.get_db)):
    db_user = db_wiring.get_user_by_email(db, email=email)
    if db_user:
        raise db_wiring.HTTPException(status_code=400, detail="Email already registered")
    os.makedirs(f"app/users/{email}")
    return db_wiring.create_user_db(db=db, email=email, password=password)


@api.post("/upload_files")
async def upload_files(user_mail: EmailStr, password: str, date_eq_start: dt, date_eq_end: dt, user_data: UploadFile, db: db_wiring.Session = db_wiring.Depends(db_wiring.get_db)):
    if not db_wiring.get_user_by_email(db=db, email=user_mail):
        db_wiring.create_user_db(db=db, email=user_mail, password=password)
    today = str(dt.now())[:-7].split()
    folder_name = today[0]
    if not os.path.exists(f"app/users/{user_mail}/{folder_name}"):
        os.makedirs(f"app/users/{user_mail}/{folder_name}")
    with open(f"app/users/{user_mail}/{folder_name}/{user_data.filename}", "wb") as buffer:
        shutil.copyfileobj(user_data.file, buffer)
        db_wiring.create_path_db(db=db, email= user_mail, path=f"app/users/{user_mail}/{folder_name}/{user_data.filename}", date_upload = folder_name, date_eq_start=str(date_eq_start), date_eq_end=str(date_eq_end))
    return {"Message": "Successfull"}

@api.get("/get_files")
async def get_files_by_date(email: EmailStr, date: d, db: db_wiring.Session = db_wiring.Depends(db_wiring.get_db)):
    return db_wiring.get_data_by_date(db=db, email=email, date=date)
@api.get("/get_last_upload")
async def get_last_upload(email: EmailStr, db: db_wiring.Session = db_wiring.Depends(db_wiring.get_db)):
    return db_wiring.get_last_data(db=db, email=email)
    
    

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