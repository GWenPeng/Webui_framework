import json

import allure
from Common.http_request import Http_client
from Common.thrift_client import Thrift_client
from EFAST import ncTEFAST


class CommonDocDomain(object):
    # @allure.step("修改本域类型")
    # def setSelfDomain(self, host="10.2.176.208", domaintype="parallel", fatherdomain="10.2.176.245"):
    #     """
    #
    #     :param fatherdomain: 父域域名或ip
    #     :param host: 本域域名或ip
    #     :param domaintype: 本域类型
    #     :return: None
    #     """
    #     client = Http_client(tagname="HTTPGWP")
    #     client.put(url="https://" + host + ":443/api/document-domain-management/v1/domain/self/type",
    #                header='{"Content-Type":"application/json"}',
    #                json={"type": domaintype, "host": fatherdomain})
    #     assert client.status_code == 200

    @allure.step("查询本域的详情")
    def getSelfDomain(self, host):
        """

        :param host: 本域域名或ip
        :return:jsonResponse
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url="https://" + host + ":443/api/document-domain-management/v1/domain/self",
                   header='{"Content-Type":"application/json"}')
        assert client.status_code == 200
        return client.jsonResponse

    @allure.step("查询关系域的详情")
    def getRelationDomain(self, uuid, host="10.2.176.245"):
        """

        :param host:
        :param uuid: 关系域UUID
        :return:jsonResponse
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url="https://" + host + ":443/api/document-domain-management/v1/domain/" + uuid,
                   header='{"Content-Type":"application/json"}')
        print(client.jsonResponse)
        assert client.status_code == 200
        return client.jsonResponse

    @allure.step("查询关系域列表")
    def getRelationDomainList(self, host="10.2.176.245", keyword="", offset=0, limit=1000):
        """

        :param limit: 获取数据量，默认20;如果limit为-1，则获取所有数据;如果limit小于-1，则忽略该参数，使用默认值;如果limit大于200，则设置为200
        :param offset:获取数据起始下标，0开始，默认0;如果start小于0，则忽略该参数，使用默认值;如果start大于数据总数，则返回空列表
        :param keyword:搜索的关键字，可以为关系域域名，支持模糊搜索； 如果不填，返回所有结果
        :param host: 本域域名或ip
        :return:jsonResponse
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="https://" + host + ":443/api/document-domain-management/v1/domain",
            params={"keyword": keyword, "start": offset, "limit": limit},
            header='{"Content-Type":"application/json"}')
        if client.status_code == 200:
            return client.jsonResponse
        else:
            return client.status_code

    @allure.step("删除关系域")
    def delRelationDomain(self, host="10.2.176.245", uuid=""):
        """

        :param uuid: 关系域的id
        :param host: 关系域域名或ip
        :return:None
        """
        client = Http_client(tagname="HTTPGWP")
        res = CommonDocDomain().getRelationDomain(uuid=uuid, host=host)
        if res["port"] != 443:
            client.put(url="/api/document-domain-management/v1/domain/" + res["id"],
                       header='{"Content-Type":"application/json"}',
                       json={"type": res["type"], "port": 443, "app_id": "appid", "app_key": "appkey"})
        client.delete(url="https://" + host + ":443/api/document-domain-management/v1/domain/" + uuid,
                      header='{"Content-Type":"application/json"}')
        # assert client.status_code == 200
        if client.status_code == 409:
            assert client.jsonResponse["code"] == 409000
            assert client.jsonResponse["message"] == "Conflict resource."
        return client.status_code

    @allure.step("添加关系域")
    def addRelationDomain(self, host, port=443, domaintype="child", app_id="admin",
                          app_key="eisoo.cn", httphost="10.2.176.245", network_type="direct"):
        """
        默认添加子域为关系域
        :param network_type:
        :param httphost: http的域
        :param app_key:
        :param app_id:
        :param port:
        :param domaintype: 域类型 child or parallel
        :param host: 域名或者ip
        :return:添加成功的关系域uuid
        """
        if isinstance(host, str):
            host = [host]
        uuid = None
        uuids = []
        for h in host:
            client = Http_client(tagname="HTTPGWP")
            if app_id is None and app_key is None:
                client.post(url="https://" + httphost + ":443/api/document-domain-management/v1/domain/",
                            header='{"Content-Type":"application/json"}',
                            jsondata={"host": h, "port": port, "type": domaintype, "network_type": network_type})
            else:
                client.post(url="https://" + httphost + ":443/api/document-domain-management/v1/domain/",
                            header='{"Content-Type":"application/json"}',
                            jsondata={"host": h, "port": port, "type": domaintype, "app_id": app_id, "app_key": app_key,
                                      "network_type": network_type})
            # print(httphost, host, domaintype)
            print(client.jsonResponse)
            assert client.status_code == 201
            location = client.respheaders['Location']
            uuid = location.split("/")[-1]
            uuids.append(uuid)
        if len(uuids) == 1:
            return uuids[0]
        else:
            return uuids

    @allure.step("递归清除所有的关系域")
    def clearRelationDomain(self, host=None):
        """
        :param host:要清除的本域域名或IP
        :return: None
        """
        if host is None:
            host = ["10.2.176.245"]
        if isinstance(host, str):
            host = [host]

        for Host in host:
            print(Host)
            L = CommonDocDomain().getRelationDomainList(host=Host)
            if isinstance(L, int):
                print(L)
            elif len(L["data"]) != 0:
                for index in range(len(L["data"])):
                    CommonDocDomain().delRelationDomain(host=Host, uuid=L["data"][index]["id"])
        return None

    @allure.step("设置关系域详情")
    def setRelationDomain(self, uuid, domaintype="parallel", port=443, app_id="admin", app_key="eisoo.cn", secret=""):
        """
        :param secret:传输密钥
        :param domaintype:关系域类型，可填：child, parallel
        :param app_id:app_id，可为任何不为空的字符串
        :param app_key:app_key，可为任何不为空字符串
        :param port:关系域端口，必须大于等于1，小于等于65535；
        :param uuid:关系域uuid
        :return:None
        """
        if domaintype == "parallel":
            data = {"type": domaintype, "port": port, "app_id": app_id, "app_key": app_key, "secret": secret}
        else:
            data = {"type": domaintype, "port": port, "app_id": app_id, "app_key": app_key}
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/document-domain-management/v1/domain/" + uuid,
                   header='{"Content-Type":"application/json"}', json=data)
        assert client.status_code == 200
        return None

    @allure.step("获取策略列表")
    def getPolicyList(self, httphost="10.2.176.245", key_word="", offset=0, limit=1000):
        """

        :param offset:
        :param limit:
        :param httphost:
        :param key_word:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl",
                   params={"key_word": key_word, "start": offset, "limit": limit},
                   header='{"Content-Type":"application/json"}')
        return client.jsonResponse

    @allure.step("新增策略")
    def addPolicy(self, httphost="10.2.176.245", content=None, name="PolicyName"):
        """

        :param content:
        :param name:
        :param httphost:
        :return:
        """
        if content is None:
            content = [{"name": "password_strength_meter", "value": {"enable": False, "length": 8}}]
        client = Http_client(tagname="HTTPGWP")
        client.post(url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl",
                    jsondata={"content": content, "name": name}, header='{"Content-Type":"application/json"}')
        assert client.status_code == 201
        location = client.respheaders['Location']
        uuid = location.split("/")[-1]
        return uuid

    @allure.step("删除策略")
    def deletepolicy(self, httphost="10.2.176.245", PolicyUUID=None):
        client = Http_client()
        client.delete(url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl/" + PolicyUUID,
                      header='{"Content-Type":"application/json"}')
        return client.status_code

    @allure.step("子域绑定策略")
    def BoundPolicy(self, httphost="10.2.176.245", PolicyUUID=None, ChildDomainUUID=None):
        """

        :param ChildDomainUUID:
        :param PolicyUUID:
        :param httphost:
        :return:
        """

        client = Http_client(tagname="HTTPGWP")
        client.put(
            url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl/" + PolicyUUID + "/bound-domain/" + ChildDomainUUID,
            header='{"Content-Type":"application/json"}')
        return client.status_code

    @allure.step("子域解除策略绑定")
    def delboundPolicy(self, httphost="10.2.176.245", PolicyUUID=None, ChildDomainUUID=None):
        """

        :param ChildDomainUUID:
        :param PolicyUUID:
        :param httphost:
        :return:
        """

        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl/" + PolicyUUID + "/bound-domain/" + ChildDomainUUID,
            header='{"Content-Type":"application/json"}')
        return client.status_code

    @allure.step("获取已绑定策略的子域")
    def getBoundPolicyChild(self, httphost="10.2.176.245", ChildDomainUUID=None):
        """

        :param ChildDomainUUID:
        :param httphost:
        :return:
        """

        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="https://" + httphost + ":443/api/document-domain-management/v1/domain/" + ChildDomainUUID + "/bound-policy-tpl",
            header='{"Content-Type":"application/json"}')
        return client.jsonResponse

    @allure.step("获取策略已绑定的子文档域")
    def getPolicyChildDomainList(self, httphost="10.2.176.245", policyuuid=None):
        """

        :param httphost:
        :param policyuuid:
        :return:
        """

        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl/" + policyuuid + "/bound-domain?offset=0&limit"
                                                                                                            "=1000 "
                                                                                                            "&key_word=",
            header='{"Content-Type":"application/json"}')
        return client.jsonResponse

    @allure.step("清空绑定子域策略")
    def clearBoundPolicyChild(self, httphost, policyuuid):
        """

        :param httphost:
        :param policyuuid:
        :return:
        """
        res = CommonDocDomain().getPolicyChildDomainList(httphost=httphost, policyuuid=policyuuid)
        if len(res["data"]) != 0:
            for index in range(len(res["data"])):
                CommonDocDomain().delboundPolicy(httphost=httphost, PolicyUUID=policyuuid,
                                                 ChildDomainUUID=res["data"][index]["id"])
        return None

    @allure.step("获取同步计划列表")
    def getSynchronizationPlanList(self, httphost="10.2.176.245", offset="0", limit="1000", key_word=""):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="https://" + httphost + ":443/api/document-domain-management/v1/library-sync?start=" + offset +
                "&limit=" + limit + "&key_word=" + key_word,
            header='{"Content-Type":"application/json"}')
        return client.jsonResponse

    @allure.step("创建文档库同步计划")
    def creatSynchronizationPlan(self, httphost="10.2.176.245", jsondata=None, mode="live", docid=None, domainid=None,
                                 libname=None):
        """

        :param libname:
        :param domainid:
        :param docid:
        :param mode:
        :param httphost:
        :param jsondata:
        :return:
        ''"""
        if jsondata is None:
            jsondata = {"interval": {"mode": mode}, "source": {"id": docid},
                        "target": {"domain": {"id": domainid}, "library": libname}}
        client = Http_client(tagname="HTTPGWP")
        client.post(url="https://" + httphost + ":443/api/document-domain-management/v1/library-sync",
                    jsondata=jsondata,
                    header='{"Content-Type":"application/json"}')
        return client.jsonResponse

    @allure.step("设置登录认证方式")
    def set_auth_login(self, httphost):
        client = Http_client(tagname="HTTPGWP")
        data = """
                [{"name":"multi_factor_auth",
                "value":{"enable":false,"image_vcode":false,"password_error_count":0,"sms_vcode":false,"otp":false}
                }]
                """
        client.put(url="https://" + httphost + ":443/api/policy-management/v1/general/multi_factor_auth/value",
                   header='{"Content-Type":"application/json"}', data=data)
        # print(client.status_code)
        return client.status_code

    @allure.step("搜索策略配置列表")
    def getPolicyIDNameByKeyword(self, httphost="10.2.176.245", offset="0", limit="1000", key_word=""):
        """

        :param offset:
        :param key_word:
        :param limit:
        :param httphost:
        :param policyuuid:
        :return:
        """

        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="https://" + httphost + "/api/document-domain-management/v1/policy-tpl",
            params={"start": offset, "limit": limit, "key_word": key_word},
            header='{"Content-Type":"application/json"}')
        return client.jsonResponse

    @allure.step("设置密码强度")
    def set_password_str(self, httphost):
        client = Http_client()
        data = [{"name": "password_strength_meter",
                 "value": {"enable": False, "length": 8}}]
        client.put(url="https://" + httphost + ":443/api/policy-management/v1/general/password_strength_meter/value",
                   header='{"Content-Type":"application/json"}', data=json.dumps(data))

        return client.status_code

    @allure.step("设置客户端登录选项")
    def set_clientLogin_Options(self, httphost):
        client = Http_client()
        data = [{"name": "client_restriction",
                 "value": {"pc_web": False, "mobile_web": False, "windows": False, "ios": False, "mac": False,
                           "android": False}}]
        client.put(url="https://" + httphost + ":443/api/policy-management/v1/general/client_restriction/value",
                   header='{"Content-Type":"application/json"}', data=json.dumps(data))
        print(client.status_code)
        return client.status_code

    @allure.step("删除用户")
    def del_user(self, user_id, host="10.2.176.245"):
        """

        :param host:
        :param user_id:
        :return:
        """
        tc = Thrift_client(host=host)
        tc.client.Usrm_DelUser(userId=user_id)
        tc.close()

    @allure.step("关闭个人文档")
    def close_person_doc(self, user_id="0d7194e0-9035-11ea-b57b-00505682e19f", host="10.2.176.245"):
        """
        EACP_DeleteUserDoc
        :return:
        """
        tc = Thrift_client(host=host, service=ncTEFAST, port=9121)
        tc.client.EFAST_DeleteUserDoc(userId=user_id, deleterId=None)
        tc.close()
