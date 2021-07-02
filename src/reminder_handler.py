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

def add_med_reminder(user_id,time,content,stop_date=None):
    global conn_string

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cmd="select * from med_reminder where user_id='"+user_id+"' and time='"+time+"' and content='"+content+"'"
    cursor.execute(cmd)
    tmp=cursor.fetchone()
    if tmp:
        print("Repeat information")
        return False
   
    if stop_date!=None:
        cmd="INSERT INTO med_reminder (user_id,time,content,stop_date) "
        cmd+="VALUES ('"+str(user_id)+"','"+str(time)+"', '"+str(content)+"', '"+str(stop_date)+"');"
    else:
        cmd="INSERT INTO med_reminder Session (user_id,time,content) "
        cmd+="VALUES ('"+str(user_id)+"','"+str(time)+"', '"+str(content)+"');"
    cursor.execute(cmd)
    conn.commit() 

    cursor.close()
    conn.close()
    print("add",user_id,time,stop_date)
    return True
def get_med_reminder(mode=None,user_id=None,time=None):
    global conn_string

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    if mode=='by time':
        cmd="select user_id from med_reminder where time='"+time+"'"
        cursor.execute(cmd)
        

    elif mode=='by user':
        cmd="select user_id from med_reminder where user_id='"+user_id+"'"
        cursor.execute(cmd)
    else:
        print("wrong mode")
        return None,False

    pt=[]
    get=False
    while True:
        tmp=cursor.fetchone()
        if tmp:
            pt.append(tmp)
            get=True
        else:
            break
        
    cursor.close()
    conn.close()
    if get:
        print("Get remind")
    else:
        print("Can't find")
    return pt,get
def del_med_reminder(user_id=None,time=None,content=None):
    global conn_string

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("delete",user_id,time,content)
    cmd="delete from med_reminder where user_id='"+user_id+"' and time='"+time+"' and content='"+content+"'"
    cursor.execute(cmd)
    conn.commit() 

def add_hos_reminder(user_id,date,time,type='Go'):
    global conn_string

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cmd="select * from hospital_reminder where user_id='"+user_id+"' and time='"+time+"' and date='"+date+"' and type='"+type+"'"
    cursor.execute(cmd)
    tmp=cursor.fetchone()
    if tmp:
        print("Repeat information")
        return False
    cmd="INSERT INTO hospital_reminder (user_id,time,date,type) "
    cmd+="VALUES ('"+str(user_id)+"','"+str(time)+"', TO_DATE('"+date+"', 'YYYY/MM/DD'), '"+str(type)+"');"
    cursor.execute(cmd)
    conn.commit() 

    cursor.close()
    conn.close()
    print("add",user_id,date,time,type)
    return True
def get_hos_reminder(mode='by time',date=None,time=None,user=None):
    global conn_string

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    if mode=='by time':
        cmd="select user_id,type from hospital_reminder where time='"+time+"' and date='"+date+"'"
    elif mode=='by user':
        cmd="select user_id,date,time,type from hospital_reminder where user_id='"+user+"'"
    else:
        print("Wrong mode")
        return [],False
    cursor.execute(cmd)
    pt=[]
    get=False
    while True:
        tmp=cursor.fetchone()
        if tmp:
            pt.append(tmp)
            get=True
        else:
            break


    cursor.close()
    conn.close()
    if get:
        print("Find")
    else:
        print("not find")
    return pt,get
def del_hos_reminder(user_id,date,time,type):
    global conn_string

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    print("delete",user_id,time,date,type)
    cmd="delete from hospital_reminder where user_id='"+user_id+"' and time='"+time+"' and  date=TO_DATE('"+date+"', 'YYYY/MM/DD') and type='"+type+"'"
    print (cmd)

    cursor.execute(cmd)
    conn.commit() 



