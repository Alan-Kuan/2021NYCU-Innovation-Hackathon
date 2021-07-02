from linebot.models import (
    TextSendMessage, FlexSendMessage,
    ButtonsTemplate, TemplateSendMessage,
    PostbackEvent, PostbackTemplateAction
)

import json
import os

divisionCode = json.load(open('../data/divisionCode.json', 'r', encoding='utf-8'))
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
