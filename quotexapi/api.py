"""Module for Qoutex websocket."""
import time
import json
import logging
import threading
import requests
import ssl
import atexit
from collections import deque
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
    buy_id = None
    def __init__(self, host, set_ssid):
        """
        :param str host: The hostname or ip address of a Qoutex server.
        :param str set_ssid: The set_ssid of a Qoutex server.
        """
        self.wss_url = "wss://ws.{host}/socket.io/?EIO=3&transport=websocket".format(host=host)
        self.websocket_client = None
        self.set_ssid = set_ssid


    @property
    def websocket(self):
        """Property to get websocket.

        :returns: The instance of :class:`WebSocket <websocket.WebSocket>`.
        """
        return self.websocket_client.wss

    def send_websocket_request(self, data):
        """Send websocket request to Qoutex server.
        :param str data: The websocket request data.
        """
        
        logger = logging.getLogger(__name__)


         
         
        while (global_value.ssl_Mutual_exclusion or global_value.ssl_Mutual_exclusion_write) and no_force_send:
            pass
        global_value.ssl_Mutual_exclusion_write=True
        self.websocket.send(data)
        logger.debug(data)
        global_value.ssl_Mutual_exclusion_write=False

    

    @property
    def ssid(self):
        """Property for get Qoutex websocket ssid chanel.
        :returns: The instance of :class:`Ssid
            <Qoutex.ws.chanels.ssid.Ssid>`.
        """
        return Ssid(self)

    # -------------------------------------------------------
    def start_websocket(self):
        global_value.check_websocket_if_connect = None
        global_value.check_websocket_if_error=False
        global_value.websocket_error_reason=None
         
        self.websocket_client = WebsocketClient(self)

        self.websocket_thread = threading.Thread(target=self.websocket.run_forever, kwargs={'sslopt': {
                                                 "check_hostname": False, "cert_reqs": ssl.CERT_NONE, "ca_certs": "cacert.pem"}})  # for fix pyinstall error: cafile, capath and cadata cannot be all omitted
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
        #the ssid is None need get ssid
        else:
            response=self.get_ssid()  
            try:
               global_value.SSID = response
            except:
                self.close()
                return False
            self.send_ssid()
        
    
        return True,None

    def close(self):
        self.websocket.close()
        self.websocket_thread.join()
    
    def websocket_alive(self):
        return self.websocket_thread.is_alive()
