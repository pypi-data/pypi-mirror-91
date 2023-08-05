#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
admin.py
"""
from django.contrib.gis.admin import OSMGeoAdmin


class MyOSMGeoAdmin(OSMGeoAdmin):
    """
    3. 对于 Web Map 开发人员的意义
       对于 Web Map 开发人员来说，最熟悉的应该是
            EPSG:4326 (WGS84) and EPSG:3857(Pseudo-Mercator)

    3.1 EPSG:4326 (WGS84)
        前面说了WGS84是目前最流行的地理坐标系统。
        在国际上，每个坐标系统都会被分配一个 EPSG 代码，EPSG:4326就是WGS84 的代码。
        GPS是基于WGS84的，所以通常我们得到的坐标数据都是WGS84的.
        一般我们在存储数据时，仍然按WGS84存储。

    3.2 EPSG:3857 (Pseudo-Mercator)伪墨卡托投影，也被称为球体墨卡托，Web Mercator。
        它是基于墨卡托投影的，把 WGS84坐标系投影到正方形。
        我们前面已经知道 WGS84 是基于椭球体的，但是伪墨卡托投影把坐标投影到球体上，
        这导致两极的失真变大，但是却更容易计算。这也许是为什么被称为”伪“墨卡托吧。
        另外，伪墨卡托投影还切掉了南北85.051129°纬度以上的地区，
        以保证整个投影是正方形的。因为墨卡托投影等正形性的特点，
        在不同层级的图层上物体的形状保持不变，
        一个正方形可以不断被划分为更多更小的正方形以显示更清晰的细节。
        很明显，伪墨卡托坐标系是非常显示数据，但是不适合存储数据的，
        通常我们使用WGS84 存储数据，使用伪墨卡托显示数据。

    """
    default_lon = 12130375.659464
    default_lat = 4057679.0826772
    default_zoom = 13
