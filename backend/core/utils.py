from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from rest_framework_jwt import utils


def get_jwt_token(user):
    payload = utils.jwt_payload_handler(user)
    token = utils.jwt_encode_handler(payload)
    return 'JWT {0}'.format(token)


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL, to])