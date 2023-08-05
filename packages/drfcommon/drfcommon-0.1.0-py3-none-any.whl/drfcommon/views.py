#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
views.py
"""
import logging
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from drfcommon.permisssions import IsAdminUser
from drfcommon.serializers import TreeSerializer


logger = logging.getLogger(__name__)


class AllowAnyView(generics.GenericAPIView):
    """
    AllowAny View
    """
    http_method_names = ['get', 'post', 'options']
    queryset = None
    permission_classes = ()
    authentication_classes = ()

    def get_queryset(self):
        return self.queryset


class AdminView(AllowAnyView):
    """
    Admin View
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [
        JSONWebTokenAuthentication, SessionAuthentication]


class IsAuthenticatedView(AllowAnyView):
    """
    IsAuthenticated View
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        JSONWebTokenAuthentication, SessionAuthentication]


class AllowAnyViewSet(GenericViewSet):
    """
    AllowAnyView Set
    """
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options', ]
    queryset = None
    serializer_class = None
    permission_classes = ()
    authentication_classes = ()
    serializer_map = None

    def get_serializer_class(self):
        if not isinstance(self.serializer_map, dict):
            return self.serializer_class
        if self.action not in self.serializer_map:
            logger.warning(f'action:{self.action} not conf serializer')
        return self.serializer_map.get(self.action, self.serializer_class)


class AllowAnyReadViewSet(AllowAnyViewSet):
    """
    AllowAnyView Set
    """

    def initialize_request(self, request, *args, **kwargs):
        """
        Set the `.action` attribute on the view, depending on the request method.
        """
        request = super().initialize_request(request, *args, **kwargs)
        if self.action in ('list', 'retrieve'):
            self.authentication_classes = ()
        return request

    def get_permissions(self):
        """
        list/retrieve no permissions
        :return:
        """
        if self.action in ('list', 'retrieve', 'list_top'):
            self.permission_classes = []
        # 默认权限
        return [permission() for permission in self.permission_classes]


class IsAuthenticatedViewSet(AllowAnyViewSet):
    """
    IsAuthenticatedView Set
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        JSONWebTokenAuthentication, SessionAuthentication]


class AdminViewSet(AllowAnyViewSet):
    """
    AdminView Set
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [
        JSONWebTokenAuthentication, SessionAuthentication]


class TreeAPIView(ListAPIView):
    """
    TreeAPI View
    """
    serializer_class = TreeSerializer
    authentication_classes = ()
    permission_classes = ()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        tree_dict = {}
        tree_data = []
        try:
            for item in serializer.data:
                tree_dict[item['id']] = item
            for i in tree_dict:
                if tree_dict[i]['pid']:
                    pid = tree_dict[i]['pid']
                    parent = tree_dict[pid]
                    parent.setdefault('children', []).append(tree_dict[i])
                else:
                    tree_data.append(tree_dict[i])
            results = tree_data
        except KeyError:
            results = serializer.data
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)
