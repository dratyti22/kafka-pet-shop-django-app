import datetime
import json
import logging
import uuid

from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.services.kafka_producer import get_kafka_producer
from src.services.tasks import send_email_task
from src.user.serializers import UserRegisterLoginSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


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
            try:
                send_email_task.delay(email)
            except Exception as e:
                logger.warning(f"Failed to queue email task (non-critical): {e}")
            return Response({"data": "На ваш email отправлено письмо для подтверждения аккаунта"},
                            status=status.HTTP_200_OK)

        return Response({"data": "Неверное поле"}, status=status.HTTP_400_BAD_REQUEST)


class UserActivateView(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request: Request, uidb64: str, token: str) -> Response:
        try:
            uuid_url = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uuid_url.decode("utf-8"))
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        is_token_valid = default_token_generator.check_token(user, token)
        if user is not None and is_token_valid:
            user.is_active = True
            user.save()
            try:
                producer = get_kafka_producer()
                data = {
                    "event_id": str(uuid.uuid4()),
                    "event_type": "user_created",
                    "event_version": "1.0",
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "data": {
                        "user_id": str(user.id),
                        "user_email": user.email,
                        "role": user.role,
                        "phone": user.phone,
                        "first_name": user.first_name,
                        "last_name": user.last_name
                    }

                }

                producer.produce(
                    "user_topic",
                    key=str(user.pk),
                    value=json.dumps(data).encode('utf-8'),
                )
                producer.flush(timeout=10)
                logger.info(f"Message sent to the topic: user_topic")
            except Exception as e:
                logger.warning(f"Failed to send Kafka event (non-critical): {e}")

            return Response({"data": "Аккаунт успешно активирован"}, status=status.HTTP_200_OK)
        return Response({"data": "Неверная ссылка"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializers_class = UserRegisterLoginSerializer

    def post(self, request: Request) -> Response:
        if request.user.is_authenticated:
            return Response({"data": "Вы уже авторизованы"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                if user.is_active:
                    login(request, user)
                    return Response({"data": "Вы успешно авторизованы"}, status=status.HTTP_200_OK)
                return Response({"data": "Аккаунт не активирован"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"data": "Неверные данные"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data": "Неверные данные"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_logout_view(request: Request) -> Response:
    if request.user.is_authenticated:
        logout(request)
        return Response({"data": "Вы успешно вышли"}, status=status.HTTP_200_OK)
    return Response({"data": "Вы не авторизованы"}, status=status.HTTP_400_BAD_REQUEST)
