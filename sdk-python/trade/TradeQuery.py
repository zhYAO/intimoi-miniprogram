import WdtClient
## 订单查询接口
t = WdtClient.WdtClient('appkey_market_test', 'AFX2fD4pt', 'haijun', 'https://openapitest.huice.com/openapi/')
params = {}
params.update({"start_time": '2024-12-19 16:00:00'})
params.update({"end_time": '2024-12-19 17:00:00'})
params.update({"page_size": '100'})
params.update({"page_no": '0'})

response = t.execute("trade_query.php", params)
print(response)


