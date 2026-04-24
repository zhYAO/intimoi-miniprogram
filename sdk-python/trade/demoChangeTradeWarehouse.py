
#  修改系统订单的仓库店铺
import WdtClient
import json
from wdt_constants import *
t =  WdtClient.WdtClient(APPKEY, APPSECRET, SID, BASEURL)
params = {}
# 订单号 页面展示的系统订单号
params.update({"trade_no":'JY2505130492'})
# 仓库id
params.update({"warehouse_id": "6"})
# 物流id
params.update({"logistics_id": "2675780066033532930"})
response = t.execute("sales_trade_modify.php", params)
print(response)