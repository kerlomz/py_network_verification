#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>


def is_unicode(uchar):
    if u'\u4e00' <= uchar <= u'\u9fff':
        return True
    else:
        return False


def contains_unicode(content):
    for uchar in content:
        if is_unicode(uchar):
            return True
        else:
            continue
    return False


def split_char(content):
    unicode_chars = []
    chars = []
    for i in content:
        if is_unicode(i):
            unicode_chars.append(i)
        else:
            chars.append(i)
    return len(unicode_chars), len(chars)


def calc_width(content, len1, len2):
    unicode_chars, chars = split_char(content)
    return int(unicode_chars * len1 + chars * len2)


if __name__ == '__main__':
    a = contains_unicode("")
    print(a)