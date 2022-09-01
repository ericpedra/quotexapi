# python
from quotexapi.api import QuotexAPI
import quotexapi.global_value as global_value
import threading
import time
import logging
import operator
from collections import defaultdict
from collections import deque

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))

class Quotex:
    __version__ = "1.3"
    def __init__(self, set_ssid):
        self.size = [1, 5, 10, 15, 30, 60, 120, 300, 600, 900, 1800,
                    3600, 7200, 14400, 28800, 43200, 86400, 604800, 2592000]
        self.set_ssid = set_ssid
        self.suspend = 0.5
        self.subscribe_candle = []
        self.subscribe_candle_all_size = []
        self.subscribe_mood = []
        
        # --start
        # self.connect()
        # this auto function delay too long
        
        

    def change_account(self, Balance_MODE):
        """Change active account `real` or `practice`"""
        real_id = None
        practice_id = None
        if Balance_MODE == "REAL":
            pass
        elif Balance_MODE == "PRACTICE":
            pass
        else:
            logging.error("ERROR doesn't have this mode")
            exit(1)
            
    def get_balance(self):
        pass
        

    def get_balances(self):
        pass
            
    # _____________________BUY________________________________

    # __________________FOR OPTION____________________________
    def buy(self, ACTIVES, price, ACTION, expirations):
        """ Buy Binary option""""
        pass
      
    def sell_option(self, options_ids):
        pass
      
    def check_win(self, id_number):
        """Check win based id""""
        pass
      
    def get_signal_data(self):
      """ Get signal Quotex server""""
        pass
      
    def get_payment(self)
        """ payment Quotex server""""
        pass

      
      
      
    # ________________________________________________________________________
    # _______________________        CANDLE      _____________________________
    # ________________________self.api.getcandles() wss________________________
    def get_candles(self, ACTIVES, interval, offset, period):
        while True:
            try:
                pass
            except:
                logging.error('**error** get_candles need reconnect')
                self.connect() #go connect
                
    def get_candle_v2(self, ACTIVES, offset):
        while True:
            try:
                pass
            except:
                logging.error('**error** get_candle_v2 need reconnect')
                self.connect() #go connect
    # ------------------------Subscribe ONE SIZE-----------------------
    def start_candles_one_stream(self, ACTIVE, size):
        pass
    def stop_candles_one_stream(self, ACTIVE, size):
        pass
    
      
    # ------------------------Subscribe ALL SIZE-----------------------

    def start_candles_all_size_stream(self, ACTIVE):
        pass
    def stop_candles_all_size_stream(self, ACTIVE):
        pass
      
      
      
    #######################################################
    # ______________________________________________________
    # _____________________REAL TIME CANDLE_________________
    # ______________________________________________________
    #######################################################
    def start_candles_stream(self, ACTIVE, size, maxdict):

        if size == "all":
            for s in self.size:
                pass
        elif size in self.size:
            pass
        else:
            logging.error('**error** start_candles_stream please input right size')
            
     def stop_candles_stream(self, ACTIVE, size):
        if size == "all":
            pass
        elif size in self.size:
            pass
        else:
            logging.error('**error** start_candles_stream please input right size')
            
    def get_realtime_candles(self, ACTIVE, size):
        if size == "all":
            try:
                pass
            except:
                logging.error('**error** get_realtime_candles() size="all" can not get candle')
                return False
        elif size in self.size:
            try:
                pass
            except:
                logging.error('**error** get_realtime_candles() size=' + str(size) + ' can not get candle')
                return False
        else:
            logging.error('**error** get_realtime_candles() please input right "size"')
            
            
    def re_subscribe_stream(self):
        try:
            pass
        except:
            pass
        
      
      
    def connect(self):
        try:
            self.api.close()
        except:
            pass
            # logging.error('**warning** self.api.close() fail')
        self.api = QuotexAPI("quotex.market", self.set_ssid)
        check = None
        check, reason = self.api.connect()
        if check == True:
            self.re_subscribe_stream()
            return True, None
        else:
            return False, reason
          
    def close(self):
        try:
            self.api.close()
        except:
            pass
          
    def check_connect(self):
        # True/False
        # if not connected, sometimes it's None, sometimes its '0', so
        # both will fall on this first case
        if not global_value.check_websocket_if_connect:
            return False
        else:
            return True
