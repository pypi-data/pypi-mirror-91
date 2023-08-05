#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
serializers.py
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from drfcommon.checks import check_date, check_filter_type
from drfcommon.choices import DateRangeChoice
from drfcommon.fields import PhoneField


class BaseSerializer(serializers.Serializer):
    """
    Base Serializer
    """
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class TreeSerializer(BaseSerializer):
    """
    Tree Serializer
    """
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')
    pid = serializers.PrimaryKeyRelatedField(read_only=True)


class BaseDateSearchSerializer(BaseSerializer):
    """
    BaseDateSearch Serializer
    """
    start_date = serializers.DateField(
        required=True, help_text='开始日期:2019-10-1')
    end_date = serializers.DateField(
        required=True, help_text='结束日期:2019-10-1')

    def validate(self, attrs):
        return attrs


class DateSearchSerializer(BaseDateSearchSerializer):
    """
    DateSearch Serializer
    """
    filter_type = serializers.ChoiceField(
        required=True, help_text=u'最小粒度:0', choices=DateRangeChoice.CHOICES)

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        check_date(start_date, end_date)
        filter_type = attrs['filter_type']
        check_filter_type(
            filter_type=filter_type, choice_map=DateRangeChoice.CHOICES_MAP)
        return attrs


class WXApiSerializer(BaseDateSearchSerializer):
    """
    WXApi Serializer
    """
    url = serializers.URLField(
        required=True, max_length=1024, help_text='微信数据分析api')

    @staticmethod
    def validate_url(url):
        """

        :param url:
        :return:
        """
        url_prefix = "https://api.weixin.qq.com/datacube/"
        if not str(url).startswith(url_prefix):
            raise ValidationError(
                detail=_('url prefix err')
            )
        return url

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        check_date(start_date, end_date)
        attrs['start_date'] = start_date.strftime('%Y%m%d')
        attrs['end_date'] = end_date.strftime('%Y%m%d')
        return attrs


class GpsCreateSerializer(BaseSerializer):
    """
    GpsCreate Serializer
    """
    x = serializers.FloatField(
        required=True,
        write_only=True,
        help_text='x: gps.point(x,y) srid=4326')
    y = serializers.FloatField(
        required=True,
        help_text='y: gps:point(x,y) srid=4326')


class BulkBaseSerializer(BaseSerializer):
    """
    批量操作
    BulkBase Serializer
    """
    id_list = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        help_text='批量执行:pk list',
    )

    def validate(self, attrs):
        id_list = attrs.get('id_list')
        if len(id_list) <= 0:
            raise ValidationError(
                detail={
                    'id_list': _('id list is None'),
                }
            )
        return attrs


class PhoneSerializer(BaseSerializer):
    """
    手机号序列化
    """
    phone = PhoneField(
        required=True, max_length=11, min_length=11, label='手机号')


class PageSerializer(BaseSerializer):
    """
    Page Serializer
    """
    page = serializers.IntegerField(
        min_value=1, default=1, help_text='第几页')
    page_size = serializers.IntegerField(
        min_value=1, default=10, help_text="每页数量")


def get_page_param(request=None):
    page = PageSerializer(data=request.query_params)
    page.is_valid(raise_exception=True)
    page_number = page.validated_data.get('page')
    page_size = page.validated_data.get('page_size')
    return page_number, page_size
