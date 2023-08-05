#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
"""

import datetime
from calendar import timegm

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from jwt import ExpiredSignature, DecodeError
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.settings import api_settings


User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


def new_jwt_token(data=None):
    """

    :param data:
    :return:
    """
    payload = jwt_payload_handler(data)
    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.datetime.utcnow().utctimetuple()
        )
    token = jwt_encode_handler(payload)
    return token


def _check_payload(token):
    # Check payload valid (based off of JSONWebTokenAuthentication,
    # may want to refactor)
    try:
        payload = jwt_decode_handler(token)
    except ExpiredSignature:
        msg = _('Signature has expired.')
        raise ValidationError(msg)
    except DecodeError:
        msg = _('Error decoding signature.')
        raise ValidationError(msg)

    return payload


def _check_user(payload):
    username = jwt_get_username_from_payload(payload)

    if not username:
        msg = _('Invalid payload.')
        raise ValidationError(msg)

    # Make sure user exists
    try:
        user = User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        msg = _("User doesn't exist.")
        raise ValidationError(msg)

    if not user.is_active:
        msg = _('User account is disabled.')
        raise ValidationError(msg)
    return user


def decode_jwt_token(token=None):
    """
    解码jwt token
    :param token:
    :return:
    """
    payload = _check_payload(token)
    return _check_user(payload=payload)
