from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.services.tasks import send_email_task
from src.user.serializers import UserRegisterLoginSerializer

User = get_user_model()


class UserRegisterView(APIView):
    serializers_class = UserRegisterLoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = User.objects.create_user(email=email, password=password)
            user.is_active = False
            user.save()
            send_email_task.delay(email)
            return Response({"data": "На ваш email отправлено письмо для подтверждения аккаунта"},
                            status=status.HTTP_200_OK)

        return Response({"data": "Неверное поле"}, status=status.HTTP_400_BAD_REQUEST)


class UserActivateView(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request: Request, uidb64: str, token: str) -> Response:
        try:
            uuid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uuid.decode("utf-8"))
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        is_token_valid = default_token_generator.check_token(user, token)
        if user is not None and is_token_valid:
            user.is_active = True
            user.save()
            return Response({"data": "Аккаунт успешно активирован"}, status=status.HTTP_200_OK)
        return Response({"data": "Неверная ссылка"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializers_class = UserRegisterLoginSerializer

    def post(self, request: Request) -> Response:
        if request.user.is_authenticated:
            return Response({"data": "Вы уже авторизованы"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data["email"]:
                user = User.objects.get(email=serializer.validated_data["email"])
                if user.is_active:
                    login(request, user)
                    return Response({"data": "Вы успешно авторизованы"}, status=status.HTTP_200_OK)
                return Response({"data": "Аккаунт не активирован"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data": "Неверные данные"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_logout_view(reqeust: Request) -> Response:
    if reqeust.user.is_authenticated:
        logout(reqeust)
        return Response({"data": "Вы успешно вышли"}, status=status.HTTP_200_OK)
    return Response({"data": "Вы не авторизованы"}, status=status.HTTP_400_BAD_REQUEST)
