#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
response.py
"""
from rest_framework import status
from rest_framework.response import Response


def make_response(data=None, errcode=0, errmsg='', **kwargs):
    """

    :param data:
    :param errcode:
    :param errmsg:
    :return:
    """
    resp = dict(data=data, errcode=errcode, errmsg=errmsg, **kwargs)
    if isinstance(data, dict):
        if 'errcode' in data:
            resp['errcode'] = data['errcode']

        if 'errmsg' in data:
            resp['errmsg'] = data['errmsg']
    return resp


def fmt_make_response(data=None, errcode=0, errmsg='', **kwargs):
    """
    直接返回统一的响应格式.

    :param data:
    :param errcode:
    :param errmsg:
    :return:
    """
    resp = dict(data=data, errcode=errcode, errmsg=errmsg, **kwargs)
    if isinstance(data, dict):
        if 'errcode' in data:
            resp['errcode'] = data['errcode']

        if 'errmsg' in data:
            resp['errmsg'] = data['errmsg']
    return Response(data, status=status.HTTP_200_OK)

