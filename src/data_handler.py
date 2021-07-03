import csv
import pandas as pd
import xlrd
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import datetime
from dotenv import load_dotenv
import io
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
def hospital():
    link="https://data.nhi.gov.tw/DataSets/DataSetResource.ashx?rId=A21030000I-D21002-005"
    r = requests.post(link)
    if r.ok:
        data = r.content.decode('utf8')
        df = pd.read_csv(io.StringIO(data))
        print(df)
    link="https://data.nhi.gov.tw/DataSets/DataSetResource.ashx?rId=A21030000I-D21003-003"
    r = requests.post(link)
    if r.ok:
        data = r.content.decode('utf8')
        df1 = pd.read_csv(io.StringIO(data))
        print(df1)
        df=pd.concat([df,df1])
    link="https://data.nhi.gov.tw/DataSets/DataSetResource.ashx?rId=A21030000I-D21004-008"
    r = requests.post(link)
    if r.ok:
        data = r.content.decode('utf8')
        df1 = pd.read_csv(io.StringIO(data))
        print(df1)
        df=pd.concat([df,df1])
    link="https://data.nhi.gov.tw/DataSets/DataSetResource.ashx?rId=A21030000I-D21001-003"
    r = requests.post(link)
    if r.ok:
        data = r.content.decode('utf8')
        df1 = pd.read_csv(io.StringIO(data))
        print(df1)
        df=pd.concat([df,df1])
    df.reset_index(inplace=True)

    with open('../data/hospital.json', 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False)
def symptom():
    url = "https://www.vghtc.gov.tw/Module/SearchBySymptom?fbclid=IwAR0xj5SvcWdpKtHfF28xve0kbkAywOGebOEI5O1P0wNWdQeI5uscmszmd5I"
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")



    text=soup.findAll(["td", "span"])

    sym_list=[]
    tp_list=[]
    part_list=[]
    x=0
    for i in range(67,571):

        if(text[i].name=='span'):
            part=text[i].text

            print('part:',part)
        else:
            if x%3==0:

                symptom=str(text[i].text)
                symptom.replace(" ","")
                print('symptom:', symptom)
            if x%3==2:
                tp=text[i].text
                tp.replace(" ","")

                tp=tp.split('、')
                tp = [x.replace("\r\n","") for x in tp]
                tp = [x.replace(" ","") for x in tp]
                print('type:',tp)
                for i in tp:
                    sym_list.append(symptom)
                    tp_list.append(i)
                    part_list.append(part)
            x+=1
    dict={'part':part_list,'symptom':sym_list,'type':tp_list}
    df=pd.DataFrame.from_dict(dict)
    with open('symptom.json', 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False)
def open_time():
    link="https://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D21006-001&l=https://data.nhi.gov.tw/resource/Opendata/全民健康保險特約院所固定服務時段.csv"
    r = requests.post(link)
    if r.ok:
        data = r.content.decode('utf8')
        df = pd.read_csv(io.StringIO(data))
        print(df)
    with open('opentime.json', 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False)
def holiday():
    link="https://data.nhi.gov.tw/DataSets/DataSetResource.ashx?rId=A21030000I-D21007-002"
    r = requests.post(link)
    if r.ok:
        data = r.content.decode('utf8')
        df = pd.read_csv(io.StringIO(data))
        print(df)
    df=df[df.特定節日>1100000]
    with open('holiday.json', 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False)
def addresstran():
    df = pd.read_json ('../data/hospital.json')
    geolocator = Nominatim(user_agent="agent")
    print(df.columns)
    find=0
    notfind=0
    for ind,row in df.iterrows():

       print(row['醫事機構名稱'])

       if ind%500==10:
            print("writing.......")
            with open('../data/hospital.json', 'w', encoding='utf-8') as file:
                df.to_json(file, force_ascii=False)
            print("finish")
            print(ind,"/",len(df.index))
       try:
           location = geolocator.geocode(str(row['醫事機構名稱']))
           df.loc[ind,'latitude']=location.latitude
           df.loc[ind,'longitude']=location.longitude
           print(" find place")
           find+=1
       except:
            try:
                location = geolocator.geocode(str(row['地址']))
                df.loc[ind,'latitude']=location.latitude
                df.loc[ind,'longitude']=location.longitude
                print(" find place")
                find+=1
            except:
                print("can't find place")
                notfind+=1
    print("writing.......")
    with open('../data/hospital.json', 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False)
    print("finish")
    print("find:",find)
    print("notfind:",notfind)

def DisRank(user_loc):
    df = pd.read_json('../data/hospital.json')
    print(df.columns)
    df['latitude']=df['latitude'].fillna('null')
    df= df[~ df['latitude'].isin(['null'])]
    df=df.reset_index(drop=True)
    print(df)
    for i in range(len(df.index)):
        df.loc[i,'Dis']=geodesic(user_loc, (df.loc[i,'latitude'],df.loc[i,'longitude'])).meters
    df=df.sort_values(by=['Dis'])
    print(df)
    print(df['醫事機構代碼'])
    return df[['醫事機構代碼','醫事機構名稱','電話', '地址', '固定看診時段','診療科別', '網址']]

def TypeRank(type=[],hospital=pd.read_json('../data/hospital.json')):
    type_dict={'胸腔內科':['內科'],'胸腔外科':['外科'],'腎臟科':['泌尿科','內科'],'血液腫瘤科':['外科','放射腫瘤科']}
    type.append('不分科')
    type.append('家醫科')
    for i in range(len(type)):
        try:
            type.append(type_dict[type[i]])
        except:
            pass
        if i ==0:
            bool=np.array(hospital['診療科別'].str.contains(type[i]))
            print(bool)
        else:
            search=np.array(hospital['診療科別'].str.contains(type[i]))

            bool=search | np.array(bool)
    hospital=hospital[bool]

    return hospital
#open_time()
#hospital()
#symptom()
#holiday()
#addresstran()
#hospital=DisRank((12,23))
#hospital=TypeRank(['胸腔內科'],hospital)
