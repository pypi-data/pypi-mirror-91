# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# TRUSTOCEAN API SDK Module
# -------------------------------------------------------------------
# Copyright (c) 2016-2099 环智中诚™ All rights reserved.
# -------------------------------------------------------------------
# Author: JasonLong <jasonlong@qiaokr.com>
# -------------------------------------------------------------------
# FILE: trustocean_sdk/client.py
# GitHub: https://github.com/londry/TRUSTOCEAN-Python-SDK
# -----------------------------------------------------------------
from .request import ApiRequest


# 产品可能会支持的所有订购周期, 具体不同产品可能支持的订购数量不同
class ProductPeriodHelper:
    # 1个月有效期
    PERIOD_MONTHLY_1_MONTH = 'monthly'
    # 3个月有效期
    PERIOD_QUARTERLY_3_MONTHS = 'quarterly'
    # 1年有效期
    PERIOD_ANNUALLY_12_MONTHS = 'annually'
    # 2年有效期
    PERIOD_BIENNIALLY_24_MONTHS = 'biennially'
    # 3年有效期
    PERIOD_TRIENNIALLY_36_MONTHS = 'triennially'
    # 4年有效期
    PERIOD_QUADRENNIAL_48_MONTHS = 'quadrennial'
    # 5年有效期
    PERIOD_QUINQUENNIAL_60_MONTHS = 'quinquennial'


# 产品的验证方式, 邮箱验证方式应该填写具体的域名邮箱地址
class DomainValidationMethodHelper:
    HTTP_FILE = 'http'
    HTTPS_FILE = 'https'
    DNS_CNAME = 'dns'


class APIClient:
    REQUEST = None

    def __init__(self, username: str, password: str):
        self.REQUEST = ApiRequest(username, password)

    # 检查API服务是否连接正常
    def check_service_status(self) -> dict:
        return self.REQUEST.send_request('ping')

    # 获取API账户基本信息
    def get_account_info(self) -> dict:
        return self.REQUEST.send_request('getProfileInfo')

    # 获取账户内可订购的产品和定价列表
    def get_product_list(self) -> dict:
        return self.REQUEST.send_request('getProductList')

    # 从远端生成域名预验证信息
    def get_pre_domain_validation_information(self, domains: list, csr_code: str, unique_id: str) -> dict:
        return self.REQUEST.send_request('getPreDomainValidationInformation',
                                         {'domains': ','.join(domains), 'csr_code': csr_code, 'unique_id': unique_id}
                                         )

    # 创建新的SSL订单
    def create_new_ssl_order(self,
                             pid: str,
                             csr_code: str,
                             period: str,
                             dcv_method: list,
                             unique_id: str,
                             contact_email: str,
                             callback_url: str = None,
                             domains: list = None,
                             organization_name: str = None,
                             organizational_unit_name: str = None,
                             registered_address_line1: str = None,
                             registered_no: str = None,
                             country: str = None,
                             state: str = None,
                             city: str = None,
                             postal_code: str = None,
                             organization_phone: str = None,
                             date_of_incorporation: str = None,
                             contact_name: str = None,
                             contact_title: str = None,
                             contact_phone: str = None,
                             renew: str = None
                             ) -> dict:
        params = {
            'pid': pid,
            'csr_code': csr_code,
            'period': period,
            'dcv_method': ','.join(dcv_method),
            'unique_id': unique_id,
            'contact_email': contact_email,
            'callback': callback_url,
            'domains': ','.join(domains),
            'renew': renew,
            'organization_name': organization_name,
            'organizationalUnitName': organizational_unit_name,
            'registered_address_line1': registered_address_line1,
            'registered_no': registered_no,
            'country': country,
            'state': state,
            'city': city,
            'postal_code': postal_code,
            'organization_phone': organization_phone,
            'date_of_incorporation': date_of_incorporation,
            'contact_name': contact_name,
            'contact_title': contact_title,
            'contact_phone': contact_phone
        }
        return self.REQUEST.send_request('addSSLOrder', params)

    # 从API服务中创建一个不重复的UniqueID
    def create_unique_id(self) -> str:
        result = self.REQUEST.send_request('createNewUniqueId')
        return result['unique_id']

    # 检查自定义生成的Unique_id是否可用
    def check_unique_id(self, unique_id: str) -> dict:
        params = {'unique_id': unique_id}
        return self.REQUEST.send_request('checkUniqueId', params)

    # 获取SSL订单的域名验证信息
    def get_domain_validation_status(self, trustocean_id: str) -> dict:
        return self.REQUEST.send_request('getDomainValidationStatus', {'trustocean_id': trustocean_id})

    # 通知CA重新执行域名验证DCV，或者重新发送验证邮件（如果有的域名选择了邮件验证方式）
    def retry_dcv_email_or_dcv_check(self, trustocean_id: str) -> dict:
        return self.REQUEST.send_request('reTryDcvEmailOrDCVCheck', {'trustocean_id': trustocean_id})

    # 修改订单中域名的验证方式
    def change_dcv_method_of_domain(self, trustocean_id: str, domain: str, new_dcv_method: str) -> dict:
        return self.REQUEST.send_request('changeDCVMethod', {
            'trustocean_id': trustocean_id,
            'method': new_dcv_method,
            'domain': domain}
                                         )

    # 移除SSL订单中无法通过DCV验证的域名
    def remove_san_domain(self, trustocean_id: str, domain: str) -> dict:
        return self.REQUEST.send_request('removeSanDomain', {'trustocean_id': trustocean_id, 'domain': domain})

    # 查询订单状态摘要
    def get_order_status(self, trustocean_id: str) -> dict:
        return self.REQUEST.send_request('getOrderStatus', {'trustocean_id': trustocean_id})

    # 查询订单详细信息
    def get_order_details(self, trustocean_id: str) -> dict:
        return self.REQUEST.send_request('getSSLDetails', {'trustocean_id': trustocean_id})

    # 重新签发SSL证书，用于更换私钥/CSR
    def reissue_ssl_order(self,
                          trustocean_id: str,
                          csr_code: str,
                          contact_email: str,
                          dcv_method: list,
                          unique_id: str,
                          domains: list = None
                          ) -> dict:
        params = {
            'trustocean_id': trustocean_id,
            'csr_code': csr_code,
            'contact_email': contact_email,
            'dcv_method': ','.join(dcv_method),
            'unique_id': unique_id,
            'domains': ','.join(domains)
        }
        return self.REQUEST.send_request('reissueSSLOrder', params)

    # 吊销SSL证书订单，吊销操作视为放弃此订单的所有权限，执行后此订单将无法操作
    def revoke_ssl(self, trustocean_id: str, revocation_reason: str) -> dict:
        return self.REQUEST.send_request('revokeSSL', {'trustocean_id': trustocean_id, 'revocation_reason': revocation_reason})

    # 提交退款申请, 提交后将等待CA审核后完成退款，退款后订单将会取消，状态通过callback url通知
    def cancel_and_refund(self, trustocean_id: str) -> dict:
        return self.REQUEST.send_request('cancelAndRefund', {'trustocean_id', trustocean_id})

    # 获取订单退款申请的处理状态
    def get_refund_status(self, trustocean_id: str) -> dict:
        return self.REQUEST.send_request('checkRefundStatus', {'trustocean_id': trustocean_id})

    # 获取包含价格信息的产品列表
    def get_product_list_with_pricing(self) -> dict:
        return self.REQUEST.send_request('getProductListWithPricing')
