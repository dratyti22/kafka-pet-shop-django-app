from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from src.services.jwt_utils import jwt_generate_token

User = get_user_model()


def send_email_activate(email: str):
    user = get_object_or_404(User, email=email)

    current_sit = Site.objects.get_current().domain
    # token = default_token_generator.make_token(user)
    # uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = jwt_generate_token(str(user.pk))
    url = reverse_lazy("user:activate", kwargs={"token": str(token)})

    message = render_to_string("email/activate_account.html",
                               {"activation_link": f"http://{current_sit}{url}"})

    subject = "Активируйте свой аккаунта"

    user.email_user(subject, message)
