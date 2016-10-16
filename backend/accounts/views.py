from rest_framework import status
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .permissions import IsOwner
from .serializers import UserSerializer
from .models import User


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        from backend.core.utils import get_jwt_token
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['user_token'] = get_jwt_token(serializer.instance)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwner,)
    authentication_classes = (JSONWebTokenAuthentication, )

