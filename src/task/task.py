# flake8: noqa
import os
import sys

from mail.service import EmailSender
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from celery import Celery
from kombu import Queue, Exchange
from config import RABBITMQ_DEFAULT_PASS, RABBITMQ_DEFAULT_USER

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672

BROKER_URL = f'pyamqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/'
CELERY_RESULT_BACKEND = 'rpc://'

# Имя вашей очереди
QUEUE_NAME = 'email_queue'

CELERY_QUEUES = (
    Queue(QUEUE_NAME, exchange=Exchange('default'), routing_key=QUEUE_NAME),
)

celery = Celery('tasks', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)