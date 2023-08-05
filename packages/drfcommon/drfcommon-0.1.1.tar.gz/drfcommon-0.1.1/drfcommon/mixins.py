#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mixins.py
"""
import logging
import random
from collections import OrderedDict

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import (
    DestroyModelMixin, CreateModelMixin,
    ListModelMixin, RetrieveModelMixin,
)

from drfcommon.response import make_response, fmt_make_response

logger = logging.getLogger('debug')


class CanDeletedMixin:
    """
    CanDeleted Mixin
    """
    def update_can_deleted_true(self, request, queryset):
        """

        :param request:
        :param queryset:
        :return:
        """
        queryset.update(can_deleted=True)

    def update_can_deleted_false(self, request, queryset):
        """

        :param request:
        :param queryset:
        :return:
        """
        queryset.update(can_deleted=False)

    update_can_deleted_true.short_description = \
        "Selected set can_deleted true"
    update_can_deleted_false.short_description = \
        "Selected set can_deleted false"


class BulkDeleteModelMixin:
    """
    Bulk deleted  a model instance.
    """

    def get_bulk_delete_queryset(self, validated_data=None):
        """

        :param validated_data:
        :return:
        """
        raise NotImplementedError(
            '`get_bulk_delete_queryset()` must be implemented.')

    def bulk_delete(self, request, *args, **kwargs):
        """
        批量删除

        ----

        """
        logger.info("__class__:{} bulk_delete request.data:{}".format(
            self.__class__, request.data))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        id_list = validated_data.get('id_list')
        queryset = self.get_bulk_delete_queryset(validated_data=validated_data)
        if queryset:
            delete_line = queryset.filter(id__in=id_list) \
                .filter(is_deleted=False) \
                .update(is_deleted=True)
        else:
            delete_line = 0
        data = {
            'delete_line': delete_line,
            'id_list': id_list,
        }
        logger.info('bulk_delete data:{}'.format(data))
        return Response(make_response(data=data))


class RandomMixin:
    """
    Random Mixin
    """
    page_size = 15

    @classmethod
    def filter_selected_pks(cls, queryset=None, selected_pks=None):
        """

        :param queryset:
        :param selected_pks:
        :return:
        """
        queryset = queryset.filter(pk__in=selected_pks)
        return queryset

    @classmethod
    def random_pk_list(cls, queryset=None, page_size=15):
        """

        :param queryset:
        :param page_size:
        :return:
        """
        if not isinstance(queryset, QuerySet):
            raise TypeError('queryset must be QuerySet instance')
        pk_list = queryset.values_list('pk', flat=True)
        logger.debug(f'page_size:{page_size} pk_list:{len(pk_list)}')
        if len(pk_list) < page_size:
            selected_len = len(pk_list)
        else:
            selected_len = page_size
        selected_pks = random.sample(list(pk_list), selected_len)
        logger.info(f'selected_pks:{selected_pks}')
        return selected_pks

    @classmethod
    def random_queryset(cls, queryset=None, page_size=15):
        """

        :param queryset:
        :param page_size:
        :return:
        """
        selected_pks = cls.random_pk_list(queryset, page_size=page_size)
        queryset = cls.filter_selected_pks(queryset, selected_pks=selected_pks)
        return selected_pks, queryset

    @classmethod
    def random_queryset_data(cls, sort_keys=None, serializer_data=None):
        """

        :param sort_keys:
        :param serializer_data:
        :return:
        """
        return_dict = OrderedDict().fromkeys(sort_keys)
        for item in serializer_data:
            return_dict[item.get('id')] = item
        return sort_keys, list(return_dict.values())

    def get_random_queryset(self, validated_data=None):
        """

        :param validated_data:
        :return:
        """
        raise NotImplementedError(
            '`get_random_queryset()` must be implemented.')

    def list_random(self, request, *args, **kwargs):
        """
        随机列表

        ----

        """
        logger.info("__class__:{} list_random request.data:{}".format(
            self.__class__, request.data))
        queryset = self.get_random_queryset()
        selected_pks, random_queryset = self.random_queryset(
            queryset=queryset, page_size=self.random_activity_size,
        )
        serializer = self.get_serializer(random_queryset, many=True)
        _, data = self.random_queryset_data(
            sort_keys=selected_pks,
            serializer_data=serializer.data,
        )
        logger.info('random_queryset_data data len:{}'.format(len(data)))
        return Response(make_response(data=data))


class GpsMixin:
    """
    Gps Mixin
    """
    def get_gps(self):
        """

        :return:
        """
        if hasattr(self, 'gps'):
            return self.gps.tuple
        return []


class SafeDestroyModelMixin(DestroyModelMixin):
    """
    Safe Destroy a model instance.
    """
    def perform_destroy(self, instance):
        if hasattr(instance, 'is_deleted'):
            instance.update(is_deleted=True)
        else:
            super().perform_destroy(instance)


class ListWithTopModelMixin:
    """
    根据置顶排序: (is_top, last_top_time) 排序
    """
    def list_top(self, request, *args, **kwargs):
        """
        根据置顶排序返回列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.order_by('-is_top', '-last_top_time')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FmtCreateModelMixin(CreateModelMixin):
    """
    Create a model instance with fmt response.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        fmt_response = fmt_make_response(serializer.data)
        return Response(
            fmt_response,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class FmtListModelMixin(ListModelMixin):
    """
     List a queryset with fmt response.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        fmt_response = fmt_make_response(serializer.data)
        return Response(fmt_response)


class FmtRetrieveModelMixin(RetrieveModelMixin):
    """
    Retrieve a model instance with fmt response.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        fmt_response = fmt_make_response(serializer.data)
        return Response(fmt_response)
