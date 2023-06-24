from pydantic import EmailStr, BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
import os, shutil
import os.path
from datetime import datetime as dt
from datetime import date as d
from .database import *
from .crud import *
from .models import *
from .schemas import *

api = FastAPI()

@api.post("/users/", response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    os.makedirs(f"app/users/{user.email}")
    return create_user_db(db=db, user=user)


@api.post("/upload_files")
async def upload_files(email: EmailStr, date_eq_start: dt, date_eq_end: dt, file: UploadFile, db: Session = Depends(get_db)):
    if not get_user_by_email(db=db, email=email):
      return RedirectResponse("/users/")
    today = str(dt.now())[:-7].split()
    folder_name = today[0]
    if not os.path.exists(f"app/users/{email}/{folder_name}"):
        os.makedirs(f"app/users/{email}/{folder_name}")
    with open(f"app/users/{email}/{folder_name}/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        create_path_db(db=db, email=email, path=f"app/users/{email}/{folder_name}/{file.filename}", date_upload = folder_name, date_eq_start=date_eq_start, date_eq_end=date_eq_end)
    return {"Message": "Successfull"}

@api.get("/get_files/{email}/{date}")
async def get_files_by_date(email:EmailStr,date: d, db: Session = Depends(get_db)):
    return get_data_by_date(db=db, email=email, date=date)
@api.get("/get_last_upload/{email}")
async def get_last_upload(email:EmailStr, db: Session = Depends(get_db)):
    return get_last_data(db=db, email=email)
    
