# Телеграм бот службы технической поддержки
(или прокси бот)
две модели в одной список ботов с токенами 
в другой список chat_id: админов-менеджеров которые отвечают на сообщение.
Бот может быть подгружен админом в группу телеграмм и публичить туда сообщения от пользователей

```
# что бы узнать chat_id: менеджера или группы (у группы будит отрицательный chat_id) 
# наберите команду в боте или в группе где вы добавили бота админом
/getchatid
```

что бы отвечать на сообщения пользователей от бота тех.поддержки, делайте обычный ответ на сообщения в телеграмме


## Внешний сервис для проброса тунеля https://serveo.net/
позволяет тестировать bot на setWebhook
```
ssh -R 80:127.0.0.1:8000 serveo.net
```

## api на Django для bota
serveo - возвращает url который будит вашим api для телеграм бота
```
toket_you_bot = ''
api_from_telegram = https://olim.serveo.net/quport/{toket_you_bot}/
```

## установить setWebhook для бота
```
https://api.telegram.org/bot{toket_you_bot}/setWebhook?url=https://olim.serveo.net/quport/{toket_you_bot}/
```

## 0.1 Django start

```
source venv/bin/activate # войти в среду
deactivate # выйти из среды

python manage.py runserver # запуск сервера

/support_bot/models.py  # добавить модель и осуществить миграцию
python manage.py makemigrations  # создает файл миграции из моделей данных
python manage.py migrate # осуществляет саму миграцию
```   

## 0.2 rezume
ничего особенного нету, но на одном сервере можно имееть несколько апи для разных токенов моделей
для разных Webhook и технически обслуживать пользователей

```
https://olim.serveo.net/quport/{toket_you_bot_1}/
https://olim.serveo.net/quport/{toket_you_bot_2}/
https://olim.serveo.net/quport/{toket_you_bot_3}/
```

для отправки сообщений в телеграм
используется простые функции requests.post в этом классе /support_bot/telega.py 