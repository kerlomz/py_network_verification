#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from tkinter import *
from tkinter.ttk import *
from nv.core import Core
from nv.config import set_license
from tkinter import messagebox
from gui.layout import LayoutGUI
from gui.widget import Widget
from gui.contansts import Place


class LicenseFrame(Frame):

    def __init__(self, parent, title='请输入使用许可', window_width=460, window_height=200):
        super().__init__()
        self.parent = parent
        # self.root.iconbitmap(System.resource_path("resource/icon.ico"))
        self.parent.title(title)
        self.window_width = window_width
        self.window_height = window_height
        self.layout_utils = LayoutGUI(self.window_width, self.window_height)
        self.widget = Widget(root=self.parent, layout_utils=self.layout_utils)
        self.core = Core()
        self.btn_submit = None
        self.text_machine_code = None
        self.auth_code = StringVar(value="")
        self.layout_utils.center_layout(self.parent)
        self.create_form()
        self.parent.mainloop()

    def create_form(self):
        self.parent.minsize(self.window_width, self.window_height)
        self.parent.maxsize(self.window_width, self.window_height)
        machine_code_label, machine_code = self.widget.text(
            prev=None, place=Place.First, title="机器码：", width=360, height=100, val=self.core.machine_code()
        )
        label, self.auth_code, entry = self.widget.entry(
            prev=machine_code_label, place=Place.Below, title="许可号：", width=290, height_offset=150
        )
        self.btn_submit = self.widget.button(
            prev=entry, place=Place.Next, title="确定", callback=self.save_license, tiny_space=False
        )

        # Label(self.parent, text='机器码：', font=('微软雅黑', 10)).place(x=init_padding, y=20)
        # Label(self.parent, text='许可号：', font=('微软雅黑', 10)).place(x=init_padding, y=140)
        # self.text_machine_code = Text(self.parent)
        # self.text_machine_code.insert(INSERT, self.core.machine_code())
        # self.text_machine_code.place(
        #     x=init_padding + 5 * placeholder_width + object_interval, y=20 + height_offset, width=360, height=100
        # )
        #
        # text_auth_code = Entry(self.parent, textvariable=self.auth_code)
        # text_auth_code.place(x=init_padding + 5 * placeholder_width + object_interval, y=140 + height_offset, width=250)
        # self.btn_submit = Button(self.parent, text='确定', command=self.save_license, width=11, state=NORMAL)
        # self.btn_submit.place(x=init_padding + 5 * placeholder_width + object_interval + 285, y=140)

    @staticmethod
    def get_screen_size(window):
        return window.winfo_screenwidth(), window.winfo_screenheight()

    @staticmethod
    def get_window_size(window):
        return window.winfo_reqwidth(), window.winfo_reqheight()

    def save_license(self):
        set_license(self.auth_code.get().strip())
        f = messagebox.showinfo(title='成功', message='许可已设置，请重启软件，有问题请联系作者')
        if f:
            sys.exit()


if __name__ == '__main__':
    page = LicenseFrame(Tk())
