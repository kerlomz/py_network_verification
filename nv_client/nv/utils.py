#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import os
import win32api
import win32con
from nv.config import LICENSE_PATH


def set_license(content):
    win32api.SetFileAttributes(LICENSE_PATH, win32con.FILE_ATTRIBUTE_NORMAL)
    with open(LICENSE_PATH, 'w', encoding="utf-8") as fp:
        fp.write(content)
    win32api.SetFileAttributes(LICENSE_PATH, win32con.FILE_ATTRIBUTE_HIDDEN + win32con.FILE_ATTRIBUTE_SYSTEM)


def read_license():
    if not os.path.exists(LICENSE_PATH):
        return ""
    with open(LICENSE_PATH, 'r', encoding="utf-8") as fp:
        return "".join(fp.readlines()).strip()
