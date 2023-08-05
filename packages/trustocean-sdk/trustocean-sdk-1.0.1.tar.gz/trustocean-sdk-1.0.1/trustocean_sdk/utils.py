# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# TRUSTOCEAN API SDK Module
# -------------------------------------------------------------------
# Copyright (c) 2016-2099 环智中诚™ All rights reserved.
# -------------------------------------------------------------------
# Author: JasonLong <jasonlong@qiaokr.com>
# -------------------------------------------------------------------
# FILE: trustocean_sdk/utils.py
# GitHub: https://github.com/londry/TRUSTOCEAN-Python-SDK
# -----------------------------------------------------------------
from OpenSSL import crypto
from .exception import UtilsError
import zipfile
import pem
import tempfile

"""
统一管理用于调用TRUSTOCEAN SSL API远端服务的请求接口
同时，可以在此自定义执行请求前逻辑
或者处理请求后的获得响应信息，比如处理一些特定的报错
"""


# 转换PEM格式的证书为PFX PKCS12格式，适用于IIS和Tomcat7或Tomcat7以上版本
def convert_pem_to_pfx(ssl_cert: str,
                       ssl_key: str,
                       ssl_ca_cert_chains: str,
                       ssl_key_password: str = None):

    loaded_ssl_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ssl_cert)
    loaded_ssl_key = crypto.load_privatekey(crypto.FILETYPE_PEM, ssl_key, passphrase=ssl_key_password)
    ca_certs = pem.parse(ssl_ca_cert_chains.encode())
    loaded_ca_certs = []
    for ca_cert in ca_certs:
        loaded_ca_certs.append(crypto.load_certificate(crypto.FILETYPE_PEM, ca_cert.as_bytes()))
    # loaded_ssl_ca_cert_chains = crypto.load_certificate(crypto.FILETYPE_PEM, ssl_ca_cert_chains)
    pkcs = crypto.PKCS12()
    pkcs.set_certificate(loaded_ssl_cert)
    pkcs.set_privatekey(loaded_ssl_key)
    pkcs.set_ca_certificates(loaded_ca_certs)
    return pkcs.export(ssl_key_password)


# 将SSL证书的CERT、KEY、CA打包为常用的Apache、IIS、Nginx、CDN等格式并创建压缩包返回文件资源
def create_certificates_zip_file(ssl_cert: str,
                                 ssl_key: str,
                                 ssl_ca_cert_chains: str,
                                 ssl_key_password: str = None) -> zipfile.ZipFile:
    # 创建临时的zip文件，用于存储zip文件内容
    temp_file_path = tempfile.TemporaryFile('w+b', suffix='.zip', prefix='tmp-cert-convert-')
    new_zip_file = zipfile.ZipFile(temp_file_path, 'a', zipfile.ZIP_DEFLATED)
    # Nginx
    new_zip_file.writestr('Nginx/server.crt', ssl_cert)
    new_zip_file.writestr('Nginx/server.key', ssl_key)
    # Apache
    new_zip_file.writestr('Apache/server.crt', ssl_cert)
    new_zip_file.writestr('Apache/ca.crt', ssl_ca_cert_chains)
    new_zip_file.writestr('Apache/server.key', ssl_key)
    # CDN
    new_zip_file.writestr('CDN/server.pem', ssl_cert + "\n" + ssl_ca_cert_chains)
    new_zip_file.writestr('CDN/ca.pem', ssl_ca_cert_chains)
    new_zip_file.writestr('CDN/private_key.pem', ssl_key)
    # IIS
    pkcs_content = convert_pem_to_pfx(ssl_cert,
                              ssl_key,
                              ssl_ca_cert_chains,
                              ssl_key_password)
    new_zip_file.writestr('IIS/server.pfx', pkcs_content)
    # 关闭ZIP文件
    # new_zip_file.printdir()
    new_zip_file.close()
    return new_zip_file


class X509Utils:
    # Sign Type Of Key
    SIGN_TYPE_RSA = crypto.TYPE_RSA
    SIGN_TYPE_ECC = crypto.TYPE_DSA

    # 根据提供的类型创建私钥
    def generate_key(self, key_type):
        key = crypto.PKey()
        key = crypto.PKey()
        if key_type == self.SIGN_TYPE_RSA:
            bits = 2048
        elif key_type == self.SIGN_TYPE_ECC:
            bits = 1024
        else:
            raise UtilsError("Unsupported Key_Sign_Type, only support RSA and ECC")
        key.generate_key(key_type, bits)
        # key_content = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
        return key

    # 根据提供的信息创建CSR代码和KEY进行返回
    def generate_csr(self,
                     key_type,
                     common_name='your-domain-name-here.com',
                     country_code='CN',
                     state_or_province_name='someState',
                     locality_name='someCity',
                     organization_name='someOrganization',
                     organizational_unit_name='someUnitName'
                     ):
        req = crypto.X509Req()
        # Return an X509Name object representing the subject of the certificate.
        req.get_subject().CN = common_name
        req.get_subject().countryName = country_code
        req.get_subject().stateOrProvinceName = state_or_province_name
        req.get_subject().localityName = locality_name
        req.get_subject().organizationName = organization_name
        req.get_subject().organizationalUnitName = organizational_unit_name
        # Set the public key of the certificate to pkey.
        key = self.generate_key(key_type)
        req.set_pubkey(key)
        # Sign the certificate, using the key pkey and the message digest algorithm identified by the string digest.
        req.sign(key, 'sha256')

        return {'csr_code': crypto.dump_certificate_request(crypto.FILETYPE_PEM, req).decode('utf-8'),
                'key_code': crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode('utf-8')
                }

