from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth import get_user_model
from applications.account.serializers import ForgotPasswordSerializer, ChangePasswordSerializer, \
    ForgotPasswordCompleteSerializer, RegisterSerializer
from rest_framework.response import Response

User = get_user_model()


class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)
    return Response('Вы успешно зарегистрировались.' 'Мы отправили вам активационный код', status=201)


# class LoginApiView(ObtainAuthToken):
#     serializer_class = LoginSerializer


# class LogoutApiView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         user = request.user
#         Token.objects.filter(user=user).delete()
#         return Response('Вы успешно вышли из аккаунта')


class ChangePasswordApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Вы успешно поменяли пароль')


class ActivationApiView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Успешно'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': 'Неправильные данные'}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordApiView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Мы отправили вам код для восстановления пароля')


class ForgotPasswordCompleteApiview(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Вы успешно обновили пароль')


