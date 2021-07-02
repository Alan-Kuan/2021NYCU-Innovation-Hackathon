
def showReminders(bot, token):
    question = 'Please specify the division you want to make appointment.'
    more_division_flex = json.load(open('../flex_templates/reminder.json', 'r', encoding='utf-8'))
    flex_template = FlexSendMessage(
        alt_text = 'Show the options to remind.',
        contents = more_division_flex
    )
    bot.reply_message(token, flex_template)
