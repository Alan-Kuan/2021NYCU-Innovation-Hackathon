import os
import psycopg2
import pandas as pd
import xlrd
import csv 
from dotenv import load_dotenv
from datetime import datetime
import time
import schedule

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
        cmd="select user_id,content from med_reminder where time='"+time+"'"
        cursor.execute(cmd)
        

    elif mode=='by user':
        cmd="select user_id,content from med_reminder where user_id='"+user_id+"'"
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

    cmd="select * from hospital_reminder where user_id='"+user_id+"' and time_slot='"+time+"' and date='"+date+"' and type='"+type+"'"
    cursor.execute(cmd)
    tmp=cursor.fetchone()
    if tmp:
        print("Repeat information")
        return False
    cmd="INSERT INTO hospital_reminder (user_id,time_slot,date,type) "
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
        cmd="select user_id,type from hospital_reminder where time_slot='"+time+"' and date='"+date+"'"
    elif mode=='by user':
        cmd="select user_id,date,time_slot,type from hospital_reminder where user_id='"+user+"'"
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
    cmd="delete from hospital_reminder where user_id='"+user_id+"' and time_slot='"+time+"' and  date=TO_DATE('"+date+"', 'YYYY/MM/DD') and type='"+type+"'"
    print (cmd)

    cursor.execute(cmd)
    conn.commit() 



def remind_event(bot):
    def remind_contact(bot=bot):
        global conn_string

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        cmd="select user_id,code from communicate where role='patient'"
        cursor.execute(cmd)
        

        id=[]

        while True:
            tmp=cursor.fetchone()
            if tmp:
                id.append(tmp)
            else:
                break
            print(id)
        cmd="delete from session where data_key='patient_warn'"
        cursor.execute(cmd)
        conn.commit()
        
        for i in id:
            cmd="Insert into session (user_id,data_key,data_value) values ('"+i[0]+"','patient_warn','"+str(i[1])+"');"
            print(cmd)
            cursor.execute(cmd)
            conn.commit()
            try:
                bot.push_message(i[0], TextSendMessage(text='嗨!你在嗎?'))
            except:
                print("Can't send msg to ",i[0])

        cursor.close()
        conn.close()
    def remind_med(time_slot,bot=bot):
        id,do=get_med_reminder(mode='by time',time=time_slot)
        if do:
            for i in id:
                try:
                    bot.push_message(i[0], TextSendMessage(text='記得要吃'+i[1]+'窩!'))
                except:
                    print("sending med msg failed")
        
    def remind_hos(time_slot,bot=bot):
        today=datetime.today().strftime('%Y/%m/%d')
        id,do=get_hos_reminder(mode='by time',time=time_slot,date=today)
         

        if do:
            for i in id:
                if i[1]=='Go':
                    msg="記得等下要看醫生窩!"
                if i[1]=='Book':
                    msg="記得等下要預約醫生窩!"
                try:
                    bot.push_message(i[0], TextSendMessage(text=msg))
                except:
                    print("sending hos msg failed")
        global conn_string

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        

        print("delete",time_slot,today)
        cmd="delete from hospital_reminder where  time_slot='"+time_slot+"'  and date='"+today+"'"
        print (cmd)

        cursor.execute(cmd)
        conn.commit() 
    
    def warning_contact(bot=bot):
        global conn_string

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        cmd="select user_id, data_value from session where data_key='patient_warn'"
        id=[]
        cursor.execute(cmd)
        while True:
            tmp=cursor.fetchone()
            if tmp:
                id.append(tmp)
            else:
                break
        print(id)
        parent=[]
        for i in id:
            cmd="select user_id from communicate where code='"+str(i[1])+"' and role='parent'"
            print(cmd)
            cursor.execute(cmd)
            try:
                parent.append(cursor.fetchone()[0])
                bot.push_message(i[0], TextSendMessage(text='您的緊急連絡人消失了!快去關心他吧'))
            except:
                print("send warning msg failed")
                pass
        print(parent)
        #send_warn_msg(id):
    def handle_med():
        global conn_string
        today=datetime.today().strftime('%Y/%m/%d')
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        print("delete",today)
        cmd="delete from med_reminder where date<'"+date+"'"
        print (cmd)

        cursor.execute(cmd)
        conn.commit() 

    schedule.every().day.at('09:00').do(remind_contact)
    schedule.every().day.at('12:00').do(warning_contact)
    schedule.every().day.at('20:00').do(remind_contact)
    schedule.every().day.at('22:30').do(warning_contact)

    schedule.every().day.at('09:00').do(remind_med,'morning')
    schedule.every().day.at('12:00').do(remind_med,'noon')
    schedule.every().day.at('17:00').do(remind_med,'evening')
    schedule.every().day.at('21:30').do(remind_med,'night')
    
    schedule.every().day.at('09:00').do(remind_hos,'morning')
    schedule.every().day.at('12:00').do(remind_hos,'noon')
    schedule.every().day.at('18:00').do(remind_hos,'evening')

    schedule.every().day.at('00:05').do(handle_med)
    #remind_contact()
   

