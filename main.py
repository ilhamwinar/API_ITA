from fastapi import Depends, FastAPI, HTTPException, status, Form, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path
from datetime import datetime
import json


#defini direktori    
current_dir = os.getcwd()


import subprocess

def parse_ita_process(gardu):
    gardu=str(gardu)
    try:
        # Run the command to get processes related to python3
        process = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        
        # Filter out the grep command itself and then filter for python3 processes
        lines = process.stdout.splitlines()
        ita_processes = [line for line in lines if 'python3' in line and '--id_gardu '+gardu in line]
        
        # Print each line that contains ITA.py
        if ita_processes:
            for line in ita_processes:
                status=200
                return status
            
        else:
            status=404
            return status
            
        
    except Exception as e:
        print(f"An error occurred: {e}")



## FUNGSI UNTUK READ LOG
def write_log(lokasi_log, datalog):
    waktulog = datetime.now()
    dirpathlog = f"{lokasi_log}"
    os.makedirs(dirpathlog, exist_ok=True)
    pathlog = f"{waktulog.strftime('%d%m%Y')}.log"
    file_path = Path(f"{dirpathlog}/{pathlog}")
    datalog = "[INFO] - " + datalog
    if not file_path.is_file():
        file_path.write_text(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}\n")
    else :
        fb = open(f"{dirpathlog}/{pathlog}", "a")
        fb.write(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}\n")
        fb.close
    
    print(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}")

# inisialisasi API
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"])

# @app.post("/active_service")
# async def active_service(gardu: str = Form(...)):
#     status2=parse_ita_process(gardu)
#     return {"status":status2}

# @app.post("/last_active")
# async def last_active(gardu: str = Form(...)):
#     # Open the file in read mode
#     try:
#         with open(gardu+'.txt', 'r') as file:
#             # Read the contents of the file
#             content = file.read()
#         status=200
#         content=str(content)
#     except:
#         content="None"
#         status=404
#     return {"status":status,"content":content}

@app.post("/active_service")
async def active_service(request: Request):
    raw_json = await request.json()  # Receive the raw JSON data
    gardu= raw_json["gerbang"]
    gardu=gardu.split("_")[1]
    status2=parse_ita_process(gardu)
    return {"status":status2}
    #return {"status":gardu}

@app.post("/last_active")
async def last_active(request: Request):
    raw_json = await request.json()  # Receive the raw JSON data
    gardu= raw_json["gerbang"]
    gardu=gardu.split("_")[1]
    try:
        with open(gardu+'.txt', 'r') as file:
            # Read the contents of the file
            content = file.read()
        status=200
        content=str(content)
    except:
        content="None"
        status=404
    return {"status":status,"content":content}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8100,log_level="info",reload=True)