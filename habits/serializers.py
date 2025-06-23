from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        if data.get("related_habit") and data.get("reward"):
            raise serializers.ValidationError(
                "Нельзя одновременно указывать related_habit и reward."
            )
        if data.get("is_reward") and (data.get("related_habit") or data.get("reward")):
            raise serializers.ValidationError(
                "У приятной привычки не может быть reward или related_habit."
            )
        if data.get("duration", 0) > 120:
            raise serializers.ValidationError("duration не больше 120 сек.")
        periodicity = data.get("periodicity", 1)
        if not (1 <= periodicity <= 7):
            raise serializers.ValidationError("periodicity 1..7 дней.")
        return data
