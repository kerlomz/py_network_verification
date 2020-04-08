#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from gui.contansts import Place
from tkinter import ttk


class LayoutGUI(object):

    def __init__(self, window_width, window_height):
        self.layout = {
            'global': {
                'start': {'x': 15, 'y': 20},
                'space': {'x': 15, 'y': 25},
                'tiny_space': {'x': 5, 'y': 10}
            }
        }
        self.window_width = window_width
        self.window_height = window_height

    def center_layout(self, root):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (
            self.window_width,
            self.window_height,
            (screenwidth - self.window_width) / 2,
            (screenheight - self.window_height) / 2
        )
        root.geometry(size)

    def first_object(self, src, width, height):
        src.place(
            x=self.layout['global']['start']['x'],
            y=self.layout['global']['start']['y'],
            width=width,
            height=height,
        )

    def widget_outside_right(self, src, target, width, height, tiny_space=False):
        target_edge = self.object_edge_info(target)
        src.place(
            x=self.window_width - width - self.layout['global']['space']['x'],
            y=target_edge['edge_y'] + self.layout['global']['tiny_space' if tiny_space else 'space']['y'],
            width=width,
            height=height
        )

    def widget_inside_right(self, src, target, width, height, tiny_space=False):
        target_edge = self.object_edge_info(target)
        src.place(
            x=target_edge['edge_x'] - self.layout['global']['space']['x'] - width,
            y=target_edge['edge_y'] - self.layout['global']['tiny_space' if tiny_space else 'space']['y'] - height,
            width=width,
            height=height
        )

    def before_widget(self, src, target, width, height, tiny_space=False):
        target_edge = self.object_edge_info(target)
        src.place(
            x=target_edge['x'] - width - self.layout['global']['tiny_space' if tiny_space else 'space']['x'],
            y=target_edge['y'],
            width=width,
            height=height
        )

    @staticmethod
    def object_edge_info(obj):
        info = obj.place_info()
        x = int(info['x'])
        y = int(info['y'])
        edge_x = int(info['x']) + int(info['width'])
        edge_y = int(info['y']) + int(info['height'])
        return {'x': x, 'y': y, 'edge_x': edge_x, 'edge_y': edge_y}

    def inside_widget(self, src, target, width, height):
        target_edge = self.object_edge_info(target)
        src.place(
            x=target_edge['x'] + self.layout['global']['space']['x'],
            y=target_edge['y'] + self.layout['global']['space']['y'],
            width=width,
            height=height
        )

    def below_widget(self, src, target, width, height, tiny_space=False):
        target_edge = self.object_edge_info(target)
        src.place(
            x=target_edge['x'],
            y=target_edge['edge_y'] + self.layout['global']['tiny_space' if tiny_space else 'space']['y'],
            width=width,
            height=height
        )

    def below_group(self, src, prev_label, prev_obj, width, height):
        label_edge = self.object_edge_info(prev_label)
        widget_edge = self.object_edge_info(prev_obj)
        src.place(
            x=label_edge['x'],
            y=widget_edge['edge_y'] + self.layout['global']['space']['y'] / 2,
            width=width,
            height=height
        )

    def next_to_widget(self, src, target, width, height, tiny_space=False, offset_y=0):
        target_edge = self.object_edge_info(target)
        src.place(
            x=target_edge['edge_x'] + self.layout['global']['tiny_space' if tiny_space else 'space']['x'],
            y=target_edge['y'] + offset_y,
            width=width,
            height=height
        )

    def widget_place(self, src, prev, place, width, height, tiny_space=False):
        if place == place.First or not prev:
            self.first_object(
                src=src,
                width=width,
                height=height
            )
        elif place == Place.Next:
            self.next_to_widget(
                src=src,
                target=prev,
                width=width,
                height=height,
                tiny_space=tiny_space
            )
        elif place == Place.Below:
            if isinstance(prev, list) and len(prev) == 2:
                self.below_group(
                    src=src,
                    prev_label=prev[0],
                    prev_obj=prev[1],
                    width=width,
                    height=height,
                )
            else:
                self.below_widget(
                    src=src,
                    target=prev,
                    width=width,
                    height=height,
                    tiny_space=tiny_space
                )
        elif place == Place.Inside:
            if not isinstance(prev, ttk.Labelframe):
                raise ValueError("The layout only works for Labelframe.")
            self.inside_widget(
                src=src,
                target=prev,
                width=width,
                height=height,
            )
        elif place == Place.OutsideRight:
            if not isinstance(prev, ttk.Labelframe):
                raise ValueError("The layout only works for Labelframe.")
            self.widget_outside_right(
                src=src,
                target=prev,
                width=width,
                height=height,
            )
        elif place == Place.InsideRight:
            if not isinstance(prev, ttk.Labelframe):
                raise ValueError("The layout only works for Labelframe.")
            self.widget_inside_right(
                src=src,
                target=prev,
                width=width,
                height=height,
            )
        elif place == Place.Prev:
            self.before_widget(
                src=src,
                target=prev,
                width=width,
                height=height,
            )