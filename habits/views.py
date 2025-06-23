from rest_framework import generics, permissions
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly


class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]
