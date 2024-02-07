from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from datetime import datetime, timedelta
# 필요한 의존성을 설치하기 위한 pip 명령어:
# pip install fastapi uvicorn Jinja2 python-multipart

app = FastAPI()
templates = Jinja2Templates(directory="templates")

background_image_url = ""#"/resources/jpg/image_free"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    url_list = ["/{hour}/{minute}", "/{hour}/{minute}/{title}", "/d-day/{year}/{month}/{day}/{hour}/{minute}/{title}"]
    return templates.TemplateResponse("list.html", {"request": request, "url_list": url_list})



@app.get("/{hour}/{minute}", response_class=HTMLResponse)
async def read_item(request: Request, hour: int, minute: int):
    now = datetime.now()
    current_time_milliseconds = int(now.timestamp() * 1000)
    end_of_day = datetime(now.year, now.month, now.day, hour, minute)
    endtime = end_of_day.timestamp() * 1000
    if now.timestamp() * 1000 > endtime:
        countdown = "퇴근 시간이 지났습니다!"
    else:
        remaining_time = end_of_day - now
        countdown = int(remaining_time.total_seconds() * 1000)  # 밀리세컨드로 변환
    return templates.TemplateResponse("club.html", {"request": request, "endtime": endtime, "countdown": countdown, "title": "퇴근", "bgurl": background_image_url})

@app.get("/resources/jpg/{filename}", response_class=FileResponse)
async def get_background_image(filename: str):
    return FileResponse("resources/" + filename + ".jpg")

@app.get("/{hour}/{minute}/{title}", response_class=HTMLResponse)
async def read_item_title(request: Request, hour: int, minute: int, title: str):
    now = datetime.now()
    current_time_milliseconds = int(now.timestamp() * 1000)
    end_of_day = datetime(now.year, now.month, now.day, hour, minute)
    endtime = end_of_day.timestamp() * 1000
    if now.timestamp() * 1000 > endtime:
        countdown = title + " 시간이 지났습니다!"
    else:
        remaining_time = end_of_day - now
        countdown = int(remaining_time.total_seconds() * 1000)  # 밀리세컨드로 변환
    return templates.TemplateResponse("club.html", {"request": request, "endtime": endtime, "countdown": countdown, "title": title, "bgurl": background_image_url})


@app.get("/d-day/{year}/{month}/{day}/{hour}/{minute}/{title}", response_class=HTMLResponse)
async def read_item_dday(request: Request, year: int, month: int , day: int, hour: int, minute: int, title: str):
    now = datetime.now()
    current_time_milliseconds = int(now.timestamp() * 1000)
    end_of_day = datetime(year, month, day, hour, minute)
    endtime = end_of_day.timestamp() * 1000
    if now.timestamp() * 1000 > endtime:
        countdown = title + " 시간이 지났습니다!"
    else:
        remaining_time = end_of_day - now
        countdown = int(remaining_time.total_seconds() * 1000)  # 밀리세컨드로 변환
    return templates.TemplateResponse("club.html", {"request": request, "endtime": endtime, "countdown": countdown, "title": title, "bgurl": background_image_url})

@app.get("/club", response_class=HTMLResponse)
async def read_item_club(request: Request):
    title = "클럽"
    now = datetime.now()
    end_of_day = now + timedelta(seconds=10)  # 현재 시간에서 10초 뒤로 설정
    endtime = int(end_of_day.timestamp() * 1000)  # 밀리세컨드로 변환
    remaining_time = end_of_day - now
    countdown = int(remaining_time.total_seconds() * 1000) 
    if now.timestamp() * 1000 > endtime:
        countdown = title + " 시간이 지났습니다!"
    else:
        remaining_time = end_of_day - now 
        countdown = int(remaining_time.total_seconds() * 1000) # 밀리세컨드로 변환
    return templates.TemplateResponse("club.html", {"request": request, "endtime": endtime, "countdown": countdown, "title": title, "bgurl": background_image_url})
