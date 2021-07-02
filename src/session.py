import os
import psycopg2

DATABASE_URL = os.popen('heroku config:get postgres://vabciqqiikqtcv:7e78e69ac57609295aceaa4b8ae30bcdf660d1cb2332ca6e4428da9e42145409@ec2-35-169-188-58.compute-1.amazonaws.com:5432/ddfpq3kb87a2u5 -a captain-gongmaru-bot').read()[:-1]
host="ec2-35-169-188-58.compute-1.amazonaws.com"
dbname = "ddfpq3kb87a2u5"
user = "vabciqqiikqtcv"
password = "7e78e69ac57609295aceaa4b8ae30bcdf660d1cb2332ca6e4428da9e42145409"
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


setSession("asdfvx","asdf","mmm")

getSessionData("asdfvx","asdf")
cursor.close()
conn.close()
