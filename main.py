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
import mysql.connector
import subprocess
import playsound
import requests
from requests_toolbelt import MultipartEncoder
from requests.exceptions import HTTPError


#defini direktori    
current_dir = os.getcwd()

## FUNGSI UNTUK READ LOG
def write_log(datalog):
    waktulog = datetime.now()
    dirpathlog = f"Log/"
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

def write_log_error(datalog):
    waktulog = datetime.now()
    dirpathlog = f"Log/"
    os.makedirs(dirpathlog, exist_ok=True)
    pathlog = f"{waktulog.strftime('%d%m%Y')}.log"
    file_path = Path(f"{dirpathlog}/{pathlog}")
    datalog = "[ERROR] - " + datalog
    if not file_path.is_file():
        file_path.write_text(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}\n")
    else :
        fb = open(f"{dirpathlog}/{pathlog}", "a")
        fb.write(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}\n")
        fb.close
    
    print(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}")

#----------------------------------------------------------------------------------------------

try:      
    MyDBLocal = mysql.connector.connect(host='127.0.0.1', database='db_aicctv',user='aicctv',password='Jmt02022!')
    MyDBLocalCursor = MyDBLocal.cursor()
except mysql.connector.Error as error:
    # LOGGER.info(f'Failed connect to local server')
    write_log_error("CANNOT CONNECT TO DATABASE")
    pass

#-----------------------------------------------------------------------------------------------


def parse_ita_process(gardu,database_connection):
    gardu=str(gardu)
    try:
        # Run the command to get processes related to python3
        process = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        
        # Filter out the grep command itself and then filter for python3 processes
        lines = process.stdout.splitlines()
        ita_processes = [line for line in lines if 'python3 ITA.py' in line and '--Location '+gardu in line]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Print each line that contains ITA.py
        if ita_processes:
            for line in ita_processes:
                status=200
                if database_connection==0:
                    try:
                        #SQLStatement = """INSERT IGNORE INTO command_log (cmd_id,server_time) Values (%s,%s) ON DUPLICATE KEY UPDATE cmd_id = VALUES(cmd_id)"""
                        SQLStatement = """INSERT INTO command_log (cmd_id,server_time) Values (%s,%s)"""
                        ValSQL = (5,current_time)
                        result = MyDBLocalCursor.execute(SQLStatement, ValSQL)
                        MyDBLocal.commit()
                    except:
                        print("GAGAL INSERT")
                    return status
                elif database_connection==1:
                    try:
                        #SQLStatement = """INSERT IGNORE INTO command_log (cmd_id,server_time) Values (%s,%s) ON DUPLICATE KEY UPDATE cmd_id = VALUES(cmd_id)"""
                        SQLStatement = """INSERT INTO command_log (cmd_id,server_time) Values (%s,%s)"""
                        ValSQL = (9,current_time)
                        result = MyDBLocalCursor.execute(SQLStatement, ValSQL)
                        MyDBLocal.commit()
                    except:
                        print("GAGAL INSERT")
                    return status
        else:
            status=404
            try:
                #SQLStatement = """INSERT IGNORE INTO command_log (cmd_id,server_time) Values (%s,%s) ON DUPLICATE KEY UPDATE cmd_id = VALUES(cmd_id)"""
                SQLStatement = """INSERT INTO command_log (cmd_id,server_time) Values (%s,%s)"""
                ValSQL = (1,current_time)
                result = MyDBLocalCursor.execute(SQLStatement, ValSQL)
                MyDBLocal.commit()
            except:
                print("GAGAL INSERT")
            return status
            
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
def parse_ita_sender(gardu,MyDBLocalCursor):
    gardu=str(gardu)
    try:
        # Run the command to get processes related to python3
        process = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        
        # Filter out the grep command itself and then filter for python3 processes
        lines = process.stdout.splitlines()
        ita_processes = [line for line in lines if 'autorunsender.sh'  in line]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Print each line that contains ITA.py
        if ita_processes:
            for line in ita_processes:
                status=200
                try:
                    #SQLStatement = """INSERT IGNORE INTO command_log (cmd_id,server_time) Values (%s,%s) ON DUPLICATE KEY UPDATE cmd_id = VALUES(cmd_id)"""
                    SQLStatement = """INSERT INTO command_log (cmd_id,server_time) Values (%s,%s)"""
                    ValSQL = (6,current_time)
                    result = MyDBLocalCursor.execute(SQLStatement, ValSQL)
                    MyDBLocal.commit()
                except:
                    print("GAGAL INSERT")
                return status
            
        else:
            status=404
            try:
                #SQLStatement = """INSERT IGNORE INTO command_log (cmd_id,server_time) Values (%s,%s) ON DUPLICATE KEY UPDATE cmd_id = VALUES(cmd_id)"""
                SQLStatement = """INSERT INTO command_log (cmd_id,server_time) Values (%s,%s)"""
                ValSQL = (2,current_time)
                result = MyDBLocalCursor.execute(SQLStatement, ValSQL)
                MyDBLocal.commit()
            except:
                print("GAGAL INSERT")
            return status
    except Exception as e:
        print(f"An error occurred: {e}")


