import json
import datetime
from src import database as db
from linebot.models import (
    TextMessage, TextSendMessage, FlexSendMessage
)

def showReminders(bot, token, user_id):
    if db.CheckCom(user_id)==False:
        contact_flex = json.load(open('./flex_templates/contact.json', 'r', encoding='utf-8'))
    else:
        contact_flex = json.load(open('./flex_templates/linked_contact.json', 'r', encoding='utf-8'))
    flex_template = FlexSendMessage(
        alt_text = 'Show the options to remind.',
        contents = contact_flex
    )
    bot.reply_message(token, flex_template)

# ==== Emergency Contact ==== #
def sendRandomCode(bot, token, randCode):
    RandCode_flex = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_3_movie.png",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
            {
                "type": "text",
                "text": "Your Random Code",
                "wrap": True,
                "weight": "bold",
                "gravity": "center",
                "size": "xl",
                "align": "center"
            },
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": f'{randCode}',
                    "wrap": True,
                    "color": "#47d685",
                    "size": "xxl",
                    "flex": 4,
                    "position": "relative",
                    "align": "center",
                    "weight": "bold",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": f'{randCode}'
                    }
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "xs",
                "contents": [
                {
                    "type": "text",
                    "text": "??????????????????????????????",
                    "size": "xs"
                },
                {
                    "type": "text",
                    "text": "????????????????????????Line????????????:",
                    "size": "xs"
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "1. ??????Reminder???",
                    "size": "xs"
                },
                {
                    "type": "text",
                    "text": "2. ?????? Emergency Contact Person???",
                    "wrap": True,
                    "size": "xs"
                },
                {
                    "type": "text",
                    "text": "?????? Enter Code???",
                    "offsetStart": "xl",
                    "size": "xs"
                },
                {
                    "type": "text",
                    "text": "3.??????????????????????????????",
                    "size": "xs",
                    "margin": "none"
                }
                ],
                "margin": "xs",
                "spacing": "xs"
            }
            ]
        }
    }
    flex_template = FlexSendMessage(
        alt_text = f'Your Random Code:{randCode}',
        contents = RandCode_flex
    )
    bot.reply_message(token, flex_template)

def requestRandCode(bot, token, user_id):
    msg = "?????????????????????"
    bot.reply_message(token, TextSendMessage(text=msg))
    db.setSession(user_id, 'rc_req', True)


def comfirmRandCode(bot, token, user_id, randCode):
    authenticate = db.ConfirmCom(user_id,randCode)
    if authenticate == True :
        response = "??????????????????????????????"
    else:
        response = "????????????????????????????????????????????????"
    bot.reply_message(
        token,
        TextSendMessage(text=response)
    )
    db.setSession(user_id, 'rc_req', False)

def deleteContact(bot, token, user_id):
    done=db.DelCom(user_id)
    if done == True:
        msg ="?????????????????????"
    else:
        msg ="?????????????????????"
    bot.reply_message(
        token,
        TextMessage(text=msg)
    )

# ==== In-take reminder ==== #
def askForMed(bot, token):
    bot.reply_message(token, TextSendMessage(text='??????????????????????????????????????????'))

def askForMedTime(bot, token, med):
    bot.reply_message(token, TextSendMessage(
        text='???????????????????????????',
        quick_reply={
            'items': [
                {
                    'type': 'action',
                    'action': {
                        'type': 'postback',
                        'label': '??????',
                        'data': f'intake-morning?med={med}'
                    }
                },
                {
                    'type': 'action',
                    'action': {
                        'type': 'postback',
                        'label': '??????',
                        'data': f'intake-noon?med={med}'
                    }
                },
                {
                    'type': 'action',
                    'action': {
                        'type': 'postback',
                        'label': '??????',
                        'data': f'intake-evening?med={med}'
                    }
                },
                {
                    'type': 'action',
                    'action': {
                        'type': 'postback',
                        'label': '??????',
                        'data': f'intake-night?med={med}'
                    }
                }
            ]
        }
    ))

def askForMedEnd(bot, token, med, time):
    bot.reply_message(token, TextSendMessage(
        text='????????????????????????',
        quick_reply={
            'items': [{
                'type': 'action',
                'action': {
                    'type': 'datetimepicker',
                    'label': '?????????',
                    'data': f'intake-end?med={med}&time={time}',
                    'mode': 'date',
                    'min': datetime.date.today().isoformat()
                }
            }]
        }
    ))
