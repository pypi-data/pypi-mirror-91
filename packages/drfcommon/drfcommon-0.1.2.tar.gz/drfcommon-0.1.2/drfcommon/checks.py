#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
admin.py
"""
from collections import OrderedDict

from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def check_date(start_date=None, end_date=None):
    """
    validate()
    :param start_date:
    :param end_date:
    :return:
    """
    timedelta = end_date - start_date
    delay = timedelta.days
    if delay < 0:
        raise ValidationError(
            detail={
                'start_date/end_date': _('start_date must >= end_date')
            })


def check_filter_type(filter_type=None, choice_map=None):
    """
    :return:
    """
    if not isinstance(choice_map, dict):
        raise TypeError('choice_map is not dict')

    if filter_type not in choice_map:
        raise ValidationError(
            detail={
                'filter_type': _('filter_type err')
            }
        )


def _tree_queryset_values(qs, keys=None, order_by_keys=None):
    """
    id, level, parent_id must include in keys
    :param qs:
    :param keys:
    :param order_by_keys:
    :return:
    """
    if not hasattr(qs.model, '_mptt_meta'):
        raise TypeError('queryset must be MPTTModel queryset')

    if not keys:
        opts = qs.model._mptt_meta
        keys = (
            'id',
            opts.level_attr,
            '{}_id'.format(opts.parent_attr),
            opts.tree_id_attr,
            opts.left_attr,
            opts.right_attr,
        )

    if 'id' not in keys:
        raise ValueError('id must in keys')

    if 'level' not in keys:
        raise ValueError('level must in keys')

    if 'parent_id' not in keys:
        raise ValueError('parent_id must in keys')

    if not order_by_keys:
        # 默认，root->left
        order_by_keys = ['id', 'lft']

    if not qs.ordered:
        qs = qs.order_by(*order_by_keys)
    qs = qs.values(*keys)

    # 组织树数据格式LIFO
    data_map = OrderedDict()
    for cur_node in qs:
        cur_node_pk = cur_node.get('id')
        # 为当前节点分配子节点数组
        cur_node['child'] = list()
        data_map[cur_node_pk] = cur_node
        cur_node_parent_id = cur_node.get('parent_id')
        if cur_node_parent_id in data_map:
            # 当前节点是子节点，追加到父节点的child列表中
            data_map[cur_node_parent_id]['child'].append(cur_node)
            data_map[cur_node_pk]['is_root'] = False
        else:
            data_map[cur_node_pk]['is_root'] = True
    return data_map


def tree_queryset_values(qs, keys=None, order_by_keys=None):
    """
    从根节点开始数据

    level: 物理属性，标识根节点.
    is_root: 逻辑属性，当前的queryset 没有父亲节点，便当作逻辑根

    :param qs:
    :param keys:
    :param order_by_keys:  order_by('id', 'lft').
    :return: mptt queryset values
    """
    data_map = _tree_queryset_values(
        qs, keys=keys, order_by_keys=order_by_keys)
    ret_map = OrderedDict()
    for k, v in data_map.items():
        if v.get('is_root', False):
            ret_map[k] = v
    data = {
        'index': list(ret_map.keys()),
        'data': ret_map,
    }
    return data


def sub_tree_queryset_values(qs, keys=None, order_by_keys=None):
    """
    返回mptt queryset 子树数据, 从任何一棵树的任意节点，返回该节点的子树数据



    :param qs:
    :param keys:
    :param order_by_keys:  order_by('id', 'lft').
    :return:
    """
    data_map = _tree_queryset_values(
        qs, keys=keys, order_by_keys=order_by_keys)
    data = {
        'index': list(data_map.keys()),
        'data': data_map.popitem(last=False),
    }
    return data
