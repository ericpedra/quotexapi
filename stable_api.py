# python
from quotexapi.api import QuotexAPI
import quotexapi.global_value as global_value

class Quotex:
  def __init__(self, set_ssid):
        self.size = [1, 5, 10, 15, 30, 60, 120, 300, 600, 900, 1800,
                    3600, 7200, 14400, 28800, 43200, 86400, 604800, 2592000]
        self.set_ssid = set_ssid
   
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
            
       # __________________________BUY__________________________

    # __________________FOR OPTION____________________________
    def buy(self, ACTIVES, price, ACTION, expirations):
        pass
      
    def check_win(self, id_number):
        pass
      
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
