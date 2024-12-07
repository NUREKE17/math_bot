import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sympy as sp
from threading import Thread
from keep_alive import keep_alive

# /start командасына жауап
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Сәлем! Мен калькулятор ботымын. Математикалық өрнек немесе теңдеу жіберіңіз.\n"
        "Мысалы: '3 × 5' немесе 'x + 2 = 10'."
    )

# Арифметикалық операцияларды өңдеу немесе теңдеулерді шешу
def calculate(update: Update, context: CallbackContext) -> None:
    try:
        expression = update.message.text
        expression = expression.replace("×", "*").replace("÷", "/")

        if "=" in expression:
            lhs, rhs = expression.split("=")
            equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            solution = sp.solve(equation)
            update.message.reply_text(f"Теңдеудің шешімі: {solution}")
        else:
            result = eval(expression)
            update.message.reply_text(f"Нәтиже: {result}")
    except Exception:
        update.message.reply_text("Қате! Өрнекті немесе теңдеуді дұрыс енгізіңіз.")

# Telegram ботының негізгі функциясы
def start_bot():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # Telegram API Token
    TOKEN = "7820799149:AAGWqhF9osabrJqMH7FEs9Gln5UVHRNyxxo"

    updater = Updater(TOKEN)

    # Командалар мен хабарларды өңдеу
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, calculate))

    # Ботты іске қосу
    updater.start_polling()
    updater.idle()

# Flask серверін бөлек ағынға қосу
def run_flask():
    keep_alive()

# Негізгі функция
def main():
    logging.basicConfig(level=logging.INFO)

    # Flask серверін бөлек ағынмен іске қосу
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Telegram ботын іске қосу
    start_bot()

if __name__ == "__main__":
    main()
