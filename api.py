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
from quotexapi.http.logout import Logout
from quotexapi.ws.chanels.ssid import Ssid
from quotexapi.ws.client import WebsocketClient
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
            :class:`Resource <Qoutex.http.resource.Resource>`.
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
        """Property for get Qoutex http login resource.

        :returns: The instance of :class:`Login
            <Qoutex.http.login.Login>`.
        """
        return Login(self)

    @property
    def ssid(self):
        """Property for get Qoutex websocket ssid chanel.
        :returns: The instance of :class:`Ssid
            <Qoutex.ws.chanels.ssid.Ssid>`.
        """
        return Ssid(self)

    # -------------------------------------------------------

    def set_session(self,cookies,headers):

        """Method to set session cookies."""

        self.session.headers.update(headers)
         
        self.session.cookies.clear_session_cookies()
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)

    def start_websocket(self):
        global_value.check_websocket_if_connect = None
        global_value.check_websocket_if_error=False
        global_value.websocket_error_reason=None
         
        self.websocket_client = WebsocketClient(self)

        self.websocket_thread = threading.Thread(target=self.websocket.run_forever, kwargs={'sslopt': {
                                                 "check_hostname": False, "cert_reqs": ssl.CERT_NONE, "ca_certs": "cacert.pem"},
                                                 "pingInterval": 25000})  # for fix pyinstall error: cafile, capath and cadata cannot be all omitted
        self.websocket_thread.daemon = True
        self.websocket_thread.start()
        while True:
            try:
                if global_value.check_websocket_if_error:
                    return False,global_value.websocket_error_reason
                if global_value.check_websocket_if_connect == 0 :
                    return False,"Websocket connection closed."
                elif global_value.check_websocket_if_connect == 1:
                    return True,None
            except:
                pass

            pass

    def send_ssid(self):
        self.profile.msg=None
        self.ssid(global_value.SSID)  # pylint: disable=not-callable
        while self.profile.msg==None:
            pass
        if self.profile.msg==False:
            return False
        else:
            return True

    def connect(self):
        
        global_value.ssl_Mutual_exclusion=False
        global_value.ssl_Mutual_exclusion_write=False
        """Method for connection to Qoutex API."""
        try:
            self.close()
        except:
            pass
        check_websocket,websocket_reason=self.start_websocket()
         
        if check_websocket==False:
            return check_websocket,websocket_reason

        #doing temp ssid reconnect for speed up
        if global_value.SSID!=None:
            
            check_ssid=self.send_ssid()
           
            if check_ssid==False:
                #ssdi time out need reget,if sent error ssid,the weksocket will close by Qoutex server
                response=self.get_ssid()
                try:
                    global_value.SSID = response.cookies["ssid"]     
                except:
                    return False,response.text
                atexit.register(self.logout)
                self.start_websocket()
                self.send_ssid()
         
        #the ssid is None need get ssid
        else:
            response=self.get_ssid()
            try:
               global_value.SSID = response.cookies["ssid"]
            except:
                self.close()
                return False,response.text
            atexit.register(self.logout)
            self.send_ssid()
        
        #set ssis cookie
        requests.utils.add_dict_to_cookiejar(self.session.cookies, {"ssid":global_value.SSID})
        

        self.timesync.server_timestamp = None
        while True:
            try:
                if self.timesync.server_timestamp != None:
                    break
            except:
                pass
        return True,None

    def close(self):
        self.websocket.close()
        self.websocket_thread.join()
    
    def websocket_alive(self):
        return self.websocket_thread.is_alive()
