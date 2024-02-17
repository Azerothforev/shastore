перед запуском проекта, пожалуйстa:

1. установите зависимости в головной директории используя команду
	pip install -r requirements.txt

2. создайте файл .env и опишите внутри него переменные для rabbitmq, postgresql, jwt-token, а также логин/пароль приложения для отправки писем по gmail:
	POSTGRES_HOST=
	POSTGRES_PORT=
	POSTGRES_DB=
	POSTGRES_USER=
	POSTGRES_PASSWORD=
	SENDER_EMAIL=
	SENDER_PASSWORD=
	SECRET=
	RABBITMQ_USER=
	RABBITMQ_PASS=
	RABBITMQ_HOST=
	
3. создайте и запустите переменную окружения:
	python -m venv venv
	source venv/Scripts/activate *для windows

4. cоздайте внутри папки src/migrations директорию versions, где будут создаваться миграции alembic.

5. сделайте миграции в директории src используя команду:
	alembic revision --autogenerate -m "ваш комментарий"

6. поднимите все контейнеры в сети через docker-compose.yaml:
	docker-compose up --build
	docker-compose up -d --build *запустите в режиме демона, если не хотите видеть логов и освободить терминал


Помните, что вы разворачиваете на локалке и для реального прода вам нужно переписать docker-compose или же создать новый