#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import PIL.ImageTk
from gui.layout import LayoutGUI
import tkinter as tk
import tkinter.ttk as ttk
from gui.contansts import Place, VAL_TYPE_MAP
from gui.utils import contains_unicode, split_char, calc_width


class XLabel(ttk.Label):
    image: PIL.ImageTk.PhotoImage

    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

    def set_image(self, image: PIL.ImageTk.PhotoImage):
        self.configure(image=image)
        self.image = image


class XButton(ttk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

    def disable(self):
        self['state'] = tk.DISABLED

    def enable(self):
        self['state'] = tk.NORMAL


class XEntry(ttk.Entry):
    val: tk.Variable

    def __init__(self, master=None, val_type=str, val=None, **kw):
        super().__init__(master=master, **kw)
        self.init_val(val_type=val_type, val=val)

    def init_val(self, val_type=str, val=None):
        self.val = VAL_TYPE_MAP.get(val_type)(master=self, value=val)
        self['textvariable'] = self.val

    @property
    def variable(self):
        return self.val

    def disable(self):
        self['state'] = tk.DISABLED

    def enable(self):
        self['state'] = tk.NORMAL

    def readonly(self):
        self['state'] = 'readonly'


class Widget(object):

    def __init__(self, root, layout_utils: LayoutGUI):
        self.root = root
        self.layout_utils = layout_utils
        self.style = ttk.Style()
        self.init_style()

    def init_style(self):
        self.style.configure('B.TButton', font=('微软雅黑', 9))
        self.style.configure('B.TEntry', font=('微软雅黑', 9))
        self.style.configure('B.TCombobox', font=('微软雅黑', 9))
        self.style.configure('B.TListbox', font=('微软雅黑', 9))
        self.style.configure('B.TRadiobutton', font=('微软雅黑', 9))

    @staticmethod
    def widget_height(text):
        return 25 if contains_unicode(text) else 20

    def label(self, prev, place: Place, text: str = None, image=None, font=('微软雅黑', 9), tiny_space=False, height_offset=0):
        label: XLabel = XLabel(self.root, text=text, anchor=tk.W, font=font)
        if image:
            label_height = image.height()
            label_width = image.width()
        else:
            label_height = self.widget_height(text)
            label_width = calc_width(text, 15, 7.5)

        label.set_image(image)
        self.layout_utils.widget_place(
            src=label,
            prev=prev,
            place=place,
            width=label_width,
            height=label_height+height_offset,
            tiny_space=tiny_space
        )
        return label

    def radiobutton(self, prev, place: Place, title, var_rad, value, tiny_space=True):
        radiobutton: ttk.Radiobutton = ttk.Radiobutton(
            self.root, text=title, variable=var_rad, value=value, style='B.TRadiobutton'
        )
        label_height = self.widget_height(title)
        label_width = calc_width(title, 15, 7.5)
        self.layout_utils.widget_place(
            src=radiobutton,
            prev=prev,
            place=place,
            width=label_width * 1.8,
            height=label_height,
            tiny_space=tiny_space
        )
        return radiobutton

    def text(
            self,
            prev,
            place: Place,
            title: str,
            width,
            height,
            val=None,
            label_tiny_space=False,
            **kw
    ):
        label: ttk.Label = self.label(prev, place, title, tiny_space=label_tiny_space)
        text: tk.Text = tk.Text(self.root)
        text.insert(tk.INSERT, val)
        self.layout_utils.next_to_widget(
            src=text,
            target=label,
            width=width,
            height=height,
            tiny_space=True,
        )
        return label, text

    def entry(
            self,
            prev,
            place: Place,
            title: str,
            width,
            height=None,
            default=None,
            val_type=str,
            font=('微软雅黑', 9),
            label_tiny_space=False,
            show=None,
            height_offset=0,
            **kw
    ):
        label: ttk.Label = self.label(prev, place, title, tiny_space=label_tiny_space, height_offset=height_offset)
        label_height = self.widget_height(title)
        entry: XEntry = XEntry(self.root, justify=tk.LEFT, val_type=val_type, val=default, font=font, show=show, **kw)

        self.layout_utils.next_to_widget(
            src=entry,
            target=label,
            width=width,
            height=height if height else label_height,
            tiny_space=True,
            offset_y=height_offset / 2
        )
        return label, entry.variable, entry

    def combobox(
            self,
            prev,
            place: Place,
            title: str,
            options,
            current=1,
            editable=False,
            blank_click_callback=None,
            selected_callback=None,
            fill_callback=None,
            click_callback=None
    ):
        label: ttk.Label = self.label(prev, place, title)
        if not editable:
            combobox: ttk.Combobox = ttk.Combobox(
                self.root, values=tuple(options) if options else None, state='readonly', style='B.TCombobox'
            )
        else:
            combobox: ttk.Combobox = ttk.Combobox(
                self.root, values=tuple(options) if options else None
            )

        combobox.current(current)

        # 被选中回调
        if selected_callback:
            combobox.bind("<<ComboboxSelected>>", lambda x: selected_callback(x))
        max_length = max([calc_width(i, 15, 7.5) for i in options])
        combobox_height = 30 if contains_unicode(options[0]) else 20

        # 空白处回调
        if blank_click_callback:
            self.root.bind('<Button-1>', lambda x: blank_click_callback(x))

        # 填充回调
        if fill_callback:
            combobox.bind(
                sequence="<Return>",
                func=lambda x: fill_callback(x)
            )

        # 点击回调
        if click_callback:
            combobox.bind(
                sequence="<Button-1>",
                func=lambda x: click_callback(x)
            )

        self.layout_utils.next_to_widget(
            src=combobox,
            target=label,
            width=max_length + 25,
            height=combobox_height,
            tiny_space=True,

        )
        return label, combobox

    def listbox(self, prev, place: Place, title: str, width, height, delete_callback=None):
        label: ttk.Label = self.label(prev, place, title)
        listbox: tk.Listbox = tk.Listbox(self.root, font=('微软雅黑', 9))

        def delete_event(event, obj: tk.Listbox, callback=None):
            i = obj.curselection()[0]
            obj.delete(i)
            if callback:
                callback()

        def listbox_scrollbar(obj: tk.Listbox):
            y_scrollbar = tk.Scrollbar(
                obj, command=listbox.yview
            )
            y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            obj.config(yscrollcommand=y_scrollbar.set)

        self.layout_utils.next_to_widget(
            src=listbox,
            target=label,
            width=width,
            height=height,
            tiny_space=True
        )
        listbox.bind(
            sequence="<Delete>",
            func=lambda x: delete_event(x, delete_callback)
        )
        listbox_scrollbar(listbox)
        return label, listbox

    def button(self, prev, place: Place, title: str, callback, tiny_space=True, width=None):

        if callback:
            button: XButton = XButton(
                self.root, text=title, command=lambda: callback(), style='B.TButton'
            )
        else:
            button: XButton = XButton(
                self.root, text=title, style='B.TButton'
            )

        btn_height = 27 if contains_unicode(title) else 20
        uchar_len, char_len = split_char(title)
        btn_width = int(uchar_len * 15 + char_len * 7.5)
        btn_width = width if width else btn_width

        self.layout_utils.widget_place(
            src=button,
            prev=prev,
            place=place,
            width=btn_width * 1.8,
            height=btn_height,
            tiny_space=tiny_space
        )
        return button

    def label_frame(self, prev, place: Place, title: str, width, height, tiny_space=True, font=('微软雅黑', 9)):
        label = ttk.Label(self.root, text=title, font=font)
        label_frame: ttk.Labelframe = ttk.Labelframe(self.root, labelwidget=label)
        self.layout_utils.widget_place(
            src=label_frame,
            prev=prev,
            place=place,
            width=width,
            height=height,
            tiny_space=tiny_space
        )
        return label_frame
