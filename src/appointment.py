from linebot.models import (
    TextSendMessage, FlexSendMessage,
    ButtonsTemplate, TemplateSendMessage,
    PostbackEvent, PostbackTemplateAction
)

import json
import os

divisionCode = {
    '01' : '家醫科',
    '02' : '內科',
    '03' : '外科',
    '04' : '小兒科',
    '05' : '婦產科',
    '06' : '骨科',
    '07' : '神經外科',
    '08' : '泌尿科',
    '09' : '耳鼻喉科',
    '10' : '眼科',
    '11' : '皮膚科',
    '12' : '神經科',
    '13' : '精神科',
    '14' : '復健科',
    '15' : '整型外科',
    '22' : '急診醫學科',
    '40' : '牙科',
    '60' : '中醫科',
    '81' : '麻醉科',
    '82' : '放射線科',
    '83' : '病理科',
    '84' : '核醫科',
    '2A' : '結核科',
    '2B' : '洗腎科',
    
    'AA' :  '腸胃內科',
    'AB' :  '心臟血管內科',
    'AC' :  '胸腔內科',
    'AD' :  '腎臟內科',
    'AE' :  '風濕免疫科',
    'AF' :  '血液腫瘤科',
    'AG' :  '內分泌科',
    'AH' :  '感染科',
    'AI' :  '潛醫科',
    'AJ' :  '胸腔暨重症加護',
    'BA' :  '直腸外科',
    'BB' :  '心臟血管外科',
    'BC' :  '胸腔外科',
    'BD' :  '消化外科',
    'CA' :  '小兒外科',
    'CB' :  '新生兒科',
    'DA' :  '疼痛科',
    'EA' :  '居家護理',
    'FA' :  '放射診斷科',
    'FB' :  '放射腫瘤科',
    'GA' :  '口腔顏面外科',
    'HA' :  '脊椎骨科',
}

inv_divisionCode = {v: k for k, v in divisionCode.items()}

def askForDivision(bot, token, division_data):
    question = 'Please specify the division you want to make appointment.'
    division_flex = json.load(open('../flex_templates/division.json', 'r', encoding='utf-8'))
    flex_template = FlexSendMessage(
        alt_text = 'Ask for division.',
        contents = division_flex
    )
    bot.reply_message(token, flex_template)

def askForMoreDivision(bot, token, division_data):
    question = 'Please specify the division you want to make appointment.'
    more_division_flex = json.load(open('../flex_templates/more_division.json', 'r', encoding='utf-8'))
    flex_template = FlexSendMessage(
        alt_text = 'Ask for more division.',
        contents = more_division_flex
    )
    bot.reply_message(token, flex_template)

def askForTime(bot, token, division_code,date):
    bot.reply_message(token, TextSendMessage(
        text='在一天的那個時段呢？',
        quick_reply={
            'items':[{
                'type':'action',
                'action':{
                    'type': 'postback',
                    'label': '早上',
                    'data': f'period-morning?division_code={division_code}&date={date}',
                    'text':'早上' 
                },
                {
                'type':'action',
                'action':{
                    'type': 'postback',
                    'label': '下午',
                    'data': f'period-afternoonperiod-morning?division_code={division_code}&date={date}',
                    'text':'下午' 
                },
                {
                'type':'action',
                'action':{
                    'type': 'postback',
                    'label': '晚上',
                    'data': f'period-nightperiod-morning?division_code={division_code}&date={date}',
                    'text':'晚上' 
                }
            }]
        }