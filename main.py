import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import sympy as sp  # sympy кітапханасын қосу
from flask import Flask
import asyncio
from threading import Thread

# Flask серверін баптау
app = Flask(__name__)

@app.route('/')
def home():
    return 'Бот жұмыс істеп тұр!'

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

# Ботты іске қосу функциясы
async def start_bot():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Командаларды өңдеу
    application.add_handler(CommandHandler("start", start))

    # Барлық хабарламаларды өңдеу
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

    # Ботты іске қосу
    await application.run_polling()

# Flask серверін бөлек ағынға қосу
def run_flask():
    app.run(host='0.0.0.0', port=5000)  # Портты өзгерттік

# Ботты және Flask серверін бір уақытта іске қосу
def main():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    
    # Flask серверін бөлек ағынға қосу
    t = Thread(target=run_flask)
    t.start()
    
    # Telegram ботының ағынды орнату
    loop.run_until_complete(start_bot())  # Бұл жерді await емес, run_until_complete деп өзгертіңіз

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Лог жүргізу үшін
    main()
