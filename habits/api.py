from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Habit
from .serializers import HabitSerializer

class MyHabitsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class MyHabitsView(generics.ListCreateAPIView):
    """
    GET  /api/habits/my-habits/   — получить свои привычки (постранично)
    POST /api/habits/my-habits/   — создать новую привычку за собой
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = HabitSerializer
    pagination_class   = MyHabitsPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

