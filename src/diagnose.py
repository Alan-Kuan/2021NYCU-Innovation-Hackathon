from linebot.models import (
    TextSendMessage,
    ButtonsTemplate, TemplateSendMessage,
    PostbackEvent, PostbackTemplateAction
)

def askForPart(bot, token, sympton_data):
    question = 'Which part do you feel not well?' if len(sympton_data) == 0 else \
               f'Other than {str(sympton_data)[1:-1]}, is there any part you feel not well?'
    actions = [
        PostbackTemplateAction(
            label='Head',
            data=f'part-head?sympton_data={str(sympton_data)}'
        ),
        PostbackTemplateAction(
            label='Eyes',
            data=f'part-eyes?sympton_data={str(sympton_data)}'
        ),
        PostbackTemplateAction(
            label='Ears',
            data=f'part-ears?sympton_data={str(sympton_data)}'
        )
    ]
    if len(sympton_data) > 0:
        actions.insert(0,
            PostbackTemplateAction(
                label='No',
                data=f'part-no?sympton_data={str(sympton_data)}'
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

def askForSympton(bot, token, sympton_data):
    question = 'Which sympton best describe your ailment?'
    actions = [
        PostbackTemplateAction(
            label='Headache',
            data=f'sympton-headache?sympton_data={str(sympton_data)}',
        ),
        PostbackTemplateAction(
            label='Dizzy',
            data=f'sympton-dizzy?sympton_data={str(sympton_data)}'
        ),
        PostbackTemplateAction(
            label='Nausia',
            data=f'sympton-nausia?sympton_data={str(sympton_data)}'
        )
    ]
    buttons_template = TemplateSendMessage(
        alt_text='Asking for symptons.',
        template=ButtonsTemplate(
            text=question,
            actions=actions
        )
    )
    bot.reply_message(token, buttons_template)

def suggest(bot, token, sympton_data):
    bot.reply_message(token, TextSendMessage(text=f'Your symptons: {str(sympton_data)}'))
