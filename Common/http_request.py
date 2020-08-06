# coding=utf8
from Common.readConfig import readconfigs
from requests.exceptions import ConnectTimeout
from json.decoder import JSONDecodeError
from Common.get_token import Token
from urllib3.exceptions import InsecureRequestWarning
from functools import lru_cache
import requests
import os
import json
import warnings

warnings.filterwarnings(action='ignore', category=InsecureRequestWarning)


class Http_client:
    # 初始化api数据
    def __init__(self, tagname="HTTP"):
        readconfig = readconfigs()
        self.host = readconfig.get_http(tagname=tagname, name='baseUrl')
        self.timeout = float(readconfig.get_http(tagname=tagname, name='timeout'))
        self.none = None
        self.status_code = self.none
        self.text = self.none  # 一个str类型reponsedata对象
        self.content = self.none
        self.jsonResponse = self.none  # 一个dict类型reponsedata对象
        self.respheaders = self.none
        # 返回response headers对象
        self.URL = self.none
        self.elapsed = self.none
        # 完成一个请求总耗时，单位s
        # Token(self)
        # self.access_token = token["access_token"]
        # self.access_token = token

    @staticmethod
    # @lru_cache()
    def add_token(token_host):
        header = {"Content-Type": "application/json",
                  "Authorization": "Bearer " + Token(host=token_host).get_token()["access_token"]}
        return header

    # 封装request.get方法
    def get(self, url, params=None, header=None, encoding='utf_8', **kwargs):
        if isinstance(header, str):
            header = eval(header)
        if "http" in url:
            token_host = url.split("//")[1].split("/")[0]
            if ":" in token_host:
                token_host = token_host.split(":")[0]
        else:
            token_host = self.host.split("//")[1]
            if ":" in token_host:
                token_host = token_host.split(":")[0]
            url = self.host + url

        try:
            header.update(self.add_token(token_host=token_host))
            resp = requests.get(url=url, params=params, headers=header, timeout=self.timeout, verify=False,
                                **kwargs)

        except ConnectTimeout as e:
            print("ConnectTimeout Error!")
            return e
        resp.encoding = encoding
        self.status_code = resp.status_code
        self.text = resp.text
        self.content = resp.content
        self.respheaders = resp.headers
        self.URL = resp.url
        try:
            self.jsonResponse = resp.json()
        except JSONDecodeError as error:
            print("Response JSONDecodeError ! %s" % error)
        self.elapsed = resp.elapsed.total_seconds()

    # 封装requests.post方法ss
    def post(self, url, params=None, jsondata=None, header=None, encoding='utf_8', **kwargs):
        if isinstance(jsondata, str):
            jsondata = eval(jsondata)
        if isinstance(header, str):
            header = eval(header)
        if "http" in url:
            token_host = url.split("//")[1].split("/")[0]
            if ":" in token_host:
                token_host = token_host.split(":")[0]
        else:
            token_host = self.host.split("//")[1]
            if ":" in token_host:
                token_host = token_host.split(":")[0]
            url = self.host + url
        try:
            header.update(self.add_token(token_host=token_host))
            resp = requests.post(url=url, data=params, json=jsondata, headers=header,
                                 timeout=self.timeout, verify=False, **kwargs)

        except ConnectTimeout as e:
            print("ConnectTimeout Error!")
            return e
        resp.encoding = encoding
        self.status_code = resp.status_code
        self.text = resp.text
        self.content = resp.content
        self.respheaders = resp.headers
        self.URL = resp.url
        try:
            self.jsonResponse = resp.json()
        except JSONDecodeError as error:
            print("Response JSONDecodeError ! %s" % error)
        self.elapsed = resp.elapsed.total_seconds()

    # 封装requests.put方法
    def put(self, url, data=None, header=None, encoding='utf_8', **kwargs):
        if isinstance(header, str):
            header = eval(header)
        if "http" in url:
            token_host = url.split("//")[1].split("/")[0]
            if ":" in token_host:
                token_host = token_host.split(":")[0]
        else:
            token_host = self.host.split("//")[1]
            if ":" in token_host:
                token_host = token_host.split(":")[0]
            url = self.host + url
        try:
            header.update(self.add_token(token_host=token_host))
            resp = requests.put(url=url, data=data, headers=header, verify=False, **kwargs)

        except ConnectTimeout as e:
            print("ConnectTimeout Error!")
            return e
        resp.encoding = encoding
        self.status_code = resp.status_code
        self.text = resp.text
        self.content = resp.content
        self.respheaders = resp.headers
        self.URL = resp.url
        try:
            self.jsonResponse = resp.json()
        except JSONDecodeError as error:
            print("Response JSONDecodeError ! %s" % error)
        self.elapsed = resp.elapsed.total_seconds()

    # 封装requests.delete方法
    def delete(self, url, params=None, jsondata=None, header=None, encoding='utf_8', **kwargs):
        if isinstance(jsondata, str):
            jsondata = eval(jsondata)
        if isinstance(header, str):
            header = eval(header)
        if "http" in url:
            token_host = url.split("//")[1].split("/")[0]
            if ":" in token_host:
                token_host = token_host.split(":")[0]
        else:
            token_host = self.host.split("//")[1]
            if ":" in token_host:
                token_host = token_host.split(":")[0]
            url = self.host + url
        try:
            header.update(self.add_token(token_host=token_host))
            resp = requests.delete(url=url, params=params, json=jsondata, headers=header,
                                   timeout=self.timeout, verify=False, **kwargs)

        except ConnectTimeout as e:
            print("ConnectTimeout Error!")
            return e
        resp.encoding = encoding
        self.status_code = resp.status_code
        self.text = resp.text
        self.content = resp.content
        self.respheaders = resp.headers
        self.URL = resp.url
        try:
            self.jsonResponse = resp.json()
        except JSONDecodeError as error:
            print("Response JSONDecodeError ! %s" % error)
        self.elapsed = resp.elapsed.total_seconds()


