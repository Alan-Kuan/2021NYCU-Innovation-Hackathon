from linebot.models import (
    TextSendMessage,
    ButtonsTemplate, TemplateSendMessage,
    PostbackEvent, PostbackTemplateAction
)

def askForPart(bot, token, symptom_data):
    question = 'Which part do you feel not well?' if len(symptom_data) == 0 else \
               f'Other than {str(symptom_data)[1:-1]}, is there any part you feel not well?'
    actions = [
        PostbackTemplateAction(
            label='Head',
            data=f'part-head?symptom_data={str(symptom_data)}'
        ),
        PostbackTemplateAction(
            label='Eyes',
            data=f'part-eyes?symptom_data={str(symptom_data)}'
        ),
        PostbackTemplateAction(
            label='Ears',
            data=f'part-ears?symptom_data={str(symptom_data)}'
        )
    ]
    if len(symptom_data) > 0:
        actions.insert(0,
            PostbackTemplateAction(
                label='No',
                data=f'part-no?symptom_data={str(symptom_data)}'
            )
        )
    buttons_template = TemplateSendMessage(
        alt_text='Asking for parts you feel not well.',
        template=ButtonsTemplate(
            text=question,
            actions=actions
        )
    )
    bot.reply_message(token, buttons_template)

def askForSymptom(bot, token, symptom_data):
    question = 'Which symptom best describe your ailment?'
    actions = [
        PostbackTemplateAction(
            label='Headache',
            data=f'symptom-headache?symptom_data={str(symptom_data)}',
        ),
        PostbackTemplateAction(
            label='Dizzy',
            data=f'symptom-dizzy?symptom_data={str(symptom_data)}'
        ),
        PostbackTemplateAction(
            label='Nausia',
            data=f'symptom-nausia?symptom_data={str(symptom_data)}'
        )
    ]
    buttons_template = TemplateSendMessage(
        alt_text='Asking for symptoms.',
        template=ButtonsTemplate(
            text=question,
            actions=actions
        )
    )
    bot.reply_message(token, buttons_template)

def suggest(bot, token, symptom_data):
    bot.reply_message(token, TextSendMessage(text=f'Your symptoms: {str(symptom_data)}'))
