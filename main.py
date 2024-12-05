import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import sympy as sp  # sympy кітапханасын қосу
from keep_alive import keep_alive  # Flask keep_alive серверін импорттау
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

        # "×" және "÷" таңбаларын алмастыру
        expression = expression.replace("×", "*").replace("÷", "/")

        # Егер өрнек теңдеу түрінде болса (мысалы, 'x + 2 = 10')
        if "=" in expression:
            # Теңдеуді шешу
            lhs, rhs = expression.split("=")
            equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            solution = sp.solve(equation)
            await update.message.reply_text(f"Теңдеудің шешімі: {solution}")
        else:
            # Әдеттегі арифметикалық өрнекті есептеу
            result = eval(expression)
            await update.message.reply_text(f"Нәтиже: {result}")
    except Exception as e:
        await update.message.reply_text("Қате! Өрнекті немесе теңдеуді дұрыс енгізіңіз.")

# Telegram ботының негізгі функциясы
async def start_bot():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Командаларды өңдеу
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

    # Ботты іске қосу
    await application.run_polling()

# Негізгі функция
def main():
    logging.basicConfig(level=logging.INFO)

    # Flask keep_alive серверін қосу
    keep_alive()

    # Telegram ботының event loop-ын іске қосу
    asyncio.run(start_bot())

if __name__ == "__main__":
    main()
