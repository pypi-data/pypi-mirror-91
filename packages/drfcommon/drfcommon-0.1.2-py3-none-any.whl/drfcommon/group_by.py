#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
desc:
    queryset group by year/month/day/hour
    group by 年/月/日/小时
"""
import logging
from collections import OrderedDict
from django.db.models import Count
from django.db.models.functions import (
    TruncHour, TruncMonth, TruncDay,
    TruncYear
)

logger = logging.getLogger('debug')


def group_by_month_mul_filed(
        queryset=None, time_filed='create_time', annotate_map=None):
    """
    获取queryset 按月分组后的数据. 多个聚合字段

    :param queryset: 时间范围过滤后的queryset
    :param time_filed: DatetimeFiled
    :param annotate_map: 聚合别名
    >>> annotate_map = dict(
        session_cnt=Sum('session_cnt'),
        visit_pv=Sum('visit_pv'),
        visit_uv_new=Sum('visit_uv_new'),
        stay_time_uv=Sum('stay_time_uv'),
        stay_time_session=Sum('stay_time_session'),
        visit_depth=Sum('visit_depth')
    )
    >>> values = ['month']
    >>> values.extend(annotate_map.keys())
    >>> values
        ['month', 'visit_depth', 'stay_time_uv', 'stay_time_session',
        'visit_pv', 'visit_uv_new', 'session_cnt']
    >>>
    :return: queryset
    """
    # 最终求值的字段
    values = ['month']
    values.extend(annotate_map.keys())

    data_list = queryset.annotate(month=TruncMonth(time_filed)) \
        .values('month') \
        .annotate(**annotate_map) \
        .values(*values).order_by('month')
    return data_list


def group_by_year(queryset=None, time_filed='create_time',
                  count_key='count', count_val=None):
    """
    获取queryset 按月分组后的数据
    :param queryset: 时间范围过滤后的queryset
    :param time_filed: DatetimeFiled
    :param count_key: 聚合别名, eg：count
    :param count_val: 聚合方法: Count('id')
    :return: queryset
    """
    if not count_val:
        count_val = Count('id')
    annotate_map = {
        count_key: count_val
    }
    data_list = queryset.annotate(year=TruncYear(time_filed)) \
        .values('year') \
        .annotate(**annotate_map) \
        .values('year', count_key).order_by('year')
    return data_list


def group_by_month(queryset=None, time_filed='create_time',
                   count_key='count', count_val=None):
    """
    获取queryset 按月分组后的数据
    :param queryset: 时间范围过滤后的queryset
    :param time_filed: DatetimeFiled
    :param count_key: 聚合别名, eg：count
    :param count_val: 聚合方法: Count('id')
    :return: queryset
    """
    if not count_val:
        count_val = Count('id')
    annotate_map = {
        count_key: count_val
    }
    data_list = queryset.annotate(month=TruncMonth(time_filed)) \
        .values('month') \
        .annotate(**annotate_map) \
        .values('month', count_key).order_by('month')
    return data_list


def group_by_day(queryset=None, time_filed='create_time',
                 count_key='count', count_val=None):
    """
    获取queryset 按月分组后的数据

    按天分组，取天和统计数量，按天排序
    :param queryset: 时间范围过滤后的queryset
    :param time_filed: DatetimeFiled
    :param count_key: 聚合别名, eg：count
    :param count_val: 聚合方法: Count('id')
    :return: queryset
    """
    if not count_val:
        count_val = Count('id')
    annotate_map = {
        count_key: count_val
    }
    data_list = queryset.annotate(day=TruncDay(time_filed)) \
        .values('day') \
        .annotate(**annotate_map) \
        .values('day', count_key).order_by('day')
    return data_list


def group_by_hour(queryset=None, time_filed='create_time',
                  count_key='count', count_val=None):
    """
    获取queryset 按月分组后的数据
    :param queryset: 时间范围过滤后的queryset
    :param time_filed: DatetimeFiled
    :param count_key: 聚合别名, eg：count
    :param count_val: 聚合方法: Count('id')
    :return: queryset
    """
    if not count_val:
        count_val = Count('id')
    annotate_map = {
        count_key: count_val
    }
    data_list = queryset.annotate(hour=TruncHour(time_filed)) \
        .values('hour') \
        .annotate(**annotate_map) \
        .values('hour', count_key).order_by('hour')
    return data_list


def to_map_by_group_by_data(data_list=None, count_key='count',
                            datetime_key='month', datetime_fmt='%Y-%m'):
    """

    :param data_list: group_by_month返回的数据, 元素必须是字典
    :param count_key: 分组中Count聚合函数对应的名字
    :param datetime_key: group by name
    :param datetime_fmt: 格式化日期
    :return: 日期为key, 数量为v的map
    """
    data_map = OrderedDict()
    for item_map in list(data_list):
        if not isinstance(item_map, dict):
            raise TypeError('item_map({}) is not dict'.format(type(item_map)))
        count = item_map.get(count_key)
        datetime_value = item_map.get(datetime_key)
        datetime_str = datetime_value.strftime(datetime_fmt)
        data_map[datetime_str] = count
    return data_map


def to_map_by_group_by_data_mul_filed(
        data_list=None, datetime_key='month', datetime_fmt='%Y-%m'):
    """

    :param data_list: group_by_month返回的数据
    :param datetime_key: group by name
    :param datetime_fmt: 格式化日期
    :return: 日期为key, 数量为v的map
    """
    data_map = OrderedDict()
    for item_map in list(data_list):
        if not isinstance(item_map, dict):
            raise TypeError('item_map({}) is not dict'.format(type(item_map)))
        datetime_value = item_map.pop(datetime_key)
        datetime_str = datetime_value.strftime(datetime_fmt)
        data_map[datetime_str] = item_map
    return data_map


GROUP_BY_FUNC_MAP = {
        'hour': (group_by_hour, 'hour', '%Y-%m-%d %H:%M:%S'),
        'day': (group_by_day, 'day', '%Y-%m-%d'),
        'month': (group_by_month, 'month', '%Y-%m'),
        'year': (group_by_year, 'year', '%Y'),
}

GROUP_BY_FUNC_MAP_MUL_FILED = {
    # 当前visit_trend最小粒度就是天，不需要分组，天的数据直接取
    'month': (group_by_month_mul_filed, 'month', '%Y-%m'),
}


def _get_group_by_data(filter_type='', queryset=None, time_filed='create_time',
                       count_key='count', count_val=None):
    """
    标准类型统计

    :param filter_type:
    :param queryset:
    :param time_filed:
    :param count_key:
    :param count_val:
    :return:
    """
    if not filter_type:
        return None
    if filter_type not in GROUP_BY_FUNC_MAP:
        raise KeyError('filter_type:{} must in {}'.format(
            filter_type, GROUP_BY_FUNC_MAP.keys()))
    group_by_func, datetime_key, datetime_fmt = GROUP_BY_FUNC_MAP[filter_type]
    data_list = group_by_func(
        queryset=queryset, time_filed=time_filed,
        count_key=count_key, count_val=count_val)
    return to_map_by_group_by_data(
        data_list, count_key=count_key,
        datetime_key=datetime_key,
        datetime_fmt=datetime_fmt)


def _get_group_by_data_mul_filed(
        filter_type='month', queryset=None, time_filed='create_time',
        annotate_map=None):
    """
    标准类型统计

    :param filter_type:
    :param queryset:
    :param time_filed:
    :param annotate_map:
    :return:
    """
    if not filter_type:
        return None
    if filter_type not in GROUP_BY_FUNC_MAP_MUL_FILED:
        raise KeyError('filter_type:{} must in {}'.format(
            filter_type, GROUP_BY_FUNC_MAP_MUL_FILED.keys()))
    group_by_func, datetime_key, datetime_fmt = \
        GROUP_BY_FUNC_MAP_MUL_FILED[filter_type]
    data_list = group_by_func(
        queryset=queryset, time_filed=time_filed,
        annotate_map=annotate_map,
        )
    return to_map_by_group_by_data_mul_filed(
        data_list,
        datetime_key=datetime_key,
        datetime_fmt=datetime_fmt
    )
