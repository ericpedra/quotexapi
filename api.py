"""Module for Qoutex websocket."""
import time
import json
import logging
import threading
import requests
import ssl
import atexit
from collections import deque
from quotexapi.http.login import Login
from quotexapi.ws.chanels.ssid import Ssid
from iqoptionapi.ws.client import WebsocketClient
import quotexapi.global_value as global_value
from collections import defaultdict


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))


requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member
class Quotex(object):  # pylint: disable=too-many-instance-attributes
    """Class for communication with Quotex API."""
     
    # pylint: disable=too-many-public-methods
    socket_option_opened={}
    def __init__(self, host, username, password, proxies=None):
        """
        :param str host: The hostname or ip address of a Qoutex server.
        :param str username: The username of a Qoutex server.
        :param str password: The password of a Qoutex server.
        :param dict proxies: (optional) The http request proxies.
        """
        self.https_url = "https://{host}/".format(host=host)
        self.wss_url = "wss://ws.{host}/socket.io/?EIO=3&transport=websocket".format(host=host)
        self.websocket_client = None
        self.session = requests.Session()
        self.session.verify = False
        self.session.trust_env = False
        self.username = username
        self.password = password
        self.proxies = proxies
        # is used to determine if a buyOrder was set  or failed. If
        # it is None, there had been no buy order yet or just send.
        # If it is false, the last failed
        # If it is true, the last buy order was successful


    def prepare_http_url(self, resource):
        """Construct http url from resource url.

        :param resource: The instance of
            :class:`Resource <Qoutex.http.resource.Resource>`.

        :returns: The full url to Qoutex http resource.
        """
        return "/".join((self.https_url, resource.url))

    def send_http_request(self, resource, method, data=None, params=None, headers=None):  # pylint: disable=too-many-arguments
        """Send http request to Qoutex server.

        :param resource: The instance of
            :class:`Resource <iqoptionapi.http.resource.Resource>`.
        :param str method: The http request method.
        :param dict data: (optional) The http request data.
        :param dict params: (optional) The http request params.
        :param dict headers: (optional) The http request headers.

        :returns: The instance of :class:`Response <requests.Response>`.
        """
        logger = logging.getLogger(__name__)
        url = self.prepare_http_url(resource)

        logger.debug(url)

        response = self.session.request(method=method,
                                        url=url,
                                        data=data,
                                        params=params,
                                        headers=headers,
                                        proxies=self.proxies)
        logger.debug(response)
        logger.debug(response.text)
        logger.debug(response.headers)
        logger.debug(response.cookies)

        response.raise_for_status()
        return response

    def send_http_request_v2(self, url, method, data=None, params=None, headers=None):  # pylint: disable=too-many-arguments
        """Send http request to Qoutex server.

        :param resource: The instance of
            :class:`Resource <iqoptionapi.http.resource.Resource>`.
        :param str method: The http request method.
        :param dict data: (optional) The http request data.
        :param dict params: (optional) The http request params.
        :param dict headers: (optional) The http request headers.

        :returns: The instance of :class:`Response <requests.Response>`.
        """
        logger = logging.getLogger(__name__)

        logger.debug(method+": "+url+" headers: "+str(self.session.headers)+" cookies: "+str(self.session.cookies.get_dict()))
        
        
        response = self.session.request(method=method,
                                        url=url,
                                        data=data,
                                        params=params,
                                        headers=headers,
                                        proxies=self.proxies)
        logger.debug(response)
        logger.debug(response.text)
        logger.debug(response.headers)
        logger.debug(response.cookies)

        #response.raise_for_status()
        return response

    @property
    def websocket(self):
        """Property to get websocket.

        :returns: The instance of :class:`WebSocket <websocket.WebSocket>`.
        """
        return self.websocket_client.wss

    def send_websocket_request(self, name, msg, request_id="",no_force_send=True):
        """Send websocket request to Qoutex server.

        :param str name: The websocket request name.
        :param dict msg: The websocket request msg.
        """
        
        logger = logging.getLogger(__name__)

        data = json.dumps(dict(name=name,
                               msg=msg, request_id=request_id))
         
         
        while (global_value.ssl_Mutual_exclusion or global_value.ssl_Mutual_exclusion_write) and no_force_send:
            pass
        global_value.ssl_Mutual_exclusion_write=True
        self.websocket.send(data)
        logger.debug(data)
        global_value.ssl_Mutual_exclusion_write=False

    @property
    def login(self):
        """Property for get IQ Option http login resource.

        :returns: The instance of :class:`Login
            <Qoutex.http.login.Login>`.
        """
        return Login(self)
