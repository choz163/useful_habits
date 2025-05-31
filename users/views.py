from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegistrationSerializer

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = []    # публичный
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {'email': user.email, 'chat_id': user.chat_id}
        return Response(data, status=status.HTTP_201_CREATED)
