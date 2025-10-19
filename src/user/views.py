import datetime
import json
import logging
import uuid

import jwt
from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.services.jwt_auth import JWTAuthentication
from src.services.jwt_utils import generate_auth_tokens, jwt_verification_token
from src.services.kafka_producer import get_kafka_producer
from src.services.tasks import send_email_task
from src.user.serializers import UserProfileSerializer, UserRegisterLoginSerializer

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
                            status=status.HTTP_201_CREATED)

        return Response({"data": "Неверное поле"}, status=status.HTTP_400_BAD_REQUEST)


class UserActivateView(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request: Request, token: str) -> Response:
        try:
            user_id = jwt_verification_token(token)
            user = User.objects.get(pk=user_id)
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return Response({"data": "Неверная ссылка"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
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
                logger.info("Message sent to the topic: user_topic")
            except Exception as e:
                logger.warning(f"Failed to send Kafka event (non-critical): {e}")

            return Response({"data": "Аккаунт успешно активирован"}, status=status.HTTP_200_OK)
        return Response({"data": "Вы уже зарегистрированы"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializers_class = UserRegisterLoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            try:
                user = User.objects.get(email=email)
                if user.check_password(password) and user.is_active:
                    tokens = generate_auth_tokens(str(user.pk))
                    return Response({"data": "Успешная авторизация", "tokens": tokens},
                                    status=status.HTTP_200_OK)
                return Response({"data": "Неверные данные или аккаунт не активирован"},
                                status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"data": "Неверные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"data": "Неверные данные"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
def user_logout_view(request: Request) -> Response:
    if request.user.is_authenticated:
        return Response({"data": "Вы успешно вышли"}, status=status.HTTP_200_OK)
    return Response({"data": "Вы не авторизованы"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
