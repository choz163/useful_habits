import pytest
from django.core.exceptions import ValidationError
from habits.models import Habit
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_duration_validator():
    u = User.objects.create_user("u")
    h = Habit(user=u, place="x", time="12:00", action="a", duration=121)
    with pytest.raises(ValidationError):
        h.full_clean()
