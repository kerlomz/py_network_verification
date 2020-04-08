#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import tkinter as tk
from enum import Enum, unique

VAL_TYPE_MAP = {
    int: tk.IntVar,
    str: tk.StringVar,
    float: tk.DoubleVar
}


@unique
class Place(Enum):
    Next = 'Next'
    Prev = 'Prev'
    Below = 'Below'
    First = 'First'
    Inside = 'Inside'
    OutsideRight = 'OutsideRight'
    InsideRight = 'InsideRight'

