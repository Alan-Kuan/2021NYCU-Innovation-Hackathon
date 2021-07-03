import os
import ast
import json
import hashlib

import richmenu, diagnose, appointment
import reminder, reminder_handler

import database as db

from dotenv import load_dotenv
from flask import Flask, request, abort
from urllib.parse import parse_qs

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent,
    MessageEvent, TextMessage, TextSendMessage,
    ButtonsTemplate, TemplateSendMessage,
    PostbackEvent, PostbackTemplateAction,
    LocationMessage
)

load_dotenv()

app = Flask(__name__)

bot = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(FollowEvent)
def handle_follow():
    richmenu.Rich_Menu_create(bot)

@handler.add(MessageEvent, message=LocationMessage)
def onSendLocation(event):
    msg = event.message
    user_id = event.source.user_id
    loc = (msg.latitude, msg.longitude)
    division_code = db.getSessionData(user_id, 'division_code')[0][0][0]
    date = db.getSessionData(user_id, 'date')[0][0][0]
    period = db.getSessionData(user_id, 'period')[0][0][0]
    appointment.getHospital(bot, event.reply_token, division_code, date, period, loc)

@handler.add(PostbackEvent)
def onPostback(event):
    user_id = event.source.user_id
    tokens = event.postback.data.split('-')
    type = tokens[0]
    tokens2 = tokens[1].split('?')
    data = tokens2[0]
    query = []
    if len(tokens2) > 1:
        query = parse_qs(tokens2[1])

    # On Menu Click
    if type == 'menu':
        if data == 'diagnose':
            #session.setSessionData(user_id, 'progress', 'diagnose')
            diagnose.askForPart(bot, event.reply_token, [])
        elif data == 'appointment':
            appointment.askForDivision(bot, event.reply_token)
        elif data == 'reminder':
            reminder.showReminders(bot, event.reply_token, event.source.user_id)

    # On Part Select
    elif type == 'part':
        symptom_data = ast.literal_eval(query['symptom_data'][0])
        if data == 'no':
            diagnose.suggest(bot, event.reply_token, symptom_data)
        else:
            diagnose.askForSymptom(bot, event.reply_token, int(data), symptom_data)

    # On Symptom Select
    elif type == 'symptom':
        symptom_data = ast.literal_eval(query['symptom_data'][0])
        symptom_data.append(data)
        if len(symptom_data) >= 3:
            diagnose.suggest(bot, event.reply_token, symptom_data)
        else:
            diagnose.askForPart(bot, event.reply_token, symptom_data)

    #On Division Select
    elif type == 'division':
        if data == 'more':
            appointment.askForMoreDivision(bot, event.reply_token)
        else:
            db.setSession(user_id, 'division_code', data)
            appointment.askForDate(bot, event.reply_token)

    #On Date Select
    elif type == 'date':
        date = event.postback.params['date']
        db.setSession(user_id, 'date', date)
        appointment.askForPeriod(bot, event.reply_token)

    # On Period Select
    elif type == 'period':
        db.setSession(user_id, 'period', data)
        appointment.getLocation(bot, event.reply_token)

    # On Location Select
    elif type == 'loc':
        division_code = db.getSessionData(user_id, 'division_code')[0][0][0]
        date = db.getSessionData(user_id, 'date')[0][0][0]
        period = db.getSessionData(user_id, 'period')[0][0][0]
        appointment.getHospital(bot, event.reply_token, division_code, date, period, None)

    elif type == 'contact':
        #user = bot.get_profile(event.source.user_id)
        user = event.source.user_id
        print(user)
        if data == 'add':
            randCode = int(hashlib.sha256(user.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
            com_status=db.addCom(user, str(randCode))
            while com_status=='code repeat':
                randCode = randCode + 1
                com_status=db.addCom(user, str(randCode))
            reminder.sendRandomCode(bot, event.reply_token, randCode)
        elif data == 'code':
            reminder.requestRandCode(bot, event.reply_token, user)
        elif data == 'remove':
            reminder.deleteContact(bot, event.reply_token, user)

    elif type == 'intake':
        if data == 'edit':
            period_dict = {
                'morning': '早上',
                'noon': '中午',
                'evening': '下午',
                'night': '晚上'
            }
            remind_list, _ = reminder_handler.get_med_reminder(mode='by user', user_id=user_id)
            reply_list = ''
            for idx, row in enumerate(remind_list):
                reply_list += f'{idx + 1}. {row[3].isoformat()} {period_dict[row[2]]}: {row[1]}\n'
            bot.reply_message(event.reply_token, TextSendMessage(
                text=reply_list,
                quick_reply={
                    'items': [
                        {
                            'type': 'action',
                            'action': {
                                'type': 'postback',
                                'data': 'intake-del',
                                'label': '我要移除某項'
                            }
                        },
                        {
                            'type': 'action',
                            'action': {
                                'type': 'postback',
                                'data': 'intake-no_problem',
                                'label': '沒有問題'
                            }
                        },
                    ]
                }
            ))
        elif data == 'del':
            db.setSession(user_id, 'del_req', 'True')
            bot.reply_message(event.reply_token, TextSendMessage(text='請告訴我編號'))
        elif data == 'no_problem':
            db.setSession(user_id, 'del_req', 'False')
            bot.reply_message(event.reply_token, TextSendMessage(text='太好了！'))
        elif data == 'on':
            db.setSession(user_id, 'intake-reminder', 'on')
            db.setSession(user_id, 'md_req', 'True')
            reminder.askForMed(bot, event.reply_token)
        elif data == 'off':
            db.setSession(user_id, 'intake-reminder', 'off')
        elif data == 'end':
            med = query['med'][0]
            time = query['time'][0]
            end = event.postback.params['date'].replace('-', '/')
            reminder_handler.add_med_reminder(user_id, time, med, end)
            bot.reply_message(event.reply_token, TextSendMessage(
                text='還要再新增提醒嗎？',
                quick_reply={
                    'items': [
                        {
                            'type': 'action',
                            'action': {
                                'type': 'postback',
                                'label': '是',
                                'data': 'intake-yes'
                            }
                        },
                        {
                            'type': 'action',
                            'action': {
                                'type': 'postback',
                                'label': '否',
                                'data': 'intake-no'
                            }
                        }
                    ]
                }
            ))
        elif data == 'yes':
            reminder.askForMed(bot, event.reply_token)
        elif data == 'no':
            db.setSession(user_id, 'md_req', 'False')
            bot.reply_message(event.reply_token, TextSendMessage(text='已新增完畢'))
        else:  # morning, afternoon, night
            med = query['med'][0]
            reminder.askForMedEnd(bot, event.reply_token, med, data)

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    msg = event.message.text
    user = event.source.user_id
    cur_session = db.getSessionKey(user)
    cur_session = cur_session[0]
    # Session Controls
    print(cur_session)
    found=False
    for cur in cur_session:
        if "rc_req" in cur:
            found = True
            break
    md_req, md_req_exists = db.getSessionData(user, 'md_req')
    del_req, del_req_exists = db.getSessionData(user, 'del_req')

    # Session Controls
    if found and db.getSessionData(user, "rc_req")[0][0][0] == 'True':
        reminder.comfirmRandCode(bot, event.reply_token,user, msg)
    elif md_req_exists and md_req[0][0] == 'True':
        reminder.askForMedTime(bot, event.reply_token, msg)
    elif del_req_exists and del_req[0][0] == 'True':
        if not msg.isnumeric():
            bot.reply_message(event.reply_token, TextSendMessage(text='請輸入數字喔'))
            return
        idx = int(msg) - 1
        remind_list, _ = reminder_handler.get_med_reminder(mode='by user', user_id=user)
        print(remind_list)
        time = remind_list[idx][2]
        content = remind_list[idx][1]
        reminder_handler.del_med_reminder(user, time, content)
        remind_list, _ = reminder_handler.get_med_reminder(mode='by user', user_id=user)
        period_dict = {
            'morning': '早上',
            'noon': '中午',
            'evening': '下午',
            'night': '晚上'
        }
        reply_list = ''
        for idx, row in enumerate(remind_list):
            reply_list += f'{idx + 1}. {row[3].isoformat()} {period_dict[row[2]]}: {row[1]}\n'
        bot.reply_message(event.reply_token, TextSendMessage(
            text=reply_list,
            quick_reply={
                'items': [
                    {
                        'type': 'action',
                        'action': {
                            'type': 'postback',
                            'data': 'intake-del',
                            'label': '我要移除某項'
                        }
                    },
                    {
                        'type': 'action',
                        'action': {
                            'type': 'postback',
                            'data': 'intake-no_problem',
                            'label': '沒有問題'
                        }
                    },
                ]
            }
        ))
    #else:
    #    unknown='未知訊息。點擊主選單以獲得更多功能。'
    #    bot.reply_message(
    #        event.reply_token,
    #        TextMessage(text=unknown)
    #    )

if __name__ == "__main__":
    app.run(debug=True)
    reminder_handler.remind_event(bot)
    while True:
        schedule.run_pending()
        time.sleep(300)
