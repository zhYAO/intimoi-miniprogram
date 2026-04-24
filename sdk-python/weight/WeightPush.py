import WdtClient
### 称重回传接口
t1 = WdtClient.WdtClient('appkey_weight_qatest', 'F10021@1', 'qatest', 'https://openapitest.huice.com/openapi/')
params = {}
params.update({"logistics_no": 'JT12121212122'})
params.update({"weight": '0.5'})
params.update({"is_setting": '0'})

response = t1.execute("vip_stockout_sales_weight_push.php", params)
print(response)
