from linebot.models import (
    TextSendMessage, FlexSendMessage,
    ButtonsTemplate, TemplateSendMessage,
    PostbackEvent, PostbackTemplateAction
)

import json
import os
import datetime

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
