from fastapi import FastAPI
from routers import authRouter,listingRouter,userRouter
from fastapi.middleware.cors import CORSMiddleware 
from datetime import datetime,timedelta
import requests
import logging
import csv

app = FastAPI()

app.include_router(authRouter.router, tags=["authentication"])
app.include_router(userRouter.router,tags=["users"])
app.include_router(listingRouter.router,tags=["listing"])


# this endpoint request to time.ir website and receive 3month time data
@app.get("/bot" ,tags=["bot"])
async def get_time():
    """this endpoint request to time.ir website and receive 3month time data"""
    now = datetime.now()
    start_date = now - timedelta(days=30 * 3)
    end_date = now

    response =requests.get(
        "https://time.ir",
        params={
          "start_date": start_date,
          "end_date": end_date,
        } )

    if response.status_code == 200:
        data = response.json()
        with open("time.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        return data
    else:
        raise Exception("Error getting time data from time.ir")
  

# created log file contains request datetime and ip
logging.basicConfig(filename="app.log",level=logging.INFO)
@app.middleware("http")
async def request_logger(request,call_next):
    logging.info(f"time::{datetime.now()}, IP:{request.client.host}")
    response = await call_next(request)
    return response

# this function make a count.txt file and when the aplication statrup, it will be updated count number
def update_counter():
    try:
        with open("count.txt", "r") as file:
            count = int(file.read())
    except FileNotFoundError:
        count = 0
    count += 1
    with open("count.txt", "w") as file:
        file.write(str(count))

@app.on_event("startup")
async def startup_event():
    update_counter()


# CORS middreware - app oly accept request from origins list
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers = ["*"]
)
