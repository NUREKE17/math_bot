import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import sympy as sp
from keep_alive import keep_alive  # Keep_alive файлын импорттаймыз

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Сәлем! Мен калькулятор ботымын!")

async def calculate(update: Update, context: CallbackContext) -> None:
    try:
        expression = update.message.text.replace("×", "*").replace("÷", "/")
        if "=" in expression:
            lhs, rhs = expression.split("=")
            equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            solution = sp.solve(equation)
            await update.message.reply_text(f"Шешімі: {solution}")
        else:
            result = eval(expression)
            await update.message.reply_text(f"Нәтиже: {result}")
    except Exception as e:
        await update.message.reply_text("Қате!")

async def start_bot():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))
    await application.run_polling()

def main():
    keep_alive()  # Keep_alive серверін қосу
    start_bot()

if __name__ == '__main__':
    main()
