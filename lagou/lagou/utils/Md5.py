# -*- coding: utf-8 -*-
"""
Md5加密
Author: Marico
Version: 1.0.1
Date: 2017-11-14
Language: Python 2.7.13
"""
import hashlib

def encrypt(str):
    '''
    MD5加密
    '''
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()
