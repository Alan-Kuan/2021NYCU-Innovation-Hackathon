import os
import psycopg2
import pandas as pd
import xlrd
import csv 
from dotenv import load_dotenv


load_dotenv('./.env.sample')



host=os.environ.get('host')
dbname = os.environ.get('dbname')
user = os.environ.get('user')
password = os.environ.get('password')
port="5432"
sslmode = "require"
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)

cursor = conn.cursor()


def setSession(user_id, data_key, data_value):
    global cursor
    data,get=getSessionData(user_id,data_key)
    if get:
        cmd="UPDATE Session SET data_value='"+str(data_value)+"'WHERE user_id='"+str(user_id)+"' and data_key='"+str(data_key)+"';"
        cursor.execute(cmd)
        conn.commit()
    else:
        cmd="SELECT max(session_id) FROM Session;"
        session_num=cursor.execute(cmd)
        try:
            session_num=int(session_num)
        except:
            session_num=-1
        cmd="INSERT INTO Session (session_id,user_id,data_key,data_value) "
        cmd+="VALUES ("+str(session_num+1)+",'"+str(user_id)+"', '"+str(data_key)+"',' "+str(data_value)+"');"
        cursor.execute(cmd)
        conn.commit()
    
    
                    

def getSessionData(user_id, data_key):
    global cursor
    cmd="SELECT data_value FROM Session "
    cmd+="WHERE user_id ='"+str(user_id)+"'"
    #""++" and data_key=="+str(data_key)+";"
    cursor.execute(cmd)

    data=[]
    get=False
    while True:
        tmp=cursor.fetchone()
        if tmp:
            data.append(tmp)
            get=True
        else:
            break
    if get:
        print("found")
    else:
        print("notfound")
    return data,get


def getSymptom(part='No'):
    global cursor
    cmd="select symptom from symptom where part='"+str(part)+"' group by symptom"
    cursor.execute(cmd)
    
    symptom=[]
    get=False
    while True:
        tmp=cursor.fetchone()
        if tmp:
            symptom.append(tmp)
            get=True
        else:
            break
    return symptom

def getType(symptom):
    cmd="select type,count(*) from("
    for i in range(len(symptom)):
        if i!=0:
            cmd+="union all "
        cmd+="select type from symptom where symptom='"+str(symptom[i])+"' "
    cmd+=")as a group by type order by count desc "
    cursor.execute(cmd)
    tp=[]
    get=False
    while True:
        tmp=cursor.fetchone()
        if tmp:
            tp.append(tmp)
            get=True
        else:
            break
    return tp

#setSession("asdfvx","asdf","mmm")

#getSessionData("asdfvx","asdf")
tp=getType(["頭 痛","投 暈","後頸疼痛"])
print(tp)
cursor.close()
conn.close()
