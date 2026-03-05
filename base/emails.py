from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(email, email_token):
    subject = 'Your account needs to be verified'
    email_from = settings.DEFAULT_FROM_EMAIL
    base_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    activation_link = f'{base_url}/accounts/activate/{email_token}'
    message = f'Hi, click on the link to activate your account {activation_link}'
    send_mail(subject, message, email_from, [email])
