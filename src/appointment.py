from linebot.models import (
    TextSendMessage, FlexSendMessage,
    ButtonsTemplate, TemplateSendMessage,
    PostbackEvent, PostbackTemplateAction
)

import json
import os

divisionCode = json.load(open('../data/divisionCode.json', 'r', encoding='utf-8'))
inv_divisionCode = {v: k for k, v in divisionCode.items()}

def askForDivision(bot, token):
    question = 'Please specify the division you want to make appointment.'
    division_flex = json.load(open('../flex_templates/division.json', 'r', encoding='utf-8'))
    flex_template = FlexSendMessage(
        alt_text = 'Asking for division.',
        contents = division_flex
    )
    bot.reply_message(token, flex_template)

def askForMoreDivision(bot, token):
    question = 'Please specify the division you want to make appointment.'
    more_division_flex = json.load(open('../flex_templates/more_division.json', 'r', encoding='utf-8'))
    flex_template = FlexSendMessage(
        alt_text = 'Asking for more division.',
        contents = more_division_flex
    )
    bot.reply_message(token, flex_template)

def askForDate(bot, token, division_code):
    pass
<<<<<<< HEAD

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
=======
>>>>>>> 26c36ab9bd954c1caea63a3803936acb42e8f6e5
