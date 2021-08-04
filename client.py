"""Module for Quotex websocket."""

import json
import logging
import websocket
import quotexapi.global_value as global_value

class WebsocketClient(object):
    """Class for work with Quotex websocket."""

    def __init__(self, api):
        """
        :param api: The instance of :class:`quotexapiAPI
            <quotexapi.api.QuotexAPI>`.
        """
        self.api = api
        self.wss = websocket.WebSocketApp(
            self.api.wss_url, on_message=self.on_message,
            on_error=self.on_error, on_close=self.on_close,
            on_open=self.on_open)
    
    def on_message(self, wss, message):
        """Method to process websocket messages."""
        # pylint: disable=unused-argument
        logger = logging.getLogger(__name__)
        logger.debug(message)
        message = json.loads(str(message))
        

     @staticmethod
    def on_error(wss, error): # pylint: disable=unused-argument
        """Method to process websocket errors."""
        logger = logging.getLogger(__name__)
        logger.error(error)
        global_value.websocket_error_reason=str(error)
        global_value.check_websocket_if_error=True
    @staticmethod
    def on_open(wss): # pylint: disable=unused-argument
        """Method to process websocket open."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")
        global_value.check_websocket_if_connect=1
    @staticmethod
    def on_close(wss): # pylint: disable=unused-argument
        """Method to process websocket close."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")
        global_value.check_websocket_if_connect=0
