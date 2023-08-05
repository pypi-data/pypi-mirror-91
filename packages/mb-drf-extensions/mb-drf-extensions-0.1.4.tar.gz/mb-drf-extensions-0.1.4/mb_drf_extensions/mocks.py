import collections
import json
import uuid

from requests_mock import Mocker

from .authentication import OAuth2Mixin


class AuthenticationMocker(Mocker):
    def __init__(
            self,
            username=None,
            user_uuid=None,
            user_scopes=None,
            access_token=None,
    ):
        super().__init__()
        self.username = username or uuid.uuid4().hex
        self.user_uuid = user_uuid or uuid.uuid4().hex
        self.user_scopes = (
            ' '.join(user_scopes) if
            isinstance(user_scopes, collections.Iterable) else ''
        )
        self.access_token = access_token or uuid.uuid4().hex

    def start(self):
        super().start()
        self.register_uri(
            'POST', OAuth2Mixin.oauth2_login_url,
            text=json.dumps({
                'access_token': self.access_token,
                'expires_in': 36000
            }),
        )
        self.register_uri(
            'POST', OAuth2Mixin.oauth2_introspect_url,
            text=json.dumps({
                'scope': self.user_scopes,
                'user': {
                    'username': self.username,
                    'uuid': self.user_uuid,
                }
            }),
        )


def authentication_mock(pass_mocker=False, **mock_kwargs):
    """
    decorator for authentication mock
    :param pass_mocker:
    :param mock_kwargs:
    :return:
    """

    def decorator(func):
        def wrapped(*args, **func_kwargs):
            with AuthenticationMocker(**mock_kwargs) as m:
                if pass_mocker:
                    func_kwargs['mocker'] = m
                return func(*args, **func_kwargs)

        return wrapped

    return decorator
