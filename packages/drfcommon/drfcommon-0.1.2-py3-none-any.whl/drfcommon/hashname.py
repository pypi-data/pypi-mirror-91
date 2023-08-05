#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
oss hash name.py
"""
import hashlib
import time

prefix = 'app'


def get_help_text(label, choices):
    """

    :param label:
    :param choices:
    :return:
    """
    return '%s, %s' % (label, ';'.join(['%s:%s' % (k, v) for k, v in choices]))


def gen_file_name(filename):
    """

    :param filename:
    :return:
    """
    ext = filename.split('.')[-1]
    return "%s.%s" % (
        hashlib.sha1(str(time.time()).encode('utf8')).hexdigest(), ext)


def content_images(instance, filename):
    """

    :param instance:
    :param filename:
    :return:
    """
    return '{}_content/images/{}'.format(prefix, gen_file_name(filename))


def content_id_card(instance, filename):
    """

    :param instance:
    :param filename:
    :return:
    """
    return '{}_content/id_card/{}'.format(prefix, gen_file_name(filename))


def content_id_photo(instance, filename):
    """

    :param instance:
    :param filename:
    :return:
    """
    return '{}_content/id_photo/{}'.format(prefix, gen_file_name(filename))


# 在upload-file接口中使用
def content_files(filename=''):
    """

    :param filename:
    :return:
    """
    return '{}_content/files/{}'.format(prefix, gen_file_name(filename))


def content_gps_json(filename=''):
    """

    :param filename:
    :return:
    """
    return '{}_content/gps_json/{}'.format(prefix, filename)


def content_device_files(year=None, month=None, day=None, filename=''):
    """

    :param year:
    :param month:
    :param day:
    :param filename:
    :return:
    """
    return '{}_content/device_files/{}/{}/{}/{}'.format(
        prefix, year, month, day, gen_file_name(filename))


def content_faces(face_id=None):
    """

    :param face_id:
    :return:
    """
    filename = '{}_template.txt'.format(face_id)
    return '{}_content/faces/{}/{}'.format(
        prefix, face_id, gen_file_name(filename))


def content_img(filename=''):
    """

    :param filename:
    :return:
    """
    return '{}_content/img/{}'.format(prefix, gen_file_name(filename))


def content_log(filename=''):
    """

    :param filename:
    :return:
    """
    return '{}_content/logs/{}'.format(prefix, gen_file_name(filename))


def content_apk(filename=''):
    """

    :param filename:
    :return:
    """
    return '{}_content/apk/{}'.format(prefix, gen_file_name(filename))


def content_mp4(filename):
    """

    :param filename:
    :return:
    """
    return '{}_content/mp4/{}'.format(prefix, gen_file_name(filename))
