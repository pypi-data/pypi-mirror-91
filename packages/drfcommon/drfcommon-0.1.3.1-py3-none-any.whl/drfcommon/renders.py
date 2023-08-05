#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
renders.py
"""

from django.utils import six
from django.utils.encoding import force_text
from django.utils.six import StringIO
from django.utils.xmlutils import SimplerXMLGenerator
from rest_framework_xml.renderers import XMLRenderer


class WeChatPayXMLRender(XMLRenderer):
    """
    https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=9_7
    <xml>
        <return_code><![CDATA[SUCCESS]]></return_code>
        <return_msg><![CDATA[OK]]></return_msg>
    </xml>
    """
    root_tag_name = 'xml'
    return_code_tag_name = 'return_code'
    return_msg_tag_name = 'return_msg'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """

        :param data:
        :param accepted_media_type:
        :param renderer_context:
        :return:
        """
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        # xml.startDocument()
        xml.startElement(self.root_tag_name, {})

        self._to_xml(xml, data)

        xml.endElement(self.root_tag_name)
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, xml, data):
        """

        :param xml:
        :param data:
        :return:
        """
        if isinstance(data, dict):
            for key, value in six.iteritems(data):
                xml.startElement(key, {})
                # value 也当成标签写入
                xml.startElement(value, {})
                # self._to_xml(xml, value)
                xml.endElement(key)

        elif data is None:
            # Don't output any value
            pass
        else:
            xml.characters(force_text(data))
