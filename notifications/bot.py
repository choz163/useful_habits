from telegram import Update
from telegram.ext import ContextTypes
from .models import TelegramUser


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    TelegramUser.objects.update_or_create(
        user__username=user.username,
        defaults={"chat_id": chat_id, "user": update.effective_user},
    )
    await update.message.reply_text("Вы зарегистрированы для напоминаний!")
