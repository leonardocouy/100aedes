from .permissions import IsOwner
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response as JSONResponse
from .serializers import UserSerializer
from .models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, CreateAPIView


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwner,)

#
# @api_view(['POST'])
# def user(request):
#     if request.method == 'POST':
#         data = request.POST
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['PUT'])
# def user_update(request, pk):
#     profile = get_object_or_404(User, pk=pk)
#     if request.method == 'PUT':
#         serializer = UserSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
