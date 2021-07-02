from linebot.models import (
    RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds,
    PostbackAction
)

# Rich Menu
def Rich_Menu_create(bot):
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
    rich_menu_id = bot.create_rich_menu(rich_menu=rich_menu_to_create)
    content_type = "image/png"
    with open('../images/rich_menu.png', 'rb') as f:
        bot.set_rich_menu_image(rich_menu_id, content_type, f)
    print(rich_menu_id)
    bot.set_default_rich_menu(rich_menu_id)