def cek_cctv(ip_address,MyDBLocalCursor):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Use the ping command with a count of 1 (only send 1 packet)
        # '-n' for Windows, '-c' for Unix-based systems like Linux or macOS
        response = subprocess.run(
            ["ping", "-c", "1", ip_address],  # Use "-n 1" instead of "-c 1" on Windows
            stdout=subprocess.PIPE,           # Capture standard output
            stderr=subprocess.PIPE            # Capture standard error
        )

        # Check the return code to determine if ping was successful
        if response.returncode == 0:
            print(f"Ping to {ip_address} was successful.")
            try:
                #SQLStatement = """INSERT IGNORE INTO command_log (cmd_id,server_time) Values (%s,%s) ON DUPLICATE KEY UPDATE cmd_id = VALUES(cmd_id)"""
                SQLStatement = """INSERT INTO command_log (cmd_id,server_time) Values (%s,%s)"""
                ValSQL = (7,current_time)
                result = MyDBLocalCursor.execute(SQLStatement, ValSQL)
                MyDBLocal.commit()
            except:
                print("GAGAL INSERT")

            status=200
            return status

        else:
            print(f"Ping to {ip_address} failed.")
            try:
                #SQLStatement = """INSERT IGNORE INTO command_log (cmd_id,server_time) Values (%s,%s) ON DUPLICATE KEY UPDATE cmd_id = VALUES(cmd_id)"""
                SQLStatement = """INSERT INTO command_log (cmd_id,server_time) Values (%s,%s)"""
                ValSQL = (3,current_time)
                result = MyDBLocalCursor.execute(SQLStatement, ValSQL)
                MyDBLocal.commit()
            except:
                print("GAGAL INSERT")
            
            status=404
            return status
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
def cek_server(ip_address,MyDBLocalCursor):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Use the ping command with a count of 1 (only send 1 packet)
        # '-n' for Windows, '-c' for Unix-based systems like Linux or macOS
        response = subprocess.run(
            ["ping", "-c", "1", ip_address],  # Use "-n 1" instead of "-c 1" on Windows
            stdout=subprocess.PIPE,           # Capture standard output
            stderr=subprocess.PIPE            # Capture standard error
        )

        # Check the return code to determine if ping was successful
        if response.returncode == 0:
            print(f"Ping to {ip_address} was successful.")
            try:
                #SQLStatement = """INSERT IGNORE INTO command_log (cmd_id,server_time) Values (%s,%s) ON DUPLICATE KEY UPDATE cmd_id = VALUES(cmd_id)"""
                SQLStatement = """INSERT INTO command_log (cmd_id,server_time) Values (%s,%s)"""
                ValSQL = (8,current_time)
                result = MyDBLocalCursor.execute(SQLStatement, ValSQL)
                MyDBLocal.commit()
            except:
                print("GAGAL INSERT")

            status=200
            return status

        else:
            print(f"Ping to {ip_address} failed.")
            try:
                #SQLStatement = """INSERT IGNORE INTO command_log (cmd_id,server_time) Values (%s,%s) ON DUPLICATE KEY UPDATE cmd_id = VALUES(cmd_id)"""
                SQLStatement = """INSERT INTO command_log (cmd_id,server_time) Values (%s,%s)"""
                ValSQL = (4,current_time)
                result = MyDBLocalCursor.execute(SQLStatement, ValSQL)
                MyDBLocal.commit()
            except:
                print("GAGAL INSERT")
            
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

