# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import List


class Config(TeaModel):
    """
    Model for initing client
    """
    def __init__(
        self,
        access_key_id: str = None,
        access_key_secret: str = None,
        security_token: str = None,
        protocol: str = None,
        read_timeout: int = None,
        connect_timeout: int = None,
        http_proxy: str = None,
        https_proxy: str = None,
        endpoint: str = None,
        no_proxy: str = None,
        max_idle_conns: int = None,
        user_agent: str = None,
        socks_5proxy: str = None,
        socks_5net_work: str = None,
    ):
        # accesskey id
        self.access_key_id = access_key_id
        # accesskey secret
        self.access_key_secret = access_key_secret
        # security token
        self.security_token = security_token
        # http protocol
        self.protocol = protocol
        # read timeout
        self.read_timeout = read_timeout
        # connect timeout
        self.connect_timeout = connect_timeout
        # http proxy
        self.http_proxy = http_proxy
        # https proxy
        self.https_proxy = https_proxy
        # endpoint
        self.endpoint = endpoint
        # proxy white list
        self.no_proxy = no_proxy
        # max idle conns
        self.max_idle_conns = max_idle_conns
        # user agent
        self.user_agent = user_agent
        # socks5 proxy
        self.socks_5proxy = socks_5proxy
        # socks5 network
        self.socks_5net_work = socks_5net_work

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.access_key_id is not None:
            result['accessKeyId'] = self.access_key_id
        if self.access_key_secret is not None:
            result['accessKeySecret'] = self.access_key_secret
        if self.security_token is not None:
            result['securityToken'] = self.security_token
        if self.protocol is not None:
            result['protocol'] = self.protocol
        if self.read_timeout is not None:
            result['readTimeout'] = self.read_timeout
        if self.connect_timeout is not None:
            result['connectTimeout'] = self.connect_timeout
        if self.http_proxy is not None:
            result['httpProxy'] = self.http_proxy
        if self.https_proxy is not None:
            result['httpsProxy'] = self.https_proxy
        if self.endpoint is not None:
            result['endpoint'] = self.endpoint
        if self.no_proxy is not None:
            result['noProxy'] = self.no_proxy
        if self.max_idle_conns is not None:
            result['maxIdleConns'] = self.max_idle_conns
        if self.user_agent is not None:
            result['userAgent'] = self.user_agent
        if self.socks_5proxy is not None:
            result['socks5Proxy'] = self.socks_5proxy
        if self.socks_5net_work is not None:
            result['socks5NetWork'] = self.socks_5net_work
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('accessKeyId') is not None:
            self.access_key_id = m.get('accessKeyId')
        if m.get('accessKeySecret') is not None:
            self.access_key_secret = m.get('accessKeySecret')
        if m.get('securityToken') is not None:
            self.security_token = m.get('securityToken')
        if m.get('protocol') is not None:
            self.protocol = m.get('protocol')
        if m.get('readTimeout') is not None:
            self.read_timeout = m.get('readTimeout')
        if m.get('connectTimeout') is not None:
            self.connect_timeout = m.get('connectTimeout')
        if m.get('httpProxy') is not None:
            self.http_proxy = m.get('httpProxy')
        if m.get('httpsProxy') is not None:
            self.https_proxy = m.get('httpsProxy')
        if m.get('endpoint') is not None:
            self.endpoint = m.get('endpoint')
        if m.get('noProxy') is not None:
            self.no_proxy = m.get('noProxy')
        if m.get('maxIdleConns') is not None:
            self.max_idle_conns = m.get('maxIdleConns')
        if m.get('userAgent') is not None:
            self.user_agent = m.get('userAgent')
        if m.get('socks5Proxy') is not None:
            self.socks_5proxy = m.get('socks5Proxy')
        if m.get('socks5NetWork') is not None:
            self.socks_5net_work = m.get('socks5NetWork')
        return self


class DemoClass(TeaModel):
    def __init__(
        self,
        some_string: str = None,
        some_date: str = None,
        some_boolean: bool = None,
        some_int: int = None,
        some_list: List[str] = None,
    ):
        # 字符串测试
        self.some_string = some_string
        # 日期测试
        self.some_date = some_date
        # Boolean测试
        self.some_boolean = some_boolean
        # 整数测试
        self.some_int = some_int
        # 列表测试
        self.some_list = some_list

    def validate(self):
        if self.some_date is not None:
            self.validate_pattern(self.some_date, 'some_date', '\\d{4}[-]\\d{1,2}[-]\\d{1,2}[T]\\d{2}:\\d{2}:\\d{2}[Z]')

    def to_map(self):
        result = dict()
        if self.some_string is not None:
            result['someString'] = self.some_string
        if self.some_date is not None:
            result['someDate'] = self.some_date
        if self.some_boolean is not None:
            result['someBoolean'] = self.some_boolean
        if self.some_int is not None:
            result['someInt'] = self.some_int
        if self.some_list is not None:
            result['someList'] = self.some_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('someString') is not None:
            self.some_string = m.get('someString')
        if m.get('someDate') is not None:
            self.some_date = m.get('someDate')
        if m.get('someBoolean') is not None:
            self.some_boolean = m.get('someBoolean')
        if m.get('someInt') is not None:
            self.some_int = m.get('someInt')
        if m.get('someList') is not None:
            self.some_list = m.get('someList')
        return self