if __name__ == '__main__':
    hc = Http_client()
    hc.get(url="https://10.2.180.130/api/document-domain-management/v1/domain/self",
           header={"Content-Type": "application/json",
                   "Authorization": "Bearer 06xzzIBHg4OaJR1drP6rG3K1JmEebDBSqcPigsQVykk.hIomct7lQd2BvaUsXZGjdeUCtuCezrh3Fm01U-vxOzE"})
    print(hc.jsonResponse)
    # token().get_token()
    # test delete方法
    # client = Http_client()
    # client.delete(url="/api/user/group/users", jsondata={
    #     "userOIDs": ["16a6ade1-0cc4-4588-8fc2-9067d9e3ff7e"],
    #     "userGroupOID": "5974a2c9-1607-46e9-8edb-ed88bf0c7a6e"
    # }, header={"Authorization": "bearer 61190e74-8c66-4fbf-bb0d-e5a382407827"})
    # print(client.text)
    # print(client.status_code)
    # print(client.elapsed)
    # print(client.headers)
    # print(client.URL)
    # header = {"Authorization": "Basic QXJ0ZW1pc0FwcDpuTENud2RJaGl6V2J5a0h5dVpNNlRwUURkN0t3SzlJWERLOExHc2E3U09X"}
    # print(type(header))
    # client = Http_client()
    # client.post(url="/oauth/token",
    #             params={"username": "13323454321", "password": "hly123", "grant_type": "password", "scope": "write"},
    #             header={
    #                 "Authorization": "Basic QXJ0ZW1pc0FwcDpuTENud2RJaGl6V2J5a0h5dVpNNlRwUURkN0t3SzlJWERLOExHc2E3U09X"})
    # print(client.jsonResponse)
    # print(client.status_code)
    # print(client.headers)
    # print(client.URL)
    # cl = Http_client()
    # res = cl.get(url="https://10.2.176.245", encoding='utf-8')
    # # res = requests.get(url="https://10.2.176.245", cert=('ca.crt', 'ca.key'))
    # # res.encoding = 'utf-8'
    # print(cl.text)
# test put方法
#     client = Http_client()
#     str={
#   "customEnumerationOID": "d3dd03de-0e08-451a-9c0f-a743d5413136",
#   "name": "类别-测试222",
#   "fieldType": "TEXT",
#   "enabled": True,
#   "values": [
#     {
#       "messageKey": "amusement",
#       "value": "娱乐",
#       "enabled": True
#     },
#     {
#       "messageKey": "repast",
#       "value": "餐饮",
#       "enabled": True
#     },
#     {
#       "messageKey": "work",
#       "value": "办公",
#       "enabled": True
#     },
#      {
#       "messageKey": "conference",
#       "value": "会务",
#       "enabled": True
#     }
#   ]
# }
#     data=json.dumps(str)
#     print(data)
#     client.put(url="/api/custom/enumerations",data=data,header={"Authorization": "Bearer 61190e74-8c66-4fbf-bb0d-e5a382407827",
#                         "Content-Type": "application/json"})
#     print(client.text)
#     print(client.status_code)
#     print(client.headers)
#     print(client.URL)


# 添加部门
#     client = Http_client()
#     client.post(url="/api/ShareMgnt/Usrm_AddDepartment",jsondata=[{"ncTAddDepartParam":{"parentId":"979fddf2-ef36-11e9-93ac-005056828221","departName":"部门2","siteId":"59eb04f2-ef2f-11e9-8753-005056828221"}}], header={
#         "Cookie": "csrftoken=xSBDp62yT9FfWPg9Qoz0O8ycbNfjFLit; clustersid=s%3Ag0bWPOyza9rCwWFwkvGeCEA2qZ2GWFWK.%2FX%2FrXQzUVkUU84VR6eGCsPD8K2OW4nZoRhTPBLFa2MA; clustertoken=97389ca0-ecbb-11e9-9e2c-1dbf94e236bc; sessionid=4da5m9v7t6rhyexjwlcdj1dd04x44g4s; consoletoken=cd38044e-9634-11ea-acd9-005056828221; lastVisitedOrigin=http%3A%2F%2F10.2.180.162",
#         "X-CSRFToken": "xSBDp62yT9FfWPg9Qoz0O8ycbNfjFLit"})
#     print(client.text)
#     print(client.status_code)
#     print(client.headers)
#     print(client.URL)

# 删除部门接口
#     client = Http_client()
#     client.post(url="/interface/department/deldepartment/",params={"id": "e85dc360-9659-11ea-abab-005056828221","managerid":"266c6a42-6131-4d62-8f39-853e7093701c"}, header={
#         "Cookie": "csrftoken=xSBDp62yT9FfWPg9Qoz0O8ycbNfjFLit; clustersid=s%3Ag0bWPOyza9rCwWFwkvGeCEA2qZ2GWFWK.%2FX%2FrXQzUVkUU84VR6eGCsPD8K2OW4nZoRhTPBLFa2MA; clustertoken=97389ca0-ecbb-11e9-9e2c-1dbf94e236bc; sessionid=4da5m9v7t6rhyexjwlcdj1dd04x44g4s; consoletoken=cd38044e-9634-11ea-acd9-005056828221; lastVisitedOrigin=http%3A%2F%2F10.2.180.162",
#         "X-CSRFToken": "xSBDp62yT9FfWPg9Qoz0O8ycbNfjFLit"})
#     print(client.text)
#     print(client.status_code)
#     print(client.headers)
#     print(client.URL)
