from pydantic import EmailStr, BaseModel
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from loguru import logger
import os, shutil
import io
import os.path
import sys
import uvicorn
from earthquake.app.earthquake import plot_map, retrieve_data, _UTC, plot_distance_time, get_dist_time
from datetime import datetime as dt
from datetime import date as d
from .database import *
from .crud import *
from .models import *
from .schemas import *


logger.add("logs/app.log", rotation="50 MB", level="DEBUG")
logger.add(sys.stdout, level="INFO", colorize=True)


api = FastAPI()

@api.post("/users/", response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    logger.info("Received request to create user")
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        logger.error(f"Email {db_user.token} already registered")
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user =  create_user_db(db=db, user=user) 
    os.makedirs(f"app/users/{user.email}")

    logger.info(f"Created directory for user {new_user.token}")
    logger.info(f"Created user in the database: {new_user.token}")
    return new_user

@api.post("/upload_files")
async def upload_files(email: EmailStr, date_eq_start: dt, date_eq_end: dt, file: UploadFile, db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=email)
    if not user:
        logger.warning(f"Unauthorized attempt to upload files")
        return RedirectResponse("/users/")
    if str(date_eq_start) > str(dt.now())[:-7]:
        logger.warning(f"Input start_date > correct date")
        raise HTTPException(status_code=400, detail="Earthquake start date cann't be in the future")
    if str(date_eq_start) > str(date_eq_end):
        logger.warning(f"Input start_date > end_date")
        raise HTTPException(status_code=400, detail="The date of the beginning of the earthquake cannot be later than the end")

    path = get_path(db=db, email=email, filename=file.filename)
    if path:
        logger.warning("File already uploaded")
        raise HTTPException(status_code=400, detail="File already uploaded")

    folder_name = d.today()
    if not os.path.exists(f"app/users/{email}/{folder_name}"):
        os.makedirs(f"app/users/{email}/{folder_name}")
        logger.info(f"Created directory for user {user.token} on {folder_name}")
    file_path = f"app/users/{email}/{folder_name}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        logger.info(f"Uploaded file: app/users/{user.token}/{folder_name}/{file.filename}")
    create_path_db(db=db, email=email,filename = file.filename, path=file_path, date_upload = folder_name, date_eq_start=date_eq_start, date_eq_end=date_eq_end)
    logger.info(f"Saved file path in the database for user {user.token}")
    return {"Message": "Successfull"}

@api.get("/get_files/{email}/{date}")
async def get_files_by_date(email:EmailStr, date: d, db: Session = Depends(get_db)):
    user = user = get_user_by_email(db=db, email=email)
    if not user:
        logger.error(f"User not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Requested files for user {user.token} on {date}")
    return get_data_by_date(db=db, email=email, date=date)

@api.get("/get_last_upload/{email}")
async def get_last_upload(email:EmailStr, db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=email)
    if not user:
        logger.error(f"User not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Requested last upload for user {user.token}")
    return get_last_data(db=db, email=email)

@api.post("/create_plot/")
async def create_plot(email: EmailStr, plot_info: Plot, db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=email)
    logger.info(f"Received request to create plot for email: {user.token}")
    if not user:
        logger.error(f"User not found")
        raise HTTPException(status_code=404, detail="User not found")
    path = os.path.dirname(plot_info.path)
    data = {plot_info.datatype: retrieve_data(plot_info.path, plot_info.datatype)}
    times = [t.replace(tzinfo=t.tzinfo or _UTC) for t in plot_info.dates]
    base_name = os.path.basename(plot_info.path)
    file_name = os.path.splitext(base_name)[0]
    savefig = os.path.join(path, file_name)
    result = get_result_db_by_path(db=db, email=email,path = savefig)
    if not result:
        create_result_db(db=db, email=email, filename=file_name, path=savefig)
    logger.info(f"Created plot for email: {user.token}")
    plot_map(times, data, plot_info.datatype, lon_limits=plot_info.lon_limits, lat_limits=plot_info.lat_limits, ncols=len(plot_info.dates), clims=plot_info.clims, savefig=savefig)
    savefig += ".png"
    return FileResponse(savefig, media_type="image/png")

@api.post("/create_plot_distance_time/")
async def create_plot_dt(email: EmailStr, plot_info: PlotDT, db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=email)
    logger.info(f"Received request to create distance-time plot for email: {user.token}")
    if not user:
        logger.error(f"User not found")
        raise HTTPException(status_code=404, detail="User not found")
    path = os.path.dirname(plot_info.path)
    data = retrieve_data(plot_info.path, plot_info.datatype)
    x, y, c = get_dist_time(data, plot_info.markers)
    base_name = os.path.basename(plot_info.path)
    file_name = os.path.splitext(base_name)[0] + "dt"
    savefig = os.path.join(path, file_name).replace('\\', '/')
    result = get_result_db_by_path(db=db, email=email,path = savefig)
    if not result:
        create_result_db(db=db, email=email, filename=file_name, path=savefig)
    logger.info(f"Created distance-time plot for email: {user.token}")
    plot_distance_time(x, y, c, plot_info.datatype, clims=plot_info.clims, savefig=savefig)
    savefig +=".png"
    return FileResponse(savefig, media_type="image/png")

@api.get("/results/{email}")
async def get_results(email:EmailStr, db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=email)
    if not user:
        logger.error(f"User not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Requested results for user {user.token}")
    return get_results_db(db=db, email=email)



