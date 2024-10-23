from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from comments.api.views import generate_auto_reply

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_task.settings')

import django
django.setup()

app = Celery('test_task')
# Встановлюємо змінну оточення для налаштувань Django


# app = Celery('test_task')

# Читаємо конфігурацію з налаштувань Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Додаємо налаштування для повторних спроб підключення до брокера
app.conf.broker_connection_retry_on_startup = True

# Автоматично виявляємо таски у додатках Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')