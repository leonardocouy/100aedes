from rest_framework.generics import UpdateAPIView, CreateAPIView
from .permissions import IsOwner
from .serializers import UserSerializer
from .models import User


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwner,)