@app.get("/get_ping")
async def ping():
    return {"status":"200"}

#API UNTUK MENJALANKAN SUARA PADA REMOTE PC
@app.get("/status_auto")
async def status_test():
    try:
        playsound(current_dir+"/sound_2.mp3")
        write_log("PLAY SOUND VIA PLAYSOUND")
        return {"status":"berhasil mode auto playsound"}
    except:
        write_log_error("GAGAL PLAY SOUND VIA PLAYSOUND")
        return {"status":"tidak berhasil mode auto playsound"}

#----------------------------------------------------------
# API MOTOR

## GET DATA CONFIG
@app.post("/get_motor_config")
async def get_motor_config(location: str = Form()):  
   
    #write_log("log_api",str(location))
    m = MultipartEncoder(fields={'location': str(location)})

    # Define the URL for the API endpoint
    url = "http://175.10.1.14:8310/get_motor_config"
    #response = requests.post(url, data=m,headers={'Content-Type': m.content_type})
    
    try:
        #response = requests.get(url)
        response = requests.post(url, data=m,headers={'Content-Type': m.content_type})
        response=response.json()
        response_code=response["status"]

        if response_code==200:
            id_cctv= response["id_cctv"]
            rtsp=response["rtsp"]
            delay=response["delay"]
            masking=response["masking"]
            endpoint=response["endpoint"]
            model=response["model"]
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sql_insert = """
            INSERT INTO motor_config (id_cctv, location, rtsp, delay, masking, endpoint, model, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                rtsp = %s, delay = %s, masking = %s, endpoint = %s, model = %s;
            """
            query_insert=(id_cctv,location,rtsp,delay,masking,endpoint,model,created_at,rtsp,delay,masking,endpoint,model)
            
            try:
                #cursor=cnx.cursor()
                write_log("log_api","START INSERTING TO MYSQL MOTOR CONFIG")
                cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
                cursor.execute(sql_insert,query_insert)
                cnx.commit()
                write_log("log_api","SUCCESSED INSERTING TO MYSQL MOTOR CONFIG")
            except Exception as err:
                #write_log("log_api","NOT INSERTED TO DATABASE MOTOR CONFIG")
                write_log("log_api",str(err))
    
            return response
        
        elif response_code==404:
            return {"status":404}
        
        # Check if the response returned a server error (5xx)
        if response.status_code == 500:
            write_log("log_api","500 Internal Server Error occurred.")
            # Get response details for debugging
            write_log("log_api","Response Content:", response.text)
            write_log("log_api","Response Headers:", response.headers)
        else:
            # If the status code is not 500, raise an error for other bad responses (4xx, 5xx)
            response.raise_for_status()

    except HTTPError as http_err:
        write_log("log_api",f"HTTP error occurred: {http_err}")  # Output for HTTP errors other than 500
        return {"status":500}

    except Exception as err:
        write_log("log_api",f"An error occurred: {err}")  # Handle any other exceptions
        return {"status":500}

#----------------------------------------------------------
# API NTP

