import json

from linebot.models import (
    TextSendMessage, FlexSendMessage
)

def showReminders(bot, token):
    contact_flex = json.load(open('../flex_templates/contact.json', 'r', encoding='utf-8'))
    flex_template = FlexSendMessage(
        alt_text = 'Show the options to remind.',
        contents = contact_flex
    )
    bot.reply_message(token, flex_template)

def sendRandomCode(bot, token, randCode):
    msg = '請複製以下後送給緊急聯絡人的Line，並請他:\n';
    msg+= '1.點擊Reminder，2.點擊Enter Code，\n 3.依照指示輸入隨機碼。\n'
    msg+= f'您的隨機碼：{str(randCode)}';
    bot.reply_message(token, TextSendMessage(text=msg))
