import json
import database as db
from linebot.models import (
    TextSendMessage, FlexSendMessage
)

def showReminders(bot, token):
    if db.()==False:
        contact_flex = json.load(open('./flex_templates/contact.json', 'r', encoding='utf-8'))
    else:
        contact_flex = json.load(open('./flex_templates/linked_contact.json', 'r', encoding='utf-8'))
    flex_template = FlexSendMessage(
        alt_text = 'Show the options to remind.',
        contents = contact_flex
    )
    bot.reply_message(token, flex_template)

def sendRandomCode(bot, token, randCode):
    msg = '請複製以下後送給緊急聯絡人的Line，並請他:\n';
    msg+= '1.點擊Reminder，\n2.點擊Enter Code，\n3.依照指示輸入隨機碼。\n'
    msg+= f'您的隨機碼：{str(randCode)}';
    bot.reply_message(token, TextSendMessage(text=msg))

def requestRandCode(bot, token, user_id):
    msg = "請輸入隨機碼："
    bot.reply_message(token, TextSendMessage(text=msg))
    db.setSession(user_id, 'rc_req', True)

def comfirmRandCode(bot, token, user_id, randCode):
    authenticate = ConfirmCom(user_id,randCode)
    if authenticate == True :
        response = "添加緊急聯絡人成功！"
    else:
        response = "隨機碼錯誤，添加緊急聯絡人失敗。"
    bot.reply_message(
        token,
        TextMessage(text=response)
    )
    db.setSession(user_id, 'rc_req', False)
