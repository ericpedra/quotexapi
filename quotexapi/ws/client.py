"""Module for IQ option websocket."""

import simplejson as json
import logging
import websocket
import quotexapi.global_value as global_value

class WebsocketClient(object):
    """Class for work with Quotex API websocket."""

    def __init__(self, api):
        """
        :param api: The instance of :class:`QuotexAPI
            <quotexapi.api.QuotexAPI>`.
        """
        self.api = api
        self.wss = websocket.WebSocketApp(
            self.api.wss_url, on_message=self.on_message,
            on_error=self.on_error, on_close=self.on_close,
            on_open=self.on_open)

    def dict_queue_add(self,dict,maxdict,key1,key2,key3,value):
        if key3 in dict[key1][key2]:
                    dict[key1][key2][key3]=value
        else:
            while True:
                try:
                    dic_size=len(dict[key1][key2])
                except:
                    dic_size=0
                if dic_size<maxdict:
                    dict[key1][key2][key3]=value
                    break
                else:
                    #del mini key
                    del dict[key1][key2][sorted(dict[key1][key2].keys(), reverse=False)[0]]   

    def on_message(self, message): # pylint: disable=unused-argument
        """Method to process websocket messages."""
        global_value.ssl_Mutual_exclusion=True
        try:
            logger = logging.getLogger(__name__)
            message = massage
            try:
                message = message[1:]
                message = message.decode('utf-8')
                logger.debug(message)
                message = json.loads(str(message))
                try:
                     self.api.buy_id= message["id"]
                except:
                    pass
            except:
                pass
        except:
            pass
        global_value.ssl_Mutual_exclusion=False


    @staticmethod
    def on_error(wss, error):  # pylint: disable=unused-argument
        """Method to process websocket errors."""
        logger = logging.getLogger(__name__)
        logger.error(error)
        global_value.websocket_error_reason = str(error)
        global_value.check_websocket_if_error = True
        

    @staticmethod
    def on_open(wss):  # pylint: disable=unused-argument
        """Method to process websocket open."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")
        global_value.check_websocket_if_connect = 1

    @staticmethod
    def on_close(wss):  # pylint: disable=unused-argument
        """Method to process websocket close."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")
        global_value.check_websocket_if_connect = 0
