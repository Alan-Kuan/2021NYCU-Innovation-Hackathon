from linebot.models import (
    TextSendMessage,
    ButtonsTemplate, TemplateSendMessage,
    PostbackEvent, PostbackTemplateAction
)

def askForDivision(bot, token):
    bot.reply_message(token, TextSendMessage(text='which division'))
