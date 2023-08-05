#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pagination.py
"""

from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """
    Standard Pagination
    """
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 150

    @staticmethod
    def fix_link(link=''):
        """

        :param link:
        :return:
        """
        # 线上使用
        if not link:
            return link
        if not link.startswith('https'):
            link = link.replace('http', 'https')
        return link

    def get_paginated_response(self, data):
        errcode = 0
        errmsg = ''
        # 通常data => query_set
        if isinstance(data, dict):
            if data.get('errcode'):
                errcode = data.get('errcode')
            if data.get('errmsg'):
                errmsg = data.get('errmsg')
        next_link = self.get_next_link()
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            # ('_next', next_link),
            ('next', self.fix_link(link=next_link)),
            ('previous', self.get_previous_link()),
            ('data', data),
            ('errcode', errcode),
            ('errmsg', errmsg),
        ]))
