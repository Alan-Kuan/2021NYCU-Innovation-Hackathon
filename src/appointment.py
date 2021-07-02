from linebot.models import (
    TextSendMessage, FlexSendMessage,
    ButtonsTemplate, TemplateSendMessage,
    PostbackEvent, PostbackTemplateAction
)

import json
import os
import datetime
import data_handler

divisionCode = json.load(open('./data/divisionCode.json', 'r', encoding='utf-8'))
inv_divisionCode = {v: k for k, v in divisionCode.items()}

def askForDivision(bot, token):
#    question = 'Please specify the division you want to make appointment.'
    division_flex = json.load(open('./flex_templates/division.json', 'r', encoding='utf-8'))
    flex_template = FlexSendMessage(
        alt_text = 'Asking for division.',
        contents = division_flex
    )
    bot.reply_message(token, flex_template)

def askForMoreDivision(bot, token):
#    question = 'Please specify the division you want to make appointment.'
    more_division_flex = json.load(open('./flex_templates/more_division.json', 'r', encoding='utf-8'))
    flex_template = FlexSendMessage(
        alt_text = 'Asking for more division.',
        contents = more_division_flex
    )
    bot.reply_message(token, flex_template)

def askForDate(bot, token, division_code):
    bot.reply_message(token, TextSendMessage(
        text='請問你要在哪一天掛號呢？',
        quick_reply={
            'items': [{
                'type': 'action',
                'action': {
                    'type': 'datetimepicker',
                    'label': '選日期',
                    'data': f'date-pick?division_code={division_code}',
                    'mode': 'date',
                    'min': datetime.date.today().isoformat()
                }
            }]
        }
    ))

def askForPeriod(bot, token, division_code,date):
    bot.reply_message(token, TextSendMessage(
        text='在一天的那個時段呢？',
        quick_reply={
            'items': [
                {
                    'type':'action',
                    'action':{
                        'type': 'postback',
                        'label': '早上',
                        'data': f'period-morning?division_code={division_code}&date={date}',
                        'text':'早上'
                    }
                },
                {
                    'type':'action',
                    'action':{
                        'type': 'postback',
                        'label': '下午',
                        'data': f'period-afternoon?division_code={division_code}&date={date}',
                        'text':'下午'
                    }
                },
                {
                    'type':'action',
                    'action':{
                        'type': 'postback',
                        'label': '晚上',
                        'data': f'period-night?division_code={division_code}&date={date}',
                        'text':'晚上'
                    }
                }
            ]
        }
    ))

def getLocation(bot, token, division_code, date, period):
    bot.reply_message(token, TextSendMessage(
        text='如果你願意提供所在位置，可以取得附近的醫療機構',
        quick_reply={
            'items': [
                {
                    'type': 'action',
                    'action': {
                        'type': 'location',
                        'label': '提供我的位置',
                        'data': f'loc-confirm?division_code={division_code}&date={date}&period={period}',
                    }
                },
                {
                    'type': 'action',
                    'action': {
                        'type': 'postback',
                        'label': '我不願提供',
                        'data': f'loc-deny?division_code={division_code}&date={date}&period={period}',
                    }
                }
            ]
        }
    ))

def getHospital(bot, token, division_code, date, period, loc):
    division = divisionCode[division_code]
    if loc is None:
        res = data_handler.TypeRank([division])
    else:
        res1 = data_handler.DisRank(loc)
        res = data_handler.TypeRank([division], res1)
    top6 = res.head(6)
    carousel_contents = []
    for _, row in top6.iterrows():
        card = json.load(open('../flex_templates/hospital.json', 'r', encoding='utf-8'))
        card['body']['contents'][0]['contents'][0]['text'] = row['醫事機構名稱']
        morning = []
        afternoon = []
        night = []
        for period in row['固定看診時段'].split('、'):
            if period[-2] == '看':
                if period[3:5] == '上午':
                    morning.append(period[2])
                elif period[3:5] == '下午':
                    afternoon.append(period[2])
                elif period[3:5] == '晚上':
                    night.append(period[2])
        open_hour = ''
        if len(morning) > 0:
            open_hour += '上午：' + '、'.join(morning) + '\n'
        if len(afternoon) > 0:
            open_hour += '下午：' + '、'.join(afternoon) + '\n'
        if len(night) > 0:
            open_hour += '晚上：' + '、'.join(night)
        card['body']['contents'][1]['contents'][1]['text'] = open_hour
        card['body']['contents'][2]['contents'][1]['text'] = row['電話']
        card['body']['contents'][3]['contents'][1]['text'] = row['地址']
        url = row['網址']
        if url is None:
            card['footer']['contents'][0] = {
                'type': 'text',
                'text': '由於資料庫沒有該機構的預約網址，請透過電話預約',
                'wrap': True
            }
        else:
            card['footer']['contents'][0]['action']['uri'] = url
        carousel_contents.append(card)
    hospital_flex = {
        'type': 'carousel',
        'contents': carousel_contents
    }
    bot.reply_message(token, FlexSendMessage(
        alt_text='Hositals near you.',
        contents=hospital_flex
    ))
