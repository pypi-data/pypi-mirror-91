#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsSuperUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSelfOrIsSuperUser(BasePermission):
    """
    自定义权限只允许User对象的所有者和超级用户进行编辑。
    """
    def has_object_permission(self, request, view, obj):
        # isAdmin
        if request.user and request.user.is_superuser:
            return True
        if not hasattr(obj, 'user'):
            return False
        return getattr(obj, 'user') == request.user


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    1.is_super
    2.staff
    """

    def has_permission(self, request, view):
        if not request.user:
            return False
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        return False


def is_admin_user(user=None):
    if not user:
        return False

    if user.is_superuser or user.is_staff:
        return True
    return False


def main():
    pass


if __name__ == '__main__':
    main()
