#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
"""
from django.contrib.contenttypes.models import ContentType
from django.db import models


def get_pk_and_ct_by_instance(instance=None):
    """
    get_for_model will get opts.app_label, opts.model_name
    :param instance:
    :return:
    """
    if not isinstance(instance, models.Model):
        raise TypeError('instance must be models.Model instance')
    object_pk = instance.pk
    content_type = ContentType.objects.get_for_model(model=instance)
    return object_pk, content_type
