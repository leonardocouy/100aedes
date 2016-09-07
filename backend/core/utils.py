from rest_framework_jwt import utils


def get_jwt_token(user):
    payload = utils.jwt_payload_handler(user)
    token = utils.jwt_encode_handler(payload)
    return 'JWT {0}'.format(token)
