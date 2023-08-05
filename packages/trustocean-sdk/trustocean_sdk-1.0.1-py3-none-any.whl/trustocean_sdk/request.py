# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# TRUSTOCEAN API SDK Module
# -------------------------------------------------------------------
# Copyright (c) 2016-2099 环智中诚™ All rights reserved.
# -------------------------------------------------------------------
# Author: JasonLong <jasonlong@qiaokr.com>
# -------------------------------------------------------------------
# FILE: trustocean_sdk/request.py
# GitHub: https://github.com/londry/TRUSTOCEAN-Python-SDK
# -----------------------------------------------------------------
import requests
import json
from .exception import APIError
"""
统一管理用于调用TRUSTOCEAN SSL API远端服务的请求接口
同时，可以在此自定义执行请求前逻辑
或者处理请求后的获得响应信息，比如处理一些特定的报错
"""


class ApiRequest:
    # 默认的API服务器节点，如果您需要使用其他后续公布的接入点，您可以通过构造方法进行覆盖
    _apiBaseServer = "https://api.trustocean.com/ssl/v5/"
    _username = None
    _password = None

    def __init__(self, username, password, new_api_base_server=None):
        if username is None or password is None:
            raise APIError("username and password must be present for make API request")
        self._username = username
        self._password = password
        if new_api_base_server is not None:
            self._apiBaseServer = new_api_base_server

    # 发送请求到环智中诚服务，并获取响应
    def send_request(self, action, params=None):
        if params is None:
            params = {'username': self._username, 'password': self._password}
        else:
            params['username'] = self._username
            params['password'] = self._password
        api_endpoint = self._apiBaseServer+action
        response = requests.post(api_endpoint, params)
        result = json.loads(json.dumps(json.loads(response.content)))
        # angry api error
        if result['status'] == 'error':
            raise APIError(result['message'])
        else:
            return result
