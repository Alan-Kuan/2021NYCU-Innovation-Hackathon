import json
import asyncio
import database as db

from linebot.models import (
    TextSendMessage,
    ButtonsTemplate, CarouselTemplate, CarouselColumn, TemplateSendMessage,
    FlexSendMessage,
    PostbackEvent, PostbackTemplateAction
)

parts = [
  '頭部',           '眼睛',
  '耳',             '鼻',
  '口咽喉',         '頸部',
  '胸肺',           '背部',
  '腹部',           '泌尿系統',
  '生殖系統',       '骨骼肌肉',
  '精神系統',       '皮膚',
  '一般症狀',       '乳房',
  '其他'
]

def askForPart(bot, token, symptom_data):
    parts_flex = json.load(open('../flex_templates/parts.json', 'r', encoding='utf-8'))
    if len(symptom_data) > 0:
        parts_flex['contents'][0]['body']['contents'][0]['text'] = '還有哪裡不舒服嗎？'
        parts_flex['contents'][1]['body']['contents'].append({
            'type': 'button',
            'action': {
              'type': 'postback',
              'label': '沒有',
              'data': f'part-no?symptom_data={str(symptom_data)}',
              'displayText': '沒有'
            },
            'color': '#35827F'
        })
    for card in parts_flex['contents']:
        for item in card['body']['contents']:
            if item['type'] == 'box':
                for btn in item['contents']:
                    btn['action']['data'] += f'?symptom_data={str(symptom_data)}'
    bot.reply_message(token, FlexSendMessage(
        alt_text='Asking for parts you feel not well.',
        contents=parts_flex
    ))

def askForSymptom(bot, token, part_idx, symptom_data):
    question = 'Which symptom best describe your ailment?'
    symptoms = db.getSymptom(parts[part_idx])
    print(symptoms)
    flex_contents = []
    for batch in range((len(symptoms) - 1) // 8 + 1):
        i = batch * 8
        card = {
          "type": "bubble",
          "size": "kilo",
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "請問哪個是你的症狀？",
                "size": "xl",
                "align": "start",
                "weight": "bold",
                "offsetBottom": "md",
                "margin": "md",
                "color": "#87CECB"
              },
              {
                "type": "separator"
              }
            ]
          }
        }
        no_items = False
        for j in range(4):
            if no_items:
                break
            row_contents = []
            for k in range(2):
                idx = i + j*2 + k
                if idx >= len(symptoms):
                    no_items = True
                    break
                S = symptoms[idx][0]
                print(S)
                row_contents.append({
                    "type": "button",
                    "action": {
                      "type": "postback",
                      "label": S,
                      "data": f"symptom-{S}?symptom_data={symptom_data}",
                      "displayText": S
                    },
                    "color": "#35827F"
                })
            row = {
                "type": "box",
                "layout": "horizontal",
                "contents": row_contents
            }
            card['body']['contents'].append(row)
        flex_contents.append(card)
    symptoms_flex = {
      "type": "carousel",
      "contents": flex_contents
    }
    bot.reply_message(token, FlexSendMessage(
        alt_text='Asking for your symptoms.',
        contents=symptoms_flex
    ))

def suggest(bot, token, symptom_data):
    bot.reply_message(token, TextSendMessage(text=f'Your symptoms: {str(symptom_data)}'))
