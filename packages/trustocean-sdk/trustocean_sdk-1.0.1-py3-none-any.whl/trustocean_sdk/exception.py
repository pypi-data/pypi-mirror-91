# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# TRUSTOCEAN API SDK Module
# -------------------------------------------------------------------
# Copyright (c) 2016-2099 环智中诚™ All rights reserved.
# -------------------------------------------------------------------
# Author: JasonLong <jasonlong@qiaokr.com>
# -------------------------------------------------------------------
# FILE: trustocean_sdk/exception.py
# GitHub: https://github.com/londry/TRUSTOCEAN-Python-SDK
# -----------------------------------------------------------------
"""
自定义的异常类型
以便于抛出请求异常时被统一的分类处理和识别
"""


class UtilsError(BaseException):
    error_info = None

    def __init__(self, error_info):
        super().__init__()  # 初始化父类
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class APIError(BaseException):
    error_info = None

    def __init__(self, error_info):
        super().__init__()  # 初始化父类
        self.error_info = error_info

    def __str__(self):
        return self.error_info
