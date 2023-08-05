#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fields.py
"""
from datetime import datetime
from rest_framework.fields import (
    CharField, IntegerField,
)

from drfcommon.time_tools import (
    utc_to_timestamp_ms, timestamp_to_utc
)
from drfcommon.validators import (
    id_card_validator, phone_validator,
    timestamp_validator,
)


class PhoneField(CharField):
    """
    Phone Field
    """
    default_error_messages = {
        # 'invalid': _('Enter a valid phone number.')
        'invalid': '请输入正确的手机号',
        'required': '手机号必须要填',
    }

    def __init__(self, **kwargs):
        self.max_value = kwargs.pop('max_value', None)
        self.min_value = kwargs.pop('min_value', None)
        super().__init__(**kwargs)
        self.validators = [phone_validator]


class IdCardField(CharField):
    """
    IdCard Field
    """
    default_error_messages = {
        # 'invalid': _('Enter a valid id card.')
        'invalid': '请输入正确的身份证号',
        'required': '身份证号必须要填',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # validator = IdCardValidator(message=self.error_messages['invalid'])
        # self.validators.append(validator)
        self.validators = [id_card_validator]


class TimeStampField(IntegerField):
    """
    TimeStamp Field
    """
    default_error_messages = {
        'invalid': '请输入正确的时间戳',
        'required': '时间戳必须要填',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(timestamp_validator)

    def to_internal_value(self, data):
        """
        int -> utc time
        :param data:
        :return:
        """
        data = super().to_internal_value(data)
        if len(str(data)) == 13:
            data = int(data/1000)
        data_time = timestamp_to_utc(data)
        return data_time

    def to_representation(self, value):
        """
        程序中的时间是utc时间，utc to timestamp
        value -> utc time
        :param value:
        :return:
        """
        if isinstance(value, datetime):
            value = utc_to_timestamp_ms(value)
        return value

