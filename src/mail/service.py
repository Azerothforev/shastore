# flake8: noqa
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import SENDER_EMAIL, SENDER_PASSWORD
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aiosmtplib import SMTP


class EmailSender:
    @staticmethod
    def get_credentials():
        sender_email = SENDER_EMAIL
        password = SENDER_PASSWORD
        return sender_email, password

    @staticmethod
    def create_message(sender_email, receiver_email, subject, body):
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        return message

    @classmethod
    async def send_email(cls, user_email, subject, body):
        sender_email, password = cls.get_credentials()
        receiver_email = user_email

        message = cls.create_message(sender_email, receiver_email, subject, body)

        async with SMTP(hostname="smtp.gmail.com", port=587) as server:
            await server.login(sender_email, password)
            await server.send_message(message)

    @classmethod
    async def send_email_after_register(cls, user_email):
        subject = "Завершение регистрации"
        body = "Ваша регистрация успешно завершена. Спасибо за ваше доверие к нам."
        await cls.send_email(user_email, subject, body)

    @classmethod
    async def send_email_after_buying_product(cls, user_email):
        subject = "Покупки"
        body = "Спасибо за покупку товара, ожидайте получения."
        await cls.send_email(user_email, subject, body)