class AnotherClass(TeaModel):
    def __init__(
        self,
        bar: str = None,
        ref: DemoClass = None,
        ref_list: List[DemoClass] = None,
    ):
        # 测试字段
        self.bar = bar
        # 引用字段
        self.ref = ref
        # 列表引用Struct
        self.ref_list = ref_list

    def validate(self):
        if self.ref:
            self.ref.validate()
        if self.ref_list:
            for k in self.ref_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.bar is not None:
            result['bar'] = self.bar
        if self.ref is not None:
            result['ref'] = self.ref.to_map()
        result['refList'] = []
        if self.ref_list is not None:
            for k in self.ref_list:
                result['refList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('bar') is not None:
            self.bar = m.get('bar')
        if m.get('ref') is not None:
            temp_model = DemoClass()
            self.ref = temp_model.from_map(m['ref'])
        self.ref_list = []
        if m.get('refList') is not None:
            for k in m.get('refList'):
                temp_model = DemoClass()
                self.ref_list.append(temp_model.from_map(k))
        return self


class StatusDemoGatewayCheckRequest(TeaModel):
    def __init__(
        self,
        auth_token: str = None,
        product_instance_id: str = None,
        region_name: str = None,
        aaaa: int = None,
        same: List[DemoClass] = None,
    ):
        self.auth_token = auth_token
        self.product_instance_id = product_instance_id
        self.region_name = region_name
        # ffff
        self.aaaa = aaaa
        # ddddd
        self.same = same

    def validate(self):
        if self.same:
            for k in self.same:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.auth_token is not None:
            result['auth_token'] = self.auth_token
        if self.product_instance_id is not None:
            result['product_instance_id'] = self.product_instance_id
        if self.region_name is not None:
            result['region_name'] = self.region_name
        if self.aaaa is not None:
            result['aaaa'] = self.aaaa
        result['same'] = []
        if self.same is not None:
            for k in self.same:
                result['same'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('auth_token') is not None:
            self.auth_token = m.get('auth_token')
        if m.get('product_instance_id') is not None:
            self.product_instance_id = m.get('product_instance_id')
        if m.get('region_name') is not None:
            self.region_name = m.get('region_name')
        if m.get('aaaa') is not None:
            self.aaaa = m.get('aaaa')
        self.same = []
        if m.get('same') is not None:
            for k in m.get('same'):
                temp_model = DemoClass()
                self.same.append(temp_model.from_map(k))
        return self


class StatusDemoGatewayCheckResponse(TeaModel):
    def __init__(
        self,
        req_msg_id: str = None,
        result_code: str = None,
        result_msg: str = None,
    ):
        self.req_msg_id = req_msg_id
        self.result_code = result_code
        self.result_msg = result_msg

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.req_msg_id is not None:
            result['req_msg_id'] = self.req_msg_id
        if self.result_code is not None:
            result['result_code'] = self.result_code
        if self.result_msg is not None:
            result['result_msg'] = self.result_msg
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('req_msg_id') is not None:
            self.req_msg_id = m.get('req_msg_id')
        if m.get('result_code') is not None:
            self.result_code = m.get('result_code')
        if m.get('result_msg') is not None:
            self.result_msg = m.get('result_msg')
        return self


class EchoDemoGatewayCheckRequest(TeaModel):
    def __init__(
        self,
        auth_token: str = None,
        product_instance_id: str = None,
        region_name: str = None,
    ):
        self.auth_token = auth_token
        self.product_instance_id = product_instance_id
        self.region_name = region_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.auth_token is not None:
            result['auth_token'] = self.auth_token
        if self.product_instance_id is not None:
            result['product_instance_id'] = self.product_instance_id
        if self.region_name is not None:
            result['region_name'] = self.region_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('auth_token') is not None:
            self.auth_token = m.get('auth_token')
        if m.get('product_instance_id') is not None:
            self.product_instance_id = m.get('product_instance_id')
        if m.get('region_name') is not None:
            self.region_name = m.get('region_name')
        return self


class EchoDemoGatewayCheckResponse(TeaModel):
    def __init__(
        self,
        req_msg_id: str = None,
        result_code: str = None,
        result_msg: str = None,
        ddd: int = None,
    ):
        self.req_msg_id = req_msg_id
        self.result_code = result_code
        self.result_msg = result_msg
        # aaa
        self.ddd = ddd

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.req_msg_id is not None:
            result['req_msg_id'] = self.req_msg_id
        if self.result_code is not None:
            result['result_code'] = self.result_code
        if self.result_msg is not None:
            result['result_msg'] = self.result_msg
        if self.ddd is not None:
            result['ddd'] = self.ddd
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('req_msg_id') is not None:
            self.req_msg_id = m.get('req_msg_id')
        if m.get('result_code') is not None:
            self.result_code = m.get('result_code')
        if m.get('result_msg') is not None:
            self.result_msg = m.get('result_msg')
        if m.get('ddd') is not None:
            self.ddd = m.get('ddd')
        return self


