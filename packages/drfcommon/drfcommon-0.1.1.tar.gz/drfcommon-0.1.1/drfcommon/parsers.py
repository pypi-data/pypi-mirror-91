#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
parsers.py
"""

from rest_framework_xml.parsers import XMLParser


class WeChatPaymentXMLParser(XMLParser):
    """
    WeChatPayment XMLParser
    """
    media_type = 'text/xml'
