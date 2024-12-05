import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import sympy as sp
from threading import Thread
from keep_alive import keep_alive
import asyncio

# /start командасына жауап
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Сәлем! Мен калькулятор ботымын. Математикалық өрнек немесе теңдеу жіберіңіз.\n"
        "Мысалы: '3 × 5' немесе 'x + 2 = 10'."
    )

# Арифметикалық операцияларды өңдеу немесе теңдеулерді шешу
async def calculate(update: Update, context: CallbackContext) -> None:
    try:
        expression = update.message.text
        expression = expression.replace("×", "*").replace("÷", "/")

        if "=" in expression:
            lhs, rhs = expression.split("=")
            equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            solution = sp.solve(equation)
            await update.message.reply_text(f"Теңдеудің шешімі: {solution}")
        else:
            result = eval(expression)
            await update.message.reply_text(f"Нәтиже: {result}")
    except Exception:
        await update.message.reply_text("Қате! Өрнекті немесе теңдеуді дұрыс енгізіңіз.")

# Telegram ботының негізгі функциясы
async def start_bot():
    application = Application.builder().token("7820799149:AAGWqhF9osabrJqMH7FEs9Gln5UVHRNyxxo").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))
    await application.run_polling()

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
    loop = asyncio.get_event_loop()  # Қолданыстағы event loop-ты алыңыз
    loop.create_task(start_bot())   # Telegram ботын event loop-қа қосыңыз
    loop.run_forever()              # Event loop-ты үздіксіз жұмыс істетіңіз

if __name__ == "__main__":
    main()
