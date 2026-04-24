import hashlib
import datetime
import calendar
import time
import urllib
import urllib.parse
import requests

def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.digest()

def md5GBK(str1):
    m = hashlib.md5(str1.encode(encoding = 'gb2312'))
    return m.hexdigest()

def byte2hex(list1):
    sign = []
    for i in list1:
        # a_bytes = bytes.fromhex(i & 0xFF)
        a_bytes = '{:02X}'.format(i)
        sign.append(a_bytes)
    return ''.join(sign).lower()

def doPost(url, params, charset, connectTimeout, readTimeout, header):
    ctype = "application/x-www-form-urlencoded;charset=" + charset
    query = buildQuery(params, charset)
    content = []
    if len(query) != 0:
        content = bytearray(query, charset)
    return _doPost(url, ctype, params, content, charset, connectTimeout, readTimeout, header)

def buildQuery(params, charset):
    if not params:
        return None
    query = []
    hasParam = False
    for key in params:
        name = key
        value = params[key]
        if name != None and len(name) > 0 and value != None and len(value) > 0:
            if hasParam:
                query.append("&")
            else:
                hasParam = True
            query.append(name)
            query.append("=")
            query.append(urllib.parse.unquote(value))
    return ''.join(query)

def _doPost(url, ctype, params, content, charset, connectTimeout, readTimeout, header):
    # data = {'Accept':'*/*','User-Agent':'wdt-python-sdk','Content-Type':ctype}
    # headers = {"Content-Tpye": ctype}
    # response = requests.post(url, data, headers)
    # req = urllib.request.Request(url)
    # res_data = urllib.request.urlopen(req)
    # res = res_data.read()
    response = requests.post(url, params)
    return response.text



class WdtClient:
    connectTimeout = 3000
    readTimeout = 15000

    def __init__(self,appkey,appsecret,sid,baseUrl):
        self.appkey = appkey
        self.appsecret = appsecret
        self.sid = sid
        self.baseUrl = baseUrl
        if not self.baseUrl.endswith("/"):
            self.baseUrl = self.baseUrl + "/"

    def signRequest(self, params, appsecret):
        # keys = tuple(params.keys())
        # list.sort(keys)
        keys = sorted(params.keys())
        key = []
        query = ""
        for i in keys:
            key.append(i)
        for i in key:
            if i == "sign":
                continue
            if len(query) > 0:
                query = query + ';'
            length = len(i)
            query = query + "{:02n}".format(length)
            query = query + '-'
            query = query + i
            query = query + ':'
            value = params[i]
            length = len(value)
            query = query + "{:04n}".format(length)
            query = query + '-'
            query = query + value
        query = query + appsecret
        # return byte2hex(bytes(md5(query), encoding="utf8"))
        return byte2hex(md5(query))

    def execute(self, relativeUrl, params):
        params.update({"appkey": self.appkey})
        params.update({"sid": self.sid})
        # now_time = datetime.datetime.now()
        # now =now_time.strftime("%Y-%m-%d %H:%M:%S")
        # params.update({"timestamp": str(calendar.timegm(time.strptime(now, '%Y-%m-%d %H:%M:%S')))})
        params.update({"timestamp": str(int(time.time()))})
        params.update({"sign": self.signRequest(params, self.appsecret)})
        return doPost(self.baseUrl + relativeUrl, params, "UTF-8", 3000, 15000, None)