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
    '2B' : '洗腎科'
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
