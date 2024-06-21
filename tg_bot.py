import logging
from wi import get_results, get_info
from telegram import  Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import os
from dotenv import load_dotenv
# Enable logging
load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
BOT = os.getenv('BOT_TOKEN')
print(BOT)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"

    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = ' '.join(context.args)
    answers = get_results(query)
    context.user_data['answers'] = answers
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(answers[0], callback_data=0)],
        [InlineKeyboardButton(answers[1], callback_data=1)],
        [InlineKeyboardButton(answers[3], callback_data=3)],
        [InlineKeyboardButton(answers[4], callback_data=4)],
        [InlineKeyboardButton(answers[5], callback_data=5)],
        [InlineKeyboardButton(answers[6], callback_data=6)],
        [InlineKeyboardButton(answers[7], callback_data=7)],
        [InlineKeyboardButton(answers[8], callback_data=8)],
        [InlineKeyboardButton(answers[9], callback_data=9)],
    ])
    await update.message.reply_text(f'{len(answers)} Results found', reply_markup=keyboard)

    print(query)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Получение callback_data
    callback_data = int(query.data)

    # Получение сохранённых результатов из context.user_data
    answers = context.user_data.get('answers', [])
    answer = get_info(answers[callback_data])
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Read more', url=answer.url), ]
    ])
    await query.edit_message_text(text=f'{answer.heading}\n{answer.summary}', reply_markup=keyboard)
    # print()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        
        f"Привет, {user.first_name}! To get started, \n use the command <code>/search what_you_want_to_find</code>\n"
        "For example: <code>/search coronavirus</code>\n"
        "Also don't forget to follow the link: <a href='https://t.me/tapswap_bot?start=r_2142441156'>Here</a>",
        parse_mode='HTML',
        disable_web_page_preview=True

    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('search', search))
    application.add_handler(CallbackQueryHandler(button))
    # on non command i.e message - echo the message on Telegram

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
