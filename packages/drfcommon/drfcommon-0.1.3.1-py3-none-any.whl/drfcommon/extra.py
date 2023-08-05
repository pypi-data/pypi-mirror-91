#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
from io import BytesIO

from django.core.files.uploadhandler import TemporaryUploadedFile
from PIL import Image


def get_img_extra(content=None, content_type='image/png'):
    if not content:
        return dict(content=None)
    if not isinstance(content, TemporaryUploadedFile):
        return dict(err='content is not TemporaryUploadedFile')
    im = Image.open(content.file.name)
    width, height = im.size
    format_ = im.format
    buffered = BytesIO()
    im.save(buffered, format=format_)
    # # base64
    image_base64 = base64.b64encode(buffered.getvalue())
    image_base64_str = image_base64.decode('utf-8')
    # # data:image/png;base64,image_data
    # image_code_data = "data:{};base64,{}".format(
    #     content_type, image_base64_str)
    # attrs['file_data'] = image_code_data
    extra = {
        'width': width,
        'height': height,
        'format': format_,
        'data': image_base64_str,
    }
    return extra


def main():
    pass


if __name__ == '__main__':
    main()
