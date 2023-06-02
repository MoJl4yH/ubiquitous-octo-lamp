# bot

Перед запуском докеров необходимо создать файл `services/web/config/.env`,
который не отслеживается из соображений безопасности
<hr><br>

**В РАЗРАБОТКЕ**

*запуск на локалке возможен благодаря утилите* `ngrok`

`ngrok http 80` - отдаст url с https

<br><hr><br>
**Этапы запуска**
1. Создать `services/web/config/.env`
2. Добавить права 666 этому файлу
3. Добавить права 666 `services/web/logs`
4. Добавить переменные окружения
5. Перейти в корень проекта
6. docker-compose up --build -d
<br><hr><br>

**Либо**

1. Перейти в корень проекта
2. sudo make build
3. make run
4. Пару раз нажать на enter
5. Следовать инструкции
6. Можно перезапустить docker
<br><hr><br>

*Эта процедура выполняется 1 раз*

<br><hr><br><br>

**Переменные окружения**

получить токен бота телеграмма `TG_TOKEN`
и токен YouGile API `YOUGILE_TOKEN`, открыть файл `services/web/config/.env`
и изменить содержимое на следующее:
```
  YOUGILE_API_URL=https://yougile.com/api-v2
  TELEGRAM_API_URL=https://api.telegram.org/bot
  BASE_URL=<ваш_полный_домен_сервера>
  TELEGRAM_TOKEN=<ваш_токен_бота_телеграмма>
  YOUGILE_TOKEN=<ваш_токен_yougile_api>
```