import requests
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import exc
from database import engine, SessionLocal
from pydantic import BaseModel, Field
from models import *
app = FastAPI()
Base.metadata.create_all(bind=engine)


def clean_date(x):
    date = x[:10:]
    return date


class data(BaseModel):
    date: str = Field(min_length=1)
    meninggal: int = Field(gt=0)
    sembuh: int = Field(gt=0)
    positif: int = Field(gt=0)
    dirawat: int = Field(gt=0)
    kum_meninggal: int = Field(gt=0)
    kum_sembuh: int = Field(gt=0)
    kum_positif: int = Field(gt=0)
    kum_dirawat: int = Field(gt=0)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def root(db: Session = Depends(get_db)):
    dat = db.query(Covid_Data).all()[-1]

    send = {
        "ok": True,
        "data": {
            "total_positive": dat.kum_positif,
            "total_recovered": dat.kum_sembuh,
            "total_deaths": dat.kum_meninggal,
            "total_active": dat.dirawat,
            "new_positive": dat.positif,
            "new_recovered": dat.sembuh,
            "new_deaths": dat.meninggal,
            "new_active": dat.dirawat
        },
        "message": True
    }
    return send



@app.get("/update_data")
async def update(db: Session = Depends(get_db)):
    q = "DELETE from tb_harian"
    try:
        r_set = db.execute(q)
    except exc as e:
        error = str(e.__dict__['orig'])


    r = requests.get('https://data.covid19.go.id/public/api/update.json').json()
    for data in r["update"]["harian"]:
        dat = Covid_Data()
        dat.date = clean_date(data["key_as_string"])
        dat.meninggal = data["jumlah_meninggal"]["value"]
        dat.sembuh = data["jumlah_sembuh"]["value"]
        dat.positif = data["jumlah_positif"]["value"]
        dat.dirawat = data["jumlah_dirawat"]["value"]
        dat.kum_meninggal = data["jumlah_positif_kum"]["value"]
        dat.kum_sembuh = data["jumlah_sembuh_kum"]["value"]
        dat.kum_positif = data["jumlah_meninggal_kum"]["value"]
        dat.kum_dirawat = data["jumlah_dirawat_kum"]["value"]
        db.add(dat)
    db.commit()
    all_data = db.query(Covid_Data).all()
    dat = {
        "Update":all_data[-1],
        "daily": all_data
    }
    return dat

@app.get("/yearly/{year}")
async def year_data(year:str,db: Session = Depends(get_db)):
    dat = db.query(Covid_Data).filter(Covid_Data.date.contains(f"{year}")).all()
    if(len(dat)==0):
        send = {
            "ok": False,
            "message": "Invalid Years"
        }
    else:
        send = {
            "ok": True,
            "data": {
                "year": year,
                "positive": dat[-1].kum_positif,
                "recovered": dat[-1].kum_sembuh,
                "deaths": dat[-1].kum_meninggal,
                "active": dat[-1].kum_dirawat
            },
            "message": True
        }
    return send

@app.get("/monthly/{year}/{month}")
async def month_data(year:str,month:str,db: Session = Depends(get_db)):
    dat = db.query(Covid_Data).filter(Covid_Data.date.contains(f"{year}-{month}")).all()
    if (len(dat) == 0 or len(year)!=4 or len(month)!=2):
        send = {
            "ok": False,
            "message": "Invalid Date"
        }
    else:
        send = {
            "ok": True,
            "data": {
                "month": f"{year}-{month}",
                "positive": dat[-1].kum_positif,
                "recovered": dat[-1].kum_sembuh,
                "deaths": dat[-1].kum_meninggal,
                "active": dat[-1].kum_dirawat
            },
            "message": True
        }
    return send

@app.get("/daily/{year}/{month}/{tanggal}")
async def daily_data(year:str,month:str,tanggal:str,db: Session = Depends(get_db)):
    dat = db.query(Covid_Data).filter(Covid_Data.date == f"{year}-{month}-{tanggal}").all()
    if (len(dat) == 0 or len(year)!=4 or len(month)!=2 or len(tanggal) !=2):
        send = {
            "ok": False,
            "message": "Invalid Date"
        }
    else:
        send = {
            "ok": True,
            "data": {
                "month": dat[0].date,
                "positive": dat[0].positif,
                "recovered": dat[0].sembuh,
                "deaths": dat[-1].meninggal,
                "active": dat[-1].dirawat
            },
            "message": True
        }
    return send