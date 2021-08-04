"""Module for Quotex http login resource."""

from quotexapi.http.resource import Resource


class Logout(Resource):
    """Class for Quotex login resource."""
    # pylint: disable=too-few-public-methods

    url = ""

    def _post(self, data=None, headers=None):
        """Send get request for Quotex API login http resource.
        :returns: The instance of :class:`requests.Response`.
        """
        return self.api.send_http_request_v2(method="POST", url="https://qxbroker.com/logout",data=data, headers=headers)

    def __call__(self):
       
        return self._post()
