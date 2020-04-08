#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from nv.config import LICENSE_PATH


def set_license(content):
    with open(LICENSE_PATH, 'w', encoding="utf-8") as fp:
        fp.write(content)


def read_license():
    with open(LICENSE_PATH, 'r', encoding="utf-8") as fp:
        return "".join(fp.readlines()).strip()
