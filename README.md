# quotexapi
Quotex Broker API  
https://autotradevip.com/en/  

### Import
from quotexapi.stable_api import IQ_Option

### Login by ssid
if connect sucess return True,None  

if connect fail return False,reason  
```python
from quotexapi.stable_api import Quotex
ssid="""42["authorization",{"session":"0psCurV1ZiFDheOPZbsuPnCscxtZh7veewewqewqewq","isDemo":0}]"""
account=Quotex(set_ssid=ssid)
check_connect,message=account.connect()
print(check_connect,message)
```
### Check_win & buy sample

```python
from quotexapi.stable_api import Quotex
ssid="""42["authorization",{"session":"0psCurV1ZiFDheOPZbsuPnCscxtZh7veewewqewqewq","isDemo":0}]"""
account=Quotex(set_ssid=ssid)
check_connect,message=account.connect()
if check_connect:
    account.change_balance("PRACTICE")#"REAL"
    id = API.buy("AUDCAD_otc", "14000", "put", "60")
    print(API.check_win(id))
```

### Buy Multi

```python
from quotexapi.stable_api import Quotex
ssid="""42["authorization",{"session":"0psCurV1ZiFDheOPZbsuPnCscxtZh7veewewqewqewq","isDemo":0}]"""
account=Quotex(set_ssid=ssid)
check_connect,message=account.connect()
account.change_balance("PRACTICE")#"REAL"
if check_connect:
    account.change_balance("PRACTICE")#"REAL"
    API.buy_multi("AUDCAD_otc", "14000", "put", "60" , 5) #5 trade
```