## GET DATA CONFIG
@app.post("/get_ntp_config")
async def get_ntp_config(location: str = Form()):  
   
    #write_log("log_api",str(location))
    m = MultipartEncoder(fields={'location': str(location)})

    # Define the URL for the API endpoint
    url = "http://175.10.1.14:8310/get_ntp_config"
    #response = requests.post(url, data=m,headers={'Content-Type': m.content_type})
    
    try:
        #response = requests.get(url)
        response = requests.post(url, data=m,headers={'Content-Type': m.content_type})
        response=response.json()
        response_code=response["status"]
        write_log("log_api",str(response_code))

        if response_code==200:
            id_cctv= response["id_cctv"]
            rtsp=response["rtsp"]
            delay=response["delay"]
            masking=response["masking"]
            endpoint=response["endpoint"]
            model=response["model"]
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sql_insert = """
            INSERT INTO ntp_config (id_cctv, location, rtsp, delay, masking, endpoint, model, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                rtsp = %s, delay = %s, masking = %s, endpoint = %s, model = %s;
            """
            query_insert=(id_cctv,location,rtsp,delay,masking,endpoint,model,created_at,rtsp,delay,masking,endpoint,model)
            
            try:
                #cursor=cnx.cursor()
                write_log("log_api","START INSERTING TO MYSQL MOTOR CONFIG")
                cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
                cursor.execute(sql_insert,query_insert)
                cnx.commit()
                write_log("log_api","SUCCESSED INSERTING TO MYSQL MOTOR CONFIG")
            except Exception as err:
                #write_log("log_api","NOT INSERTED TO DATABASE MOTOR CONFIG")
                write_log("log_api",str(err))
    
            return response
        
        elif response_code==404:
            return {"status":404}
        
        # Check if the response returned a server error (5xx)
        if response.status_code == 500:
            write_log("log_api","500 Internal Server Error occurred.")
            # Get response details for debugging
            write_log("log_api","Response Content:", response.text)
            write_log("log_api","Response Headers:", response.headers)
        else:
            # If the status code is not 500, raise an error for other bad responses (4xx, 5xx)
            response.raise_for_status()

    except HTTPError as http_err:
        write_log("log_api",f"HTTP error occurred: {http_err}")  # Output for HTTP errors other than 500
        return {"status":500}

    except Exception as err:
        write_log("log_api",f"An error occurred: {err}")  # Handle any other exceptions
        return {"status":500}

#----------------------------------------------------------
# API GRAFANA ACTIVE ITA

@app.post("/db_service")
async def db_service(request: Request):
    raw_json = await request.json()  # Receive the raw JSON data
    gardu= raw_json["ITA"]
    status2=parse_ita_process(gardu,1)
    return {"status":status2}

@app.post("/ita_service")
async def ita_service(request: Request):
    raw_json = await request.json()  # Receive the raw JSON data
    gardu= raw_json["ITA"]
    status2=parse_ita_process(gardu,0)
    return {"status":status2}

@app.post("/sender_service")
async def sender_service(request: Request):
    raw_json = await request.json()  # Receive the raw JSON data
    gardu= raw_json["ITA"]
    status2=parse_ita_sender(gardu,MyDBLocalCursor)
    return {"status":status2}

@app.post("/last_active")
async def last_active(request: Request):
    raw_json = await request.json()  # Receive the raw JSON data
    gardu= raw_json["ITA"]
    #gardu=gardu.split("_")[1]
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

@app.post("/cek_cctv")
async def pingcctv(request: Request):
    raw_json = await request.json()  # Receive the raw JSON data
    gardu= raw_json["ITA"]
    gardu=str(gardu)
    status2=cek_cctv(gardu,MyDBLocalCursor)
    return {"status":status2}

@app.post("/cek_server")
async def pingserver(request: Request):
    raw_json = await request.json()  # Receive the raw JSON data
    gardu= raw_json["ITA"]
    gardu=str(gardu)
    status2=cek_server(gardu,MyDBLocalCursor)
    return {"status":status2}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8200,log_level="info",reload=True)