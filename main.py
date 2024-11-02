from telegram.ext import ApplicationBuilder, ContextTypes, CallbackContext, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from configuration import TELEGRAM_TOKEN


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Следуйте инструкциям.\n\n", parse_mode="Markdown")
    if ("step" not in context.user_data or context.user_data['step'] == 'name'):
        await update.message.reply_text("Введите ваше имя:")
    elif context.user_data['step'] == 'birthday_day':
        await update.message.reply_text("Введите день рождения:")
    elif context.user_data['step'] == 'birthday_month':
        await update.message.reply_text("Введите месяц рождения:")
    elif context.user_data['step'] == 'press_button':
        await update.message.reply_text("Просто нажмите на кнопку с тортиком......")
    elif context.user_data['step'] == 'cake':
        if 'restart' in context.user_data:
            await update.message.reply_text("GG")
            await update.message.reply_text("/restart123", parse_mode='Markdown')
            await update.message.reply_text("/sus", parse_mode='Markdown')
        else:
            await update.message.reply_text("Ааааааааааууууеееее вы прошли игру. Но что если все сломать...")
            await update.message.reply_text("/restart123", parse_mode='Markdown')


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Приветики, это супер бот")

    if 'step' not in context.user_data:
        context.user_data['step'] = 'name'
        context.user_data['attempts'] = 0
        await update.message.reply_text("Введите ваше имя:")
    elif context.user_data['step'] == 'cake':
        await update.message.reply_text("Именинник 🤭")
    else:
        await update.message.reply_text("Заблудились? Жмите /help", parse_mode="Markdown")



WRONG = "Ответ неправильный"
CORRECT = "Правильно"

# Обработчик сообщений пользователя
async def handle_message(update: Update, context: CallbackContext) -> None:
    if 'step' not in context.user_data:
        context.user_data['step'] = 'name'
        context.user_data['attempts'] = 0

    step = context.user_data['step']
    message_text = str.lower(update.message.text)

    if step == 'name':
        if (message_text == "артем"):
            await update.message.reply_text(CORRECT)
            await update.message.reply_text("Введите день рождения:")
            context.user_data['step'] = 'birthday_day'
            context.user_data['attempts'] = 0
        else:
            context.user_data['attempts'] += 1
            await update.message.reply_text(WRONG)
            if context.user_data['attempts'] == 3:
                await update.message.reply_text("Подсказка: А****")
            if context.user_data['attempts'] == 4:
                await update.message.reply_text("Подсказка: А**е*")
            if context.user_data['attempts'] == 7:
                await update.message.reply_text("Помянем... Ладно, Артем, проехали...")
                await update.message.reply_text("Введите день рождения:")
                context.user_data['step'] = 'birthday_day'
                context.user_data['attempts'] = 0

    elif step == 'birthday_day':
        if (message_text == "1" or message_text == "01" or message_text == "первого" or message_text == "один" or message_text == "первое"):
            await update.message.reply_text(CORRECT)
            await update.message.reply_text("Введите месяц рождения:")
            context.user_data['step'] = 'birthday_month'
            context.user_data['attempts'] = 0
        else:
            if (context.user_data['attempts'] == 0):
                context.user_data['attempts'] += 1
                await update.message.reply_text(WRONG)
                await update.message.reply_text("Кажется вы забыли день своего рождения. Не осуждаем. Напомним: первое")
            else:
                await update.message.reply_text(WRONG)
                await update.message.reply_text("Вы dur... Ладно....")
                await update.message.reply_text("Введите месяц рождения:")
                context.user_data['step'] = 'birthday_month'
                context.user_data['attempts'] = 0

    elif step == 'birthday_month':
        if (message_text == "11" or message_text == "ноябрь" or message_text == "ноября" or message_text == "первое"):
            await update.message.reply_text(CORRECT)
            step = 'cake'
            context.user_data['step'] = step
            context.user_data['attempts'] = 0
        else:
            if (context.user_data['attempts'] == 0):
                context.user_data['attempts'] += 1
                await update.message.reply_text(WRONG)
                await update.message.reply_text("Кажется вы забыли месяц своего рождения. Не осуждаем. Напомним: ноя**ь")
            else:
                await update.message.reply_text(WRONG)
                await context.bot.send_photo(chat_id=update.message.chat_id, photo=open('dur.jpg', 'rb'))
                await update.message.reply_text("НОЯБРЬ!!! ПЕРВОЕ НОЯБРЯ!!")
                context.user_data['step'] = 'press_button'
                context.user_data['attempts'] = 0
                await cake_button(update, context)

    elif step == 'press_button':
        context.user_data['attempts'] += 1
        if context.user_data['attempts'] % 2:
            await update.message.reply_text("Жми!!")
        if not context.user_data['attempts'] % 2:
            await update.message.reply_text("Не тупи, сникерсни")
        if not context.user_data['attempts'] % 3:
            await cake_button(update, context)

    if step == 'cake':
        context.user_data['attempts'] += 1
        await update.message.reply_text("С ДЭРЭЭЭЭЭЭЭЭ " + str(context.user_data['attempts']) + " 🎉")
        await context.bot.send_sticker(chat_id=context._user_id, sticker="CAACAgQAAxkBAAPmZyUsJq09pfFqXXvyQTV_F3Ns_3oAAp0AA845CA3b09W6-b0_FDYE")
            

async def cake_button(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Перекус? 🍰", callback_data="cake")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Вы наверное просто устали.', reply_markup=reply_markup, parse_mode='Markdown')



async def cake(update: Update, context: CallbackContext, choice=None):
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        choice = query.data
    else:
        query = update.message
        choice = choice or query.text[1:]

    context.user_data['step'] = 'cake'
    context.user_data['attempts'] = 0
    await query.edit_message_text("С ДЭЭЭЭЭРЭЭЭЭЭЭЭЭ 🎉")
    await context.bot.send_sticker(chat_id=context._user_id, sticker="CAACAgQAAxkBAAPmZyUsJq09pfFqXXvyQTV_F3Ns_3oAAp0AA845CA3b09W6-b0_FDYE")


# Обработчик сообщений пользователя
async def test(update: Update, context: CallbackContext) -> None:
    print(update.message.sticker.file_id)


async def restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Начинаем заново 😈")
    await context.bot.send_sticker(chat_id=context._user_id, sticker="CAACAgIAAxkBAAIC0mclNRtRIqeCh8f03mL9-JxFL2xUAAJqDwACLeBBSw95apK5o3GvNgQ")
    await update.message.reply_text("Введите ваше имя:")
    context.user_data['step'] = 'name'
    context.user_data['attempts'] = 0
    context.user_data['restart'] = 1

        
async def game_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Конец)")
    await context.bot.send_sticker(chat_id=context._user_id, sticker="CAACAgIAAxkBAAIDKmclNpDKHVwk0fi-oDFhoYVx7OP1AAICAwACWAQ_Lq1uOA2MdIteNgQ")


# Основная функция запуска бота
def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Обработчики сообщений пользователя
    #application.add_handler(MessageHandler(None, test))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(cake, pattern='^(cake)$'))

    # Регистрируем обработчики команд и нажатий
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("restart123", restart_command))
    application.add_handler(CommandHandler("sus", game_over))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
