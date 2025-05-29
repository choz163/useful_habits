from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_reward = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                      limit_choices_to={'is_reward': True})
    periodicity = models.PositiveIntegerField(default=1,
        help_text='Периодичность в днях (1–7)')
    reward = models.CharField(max_length=255, blank=True, null=True)
    duration = models.PositiveIntegerField(help_text='Время на выполнение в секундах')
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError("Можно указать либо связанную привычку, либо текст награды, но не оба сразу.")
        if self.is_reward and (self.related_habit or self.reward):
            raise ValidationError("Приятная привычка не может иметь награду или связанную привычку.")
        if self.duration > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")
        if not (1 <= self.periodicity <= 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} at {self.time}"
