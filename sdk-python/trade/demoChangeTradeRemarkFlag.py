import WdtClient
import json
from wdt_constants import *
# 批量修改订单的标旗
t =  WdtClient.WdtClient(APPKEY, APPSECRET, SID, BASEURL)
params = {}
# 订单id ，多个订单id用,分隔
params.update({"trade_ids":'2627576769963622404,2625366574315339791'})
params.update({"remark_flag": "1"});
response = t.execute("sales_trade_batch_remark_flag.php", params)
print(response)

