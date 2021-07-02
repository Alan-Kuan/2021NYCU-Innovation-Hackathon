import os
import ast
import richmenu, diagnose, appointment
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
            pass

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

    #On Time Select
    elif type == 'date':
        division_data = ast.literal_eval(query['division_data'][0])
        division_data.append(data)

if __name__ == "__main__":
    app.run(debug=True)
