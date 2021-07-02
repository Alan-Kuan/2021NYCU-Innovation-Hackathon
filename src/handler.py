import os
import ast
import json
import hashlib
import richmenu, diagnose, appointment, reminder
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
    PostbackEvent, PostbackTemplateAction
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
            reminder.showReminders(bot, event.reply_token)

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
            appointment.askForDate(bot, event.reply_token, data)

    #On Date Select
    elif type == 'date':
        date = event.postback.params['date'].replace('-', '/')
        appointment.askForPeriod(bot, event.reply_token, query['division_code'][0], date)

    # On Period Select
    elif type == 'period':
        division_code = query['division_code'][0]
        date = query['date'][0]
        period_dict = {
            'morning': '早上',
            'afternoon': '下午',
            'night': '晚上'
        }
        period = period_dict[data]
        bot.reply_message(event.reply_token, TextSendMessage(
            text=f'你打算在{date}{period}時段預約{division_code}'
        ))

    elif type == 'contact':
        #user = bot.get_profile(event.source.user_id)
        user = event.source.user_id
        print(user)
        if data == 'add':
            randCode = int(hashlib.sha256(user.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
            while(db.addCom(user, str(randCode))==False):
                randCode = randCode + 1
            reminder.sendRandomCode(bot, event.reply_token, randCode)
        elif data == 'code':
            pass

if __name__ == "__main__":
    app.run(debug=True)
