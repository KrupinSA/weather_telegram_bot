** Данный  сервис позволяет  получить прогноз погоды через телеграмм бота.

Первоначально необходимо получить токен.

По ссылке можно ознакомиться с инструкцией.

https://core.telegram.org/bots#6-botfather

Для работы сервиса необходим python3.8 и выше.

Устанавливаем необходимые модули
pip3 install -r requirements.txt

Экспортируем токен в переменную окружения.
export TELEGRAM_TOKEN="......"

запуск 
python3 app.py

Наш бот ожидает получить число (0-31) - день за который он нам покажет прогнозируемую погоду (месяц вводить ненужно)


