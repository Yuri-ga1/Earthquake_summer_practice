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
    
class Plot(BaseModel):
    path: str
    dates: list[dt]
    datatype: str
    markers: list[dict]
    lon_limits: tuple[int, int]
    lat_limits: tuple[int, int]
    clims: dict


'''
        "2023-02-06 01:17:00",
         "2023-02-06 01:32:00",
         "2023-02-06 01:37:00"

         {
  "path": "app/users/user@example.com/2023-07-01/roti_01_17.h5",
  "dates": [
    "2023-02-06 01:17:00",
         "2023-02-06 01:32:00",
         "2023-02-06 01:37:00"
  ],
  "datatype": "ROTI",
  "markers": [
    {"lat": 37.220, 
                        "lon": 37.019, 
                        "time": "2023-02-06 01:17:34"}
  ],
  "lon_limits": [
    25,
    50
  ],
  "lat_limits": [
    25,
    50
  ],
  "clims": {"ROTI": [-0,0.5,"TECu/min"]}
}
'''