from celery import shared_task
from django.conf import settings
from django.utils import timezone
from telegram import Bot
from .models import TelegramUser
from habits.models import Habit

@shared_task
def send_reminders():
    now = timezone.localtime().time().replace(second=0, microsecond=0)
    today = timezone.localdate()
    # выбираем привычки, у которых time == now и сегодня нужно напомнить
    habits = Habit.objects.filter(time=now)
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    for h in habits:
        # проверка выполнения за прошлые дни и периодичности опускается
        try:
            chat = h.user.telegramuser.chat_id
        except TelegramUser.DoesNotExist:
            continue
        text = f"Напоминание: {h.action} в {h.time}"
        bot.send_message(chat_id=chat, text=text)
