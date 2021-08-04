"""Module for Quotex http login resource."""

from quotexapi.http.resource import Resource


class Login(Resource):
    """Class for IQ option login resource."""
    # pylint: disable=too-few-public-methods

    url = ""

    def _post(self, data=None, headers=None):
        """Send get request for IQ Option API login http resource.
        :returns: The instance of :class:`requests.Response`.
        """
        return self.api.send_http_request_v2(method="POST", url="https://qxbroker.com/en/sign-in/",data=data, headers=headers)

    def __call__(self, username, password, token):
        """Method to get IQ Option API login http request.
        :param str username: The username of a IQ Option server.
        :param str password: The password of a IQ Option server.
        :returns: The instance of :class:`requests.Response`.
        """
        data = {"_token": token
        "email": username
        "password": password
        return self._post(data=data)
