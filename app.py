import os
import locale
import weather_requests
from datetime import datetime
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters


def check_format(text):
    '''
    проверяем формат даты введенного пользователем.
    Ожидается число в формате %d или %dd.
    Месяц подставлется текущий, либо следующий, если введенная дата меньше текущего числа 

    '''
    if len(text) in (1,2):
        try:
            if datetime.today().day<=int(text):
                raw_day = text, str(datetime.today().month), str(datetime.today().year)
            elif datetime.today().month < 12:
                raw_day = text, str((datetime.today().month + 1) % 12 or 12), str(datetime.today().year)
            else:
                raw_day = text, str((datetime.today().month + 1) % 12 or 12), str(datetime.today().year + 1)
        except ValueError:
            return None        
        text = "/".join(raw_day)

    try:
        return datetime.strptime(text, '%d/%m/%Y')
    except ValueError:
        pass
    return None


def check_date(date):
    '''
    Проверяем рамки для ввода даты
    '''
    count_days = (date - datetime.today()).days
    if count_days < 28:
        return True
    return False


def get_weather(date):
    '''
    Получаем погодный календарь на целый месяц.
    Ищем по календарю интересубщую нас дату.
    '''
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    for day, data in weather_requests.get_weathers().items():
        if datetime.strptime(day, '%d %B').strftime('%d%m') == date.strftime('%d%m'):
            raw_data = day, *data
            return "; ".join(raw_data)
    return None


def response(update, context):
    '''
    ответы для нашенго бота
    '''
    date = check_format(update.message.text)
    if not date:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='дата не соответствует формату (dd)')
        return None

    if not check_date(date):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Дата не должна превышать тридцать дней от текущей')
        return None

    if weather := get_weather(date):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=weather)
        return None


                                 




if __name__=="__main__":
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    response_handler = MessageHandler(Filters.text, response)
    dispatcher.add_handler(response_handler)

    updater.start_polling()
