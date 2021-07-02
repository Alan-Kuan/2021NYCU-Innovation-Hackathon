import os

if os.getenv('DEVELOPMENT') is not None:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='../.env')

import sys

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent, PostbackEvent, TextMessage, TextSendMessage
)
from linebot.models.actions import (
    PostbackAction, MessageAction, URIAction
)
from linebot.models.rich_menu import (
    RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds
)


app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET')  or 'YOUR_SECRET'
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')  or 'YOUR_ACCESS_TOKEN'

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    #debug
    print(channel_access_token)
    print(channel_secret)
    
    # handle webhook body
    try:
        handler.handle(body, signature)        
    except InvalidSignatureError:
        abort(400)
    return 'OK'


    
# Rich Menu Example
@handler.add(FollowEvent)
def handle_follow():
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name="Medical Assistant Richmenu",
        chat_bar_text="Need help?",
        areas=[RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
            action=PostbackAction(label='diagnose',data='menu-diagnose')),
            RichMenuArea(
                bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                action=PostbackAction(label='Appointment',data='menu-appointment')),
            RichMenuArea(
                bounds=RichMenuBounds(x=833*2, y=0, width=833, height=843),
                action=PostbackAction(label='Reminder',data='menu-reminder')),
            ]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    content_type = "image/png"
    with open('richmenu-template-guide-01.0ca7294f.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)
    print(rich_menu_id)
    line_bot_api.set_default_rich_menu(rich_menu_id)

# PostbackEvent
@handler.add(PostbackEvent)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.postback.data)
    )

# Echo function
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

# CSV Example
# import csv
# @handler.add(MessageEvent, message=TextMessage)
# def message_text(event):
#     rows_list = []
#     with open(os.path.abspath("maskdata.csv"), newline='') as csvfile:
#         rows = csv.reader(csvfile, delimiter=',')
#         for row in rows:
#             rows_list.append(row)
#
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=str(rows_list[1]))
#     )

# @handler.add(MessageEvent, message=TextMessage)
# def message_text(event):
#     print(event)
#     user = line_bot_api.get_profile(event.source.user_id)
#     print("!!!!!!!!!!!!!!!!!")
#     print(user)
#     print("!!!!!!!!!!!!!!!!!")
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextMessage(text=f'Hello {user.display_name}, your image url is {user.picture_url}')
#     )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
