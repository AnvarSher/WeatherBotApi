# WeatherBotApi

В данном репозитории расположено тестовое приложение реализующее API для telegram bot-а,
который выдает информацию о погоде в указанной локации.

Бот распознает текстовую информацию и воспринимает ее в качестве названия локации.
Бот так же распознает переданную в сообщении геолокацию.

Сервис реализован с использованием django rest framework.

## Установка и настройка

### Шаг 1. Клонируйте репозиторий
```
git clone https://github.com/AnvarSher/WeatherBotApi.git
```

### Шаг 2. Активируйте виртуальную среду

Перейдите в корневую директорию проекта:
```
cd WeatherBotApi/
```

Создайте виртуальную среду с помощью команды: 
```
"python3 -m venv env" (Windows/Linux) либо "virtualenv -p python3 env" (MacOS)
```

Затем активируйте eё:
```
"source env/bin/activate" (Linux/MacOS)  либо "env\Scripts\activate" (Windows)
```

### Шаг 3. Укажите переменные среды

Проставьте значение настройки BOT_TOKEN=(Token) в файле botenv.dev.

> Можете использовать уже указанный BOT_TOKEN. (Имя бота - @MyWeatherIsBot)


### Шаг 4. Запустите контейнеры

> При необходимости изменить порт web приложения в файле docker-compose.yaml. По умолчанию установлен порт 8000.

Запустите контейнеры:

```
(env) docker-compose up -d --build
```

### Шаг 5. Подвяжите webhook бота

Выполните GET запрос по адресу: 
```
https://api.telegram.org/bot(Token)/setWebhook?url=https://(Domen or IP-address)/api/bot/
```

#### Бот готов к использованию!


## Данные

Cхему данных можно подсмотреть в файле database-diagram.png. Тут всего три объекта.

<img src="https://github.com/AnvarSher/WeatherBotApi/blob/main/database-diagram.png?raw=true" alt="database-diagram.png"/>

Client - данные пользователя telegram, который обращается к боту.

Weather - информация о погоде в определенной точке на определенный момент времени.

ClientRequest - информация о запросе клиента, если это текстовый запрос, то текст запроса,
если это локация - то координаты. 
Если запрос выполнен успешно, то ClientRequest будет привязан к Weather.
Если запрос выполнен не успешно, ошибку можно будет увидеть в поле error объекта ClientRequest.	