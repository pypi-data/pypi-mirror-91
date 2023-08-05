#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:
Email:

date:
desc:

"""
import re
import datetime

from rest_framework.exceptions import ValidationError


class PhoneValidator(object):
    """
    PhoneValidator
    """
    # message = _('Not a invalid phone')
    message = '请输入正确的手机号码'
    code = 'invalid'
    pattern = re.compile(r"^1[3-9]\d{9}$")

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        phone_str = str(value)
        num = self.pattern.match(phone_str)
        if not num:
            raise ValidationError(
                detail="{}:{}".format(self.message, phone_str)
            )


class IdCardValidator(object):
    """
    http://shenfenzheng.293.net/

    公民身份证号码按照 GB11643—1999《公民身份证号码》国家标准编制，
    由18位数字组成：
        前6位为行政区划分代码，
        第7位至14位为出生日期码，
        第15位至17位为顺序码，
        第18位为校验码。
    在上世纪（二十世纪）办的身份证为15位数字码。
    原来7、8位的年份号到2000年后攺为全称，如1985年过去7、8位码是85，现在增改为1985，
    而又在最后一位增加校验码，如后三位原来601，加一个5成为6015。
    身份证一经编定不作改变，派出所会在户口资料中给你加上，你要换新证时就是18位的新码了。

    # 身份证18位编码规则：dddddd yyyymmdd xxx y
    # dddddd：地区码
    # yyyymmdd: 出生年月日
    # xxx:顺序类编码，无法确定，奇数为男，偶数为女
    # y: 校验码，该位数值可通过前17位计算获得
    # <p />
    # 18位号码加权因子为(从右到左) Wi =
    # [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
    # 验证位 Y = [ 1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2 ]
    # 校验位计算公式：Y_P = mod( ∑(Ai×Wi),11 )
    # i为身份证号码从右往左数的 2...18 位; Y_P为脚丫校验码所在校验码数组位置
    """
    # message = _('Not a invalid id card')
    message = '请输入正确的身份证号'
    code = 'invalid'
    chmap = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
        '6': 6, '7': 7, '8': 8, '9': 9, 'x': 10, 'X': 10
    }

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def ch_to_num(self, ch):
        """

        :param ch:
        :return:
        """
        return self.chmap[ch]

    @staticmethod
    def verify_list(l):
        """

        :param l:
        :return:
        """
        ret = 0
        for ii, n in enumerate(l):
            i = 18-ii
            weight = 2**(i-1) % 11
            ret = (ret + n*weight) % 11
        return ret == 1

    def __call__(self, value):
        char_list = list(value)
        try:
            num_list = [self.ch_to_num(ch) for ch in char_list]
        except Exception as e:
            # raise ValidationError(
            #     detail='invalid id_card value:{}'.format(value))
            raise ValidationError(
                detail="{}:{} e:{}".format(self.message, value, e)
            )
        if not self.verify_list(num_list):
            raise ValidationError(detail=self.message)


class TimeStampValidator(object):
    """
    TimeStamp Validator
    """
    # message = _('Not a invalid phone')
    message = '请输入正确的时间戳'
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if not isinstance(value, datetime.datetime):
            raise ValidationError(
                detail="{}:{}".format(self.message, value)
            )


id_card_validator = IdCardValidator()
phone_validator = PhoneValidator()
timestamp_validator = TimeStampValidator()


def test_id_card():
    """

    :return:
    """
    # https://www.cnblogs.com/linus-tan/p/7111797.html
    code_list = [
        '610321199301140617',
        '230227198302151067',
        '120111199207178301',
        '45128119860426100X',
        '33010619930228635X',
        '540124197702281542'
    ]
    for code in code_list:
        id_card_validator(code)


def test_phone():
    """

    :return:
    """
    phone_list = [
        '13152051317',
        '14152051317',
        '19152051317',
        # '1315205131',
        # '131520513171',
    ]
    for phone in phone_list:
        phone_validator(phone)


def main():
    """

    :return:
    """
    test_id_card()
    test_phone()


if __name__ == '__main__':
    main()
