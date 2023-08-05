#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
exceptions.py
"""

import logging

from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    ValidationError
)
from rest_framework.views import exception_handler


logger = logging.getLogger('debug')


class MyValidationError(ValidationError):
    """
    MyValidation Error
    """
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        logger.error('ValidationError detail:{} code:{}'.format(detail, code))
        if code:
            self.status_code = code
        super(MyValidationError, self).__init__(detail=detail, code=code)


class MyAPIException(APIException):
    """
    detail 只返回string
    """
    status_code = status.HTTP_200_OK
    default_detail = _('A server error occurred.')
    default_code = 'error'
    err_code = status.HTTP_200_OK

    def __init__(self, detail=None, err_code=None):
        logger.error('APIException detail:{} code:{}'.format(detail, err_code))
        # if 100 <= code <= 599:
        #     self.status_code = code
        # else:
        #     err_code = code
        if err_code:
            self.err_code = err_code
        super(MyAPIException, self).__init__(
            detail=detail, code=self.status_code)


def custom_view_exception_handler(exc, context):
    """
    处理views中的异常, 视图函数只返回200，errmsg/errcode

    exc.detail
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

    :param exc: APIException
    :param context:
    :return:
    """
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if not response:
        return response
    # 保存错误码.
    if hasattr(exc, 'err_code'):
        response.data['errcode'] = exc.err_code
        response.status_code = status.HTTP_200_OK
    if 'detail' in response.data:
        detail = response.data.pop('detail')
        if detail:
            response.data['errmsg'] = detail
    return response
