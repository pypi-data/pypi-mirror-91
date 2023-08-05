#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DateRangeChoice(object):
    """
    时间范围
    """
    HOUR = 0
    DAY = 1
    MON = 2
    YEAR = 3
    CHOICES = (
        (HOUR, '小时'),
        (DAY, '天'),
        (MON, '月'),
        (YEAR, '年'),
    )
    # 数据库使用
    CHOICES_MAP_STR = {
        HOUR: 'hour',
        DAY: 'day',
        MON: 'month',
        YEAR: 'year',
    }
    CHOICES_VALUE = [item[0] for item in CHOICES]
    CHOICES_MAP = {k: v for k, v in CHOICES}


class AppTypeChoice(object):
    """
    状态类型: 1成功，0失败
    """
    DEFAULT = 0
    IOS = 1
    ANDROID = 2

    CHOICES = (
        (DEFAULT, '默认'),
        (IOS, '苹果'),
        (ANDROID, '安卓'),
    )
    CHOICES_VALUE = [item[0] for item in CHOICES]
    CHOICES_MAP = {k: v for k, v in CHOICES}


class AuthorizationStatus(object):
    CREATE = 0
    PASS = 1
    FAIL = 2

    CHOICES = (
        (CREATE, '审核中'),
        (PASS, '审核通过'),
        (FAIL, '审核失败'),
    )
    CHOICES_MAP = {k: v for k, v in CHOICES}


class ActionTypeStatus(object):
    ADD = 0
    REMOVE = 1
    CHOICES = (
        (ADD, '添加'),
        (REMOVE, '删除'),
    )
    CHOICES_MAP = {k: v for k, v in CHOICES}


class UseStatusChoice(object):
    """
    核销状态:
        有效: 未过期
        无效: 过期, 未到指定日期
    """
    INVALID = 0
    VALID = 1
    CHOICES = ((INVALID, '无效'), (VALID, '有效'),)
    CHOICES_VALUE = (INVALID, VALID)
    CHOICES_MAP = {k: v for k, v in CHOICES}

