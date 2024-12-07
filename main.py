import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sympy as sp
from threading import Thread
from keep_alive import keep_alive

# Логты конфигурациялау
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

# /start командасына жауап
def start(update: Update, context: CallbackContext) -> None:
    try:
        update.message.reply_text(
            "Сәлем! Мен калькулятор ботымын. Математикалық өрнек немесе теңдеу жіберіңіз.\n"
            "Мысалы: '3 × 5' немесе 'x + 2 = 10'."
        )
        logger.info("Пайдаланушы /start командасын бастады.")
    except Exception as e:
        logger.error(f"/start командасында қате пайда болды: {e}")

# /help командасына жауап
def help(update: Update, context: CallbackContext) -> None:
    try:
        update.message.reply_text(
            "Мен калькулятор ботымын. Арифметикалық өрнектерді және теңдеулерді шешуге көмектесемін.\n"
            "Қолдану мысалдары:\n"
            "'3 × 5' немесе 'x + 2 = 10'.\n\n"
            "Менің жұмысым:\n"
            "1. Арифметикалық операцияларды орындау.\n"
            "2. Теңдеулерді шешу.\n\n"
            "Қосымша сұрақтар болса, маған хабарласыңыз!"
        )
        logger.info("Пайдаланушыға /help командасымен көмек көрсетілді.")
    except Exception as e:
        logger.error(f"/help командасында қате пайда болды: {e}")

# Арифметикалық операцияларды өңдеу немесе теңдеулерді шешу
def calculate(update: Update, context: CallbackContext) -> None:
    try:
        expression = update.message.text
        expression = expression.replace("×", "*").replace("÷", "/")
        logger.info(f"Пайдаланушыдан келіп түскен өрнек: {expression}")

        if "=" in expression:
            lhs, rhs = expression.split("=")
            equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            solution = sp.solve(equation)
            update.message.reply_text(f"Теңдеудің шешімі: {solution}")
            logger.info(f"Теңдеудің шешімі: {solution}")
        else:
            result = eval(expression)
            update.message.reply_text(f"Нәтиже: {result}")
            logger.info(f"Арифметикалық нәтиже: {result}")
    except Exception as e:
        update.message.reply_text("Қате! Өрнекті немесе теңдеуді дұрыс енгізіңіз.")
        logger.error(f"Өрнек немесе теңдеуді өңдеуде қате пайда болды: {e}")

# Telegram ботының негізгі функциясы
def start_bot():
    try:
        # Telegram API Token
        TOKEN = "7820799149:AAGWqhF9osabrJqMH7FEs9Gln5UVHRNyxxo"

        updater = Updater(TOKEN)

        # Командалар мен хабарларды өңдеу
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))  # /help командасын қосу
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, calculate))

        # Ботты іске қосу
        updater.start_polling()
        logger.info("Бот іске қосылды.")
        updater.idle()
    except Exception as e:
        logger.error(f"Ботты іске қосу кезінде қате пайда болды: {e}")

# Flask серверін бөлек ағынға қосу
def run_flask():
    try:
        keep_alive()
        logger.info("Flask сервері іске қосылды.")
    except Exception as e:
        logger.error(f"Flask серверін іске қосу кезінде қате пайда болды: {e}")

# Негізгі функция
def main():
    try:
        logging.basicConfig(level=logging.INFO)

        # Flask серверін бөлек ағынмен іске қосу
        flask_thread = Thread(target=run_flask)
        flask_thread.start()

        # Telegram ботын іске қосу
        start_bot()
    except Exception as e:
        logger.error(f"Негізгі функцияда қате пайда болды: {e}")

if __name__ == "__main__":
    main()
