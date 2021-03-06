import os
import psycopg2
import pandas as pd
import xlrd
import csv
from dotenv import load_dotenv


load_dotenv()



host=os.environ.get('host')
dbname = os.environ.get('dbname')
user = os.environ.get('user')
password = os.environ.get('password')
port="5432"
sslmode = "require"
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)


def setSession(user_id, data_key, data_value):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    data,get=getSessionData(user_id,data_key)
    if get:
        cmd="UPDATE Session SET data_value='"+str(data_value)+"'WHERE user_id='"+str(user_id)+"' and data_key='"+str(data_key)+"';"
        cursor.execute(cmd)
        conn.commit()
    else:
        cmd="INSERT INTO Session (user_id,data_key,data_value) "
        cmd+="VALUES ('"+str(user_id)+"', '"+str(data_key)+"','"+str(data_value)+"');"
        cursor.execute(cmd)
        conn.commit()
    cursor.close()
    conn.close()
    
def getSessionData(user_id, data_key):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    #global cursor
    cmd="SELECT data_value FROM Session "
    cmd+="WHERE user_id = '"+str(user_id)+"'"
    cmd+="AND data_key = '"+str(data_key)+"';"
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
    cursor.close()
    conn.close()
    return data,get
    
def getSessionKey(user_id):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cmd="SELECT data_key FROM Session "
    cmd+="WHERE user_id = '"+str(user_id)+"'"

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
    cursor.close()
    conn.close()
    return data,get

def getSymptom(part='No'):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    #global cursor
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
    cursor.close()
    conn.close()
    return symptom

def getType(symptom):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
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
    cursor.close()
    conn.close()
    return tp

def addCom(user_id,code):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    if CheckCom(user_id):
        print("Already connected")
        return 'has connection'

    cmd="select * from communicate where code='"+code+"'"
    cursor.execute(cmd)
    tmp=cursor.fetchone()
    if tmp:
        print("code repeat")
        return 'code repeat'
   
    cmd="select * from communicate where user_id='"+user_id+"'"
    cursor.execute(cmd)
    tmp=cursor.fetchone()
    if tmp:
        cmd="update communicate set code='"+code+"' where user_id='"+user_id+"'"
        cursor.execute(cmd)
        conn.commit()
        print("id repeat, update new code")
        return 'id repeat'
    


    cmd="insert into communicate (user_id,code,role) values ('"+str(user_id)+"','"+str(code)+"','patient')"
    cursor.execute(cmd)
    conn.commit()
    print("successful add patient")
    cursor.close()
    conn.close()
    return 'add'

def ConfirmCom(user_id,code):
    if CheckCom(user_id):
        return False

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cmd="select * from communicate where user_id='"+user_id+"'"
    cursor.execute(cmd)
    pt=[]
    while True:
        tmp=cursor.fetchone()
        if tmp:
            pt.append(tmp)
            get=True
        else:
            break
    if len(pt)>0:
        print("Setting parent error")
        cursor.close()
        conn.close()
        return False

    cmd="select role,count(*) from(select code,role from communicate where code='"+str(code)+"')as a group by role"
    cursor.execute(cmd)
    pt=[]
    while True:
        tmp=cursor.fetchone()
        if tmp:
            pt.append(tmp)
            get=True
        else:
            break
    Check=False
    if len(pt)==1:
        cmd="insert into communicate (user_id,code,role) values ('"+str(user_id)+"','"+str(code)+"','parent')"
        cursor.execute(cmd)
        conn.commit()
        print("Confirmed parent.")
    elif len(pt)==0:
        print("Can't find the patient")
    elif len(pt)>1:
        print("The parent had been set")
    cursor.close()
    conn.close()
    return True

def DelCom(user_id):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cmd="select code from communicate where user_id='"+user_id+"'"
    cursor.execute(cmd)


    tmp=cursor.fetchone()
    if tmp:
        code=tmp[0]
        get=True
    else:
        print("Can't find user_id")
        cursor.close()
        conn.close()
        return False
    cmd="delete from communicate where code='"+str(code)+"'"
    cursor.execute(cmd)
    conn.commit()
    print("Successful delete")
    cursor.close()
    conn.close()
    return True

def CheckCom(user_id):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cmd="select code from communicate where user_id='"+user_id+"'"
    cursor.execute(cmd)
    tmp=cursor.fetchone()
    if tmp:
        code=tmp
        code=code[0]
    else:
        print('not in database')
        return False
    cmd="select count(*) from communicate where code='"+code+"'"
    cursor.execute(cmd)
    tmp=cursor.fetchone()
    if tmp:
        cnt=tmp
        cnt=cnt[0]
        print(cnt)
    if cnt==2:
        print("have connection")
        return True
    else:
        return False




