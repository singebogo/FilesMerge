import tkinter as tk
from tkinter import ttk

from src.gui.converterFrame.splitConverterFrame import SplitConverterFrame
from src.gui.converterFrame.mergeConverterFrame import MergeConverterFrame


class ControlFrame(ttk.LabelFrame):

    def __init__(self, container):
        super(ControlFrame, self).__init__(container)

        self['text'] = '类型'
        options = {'padx': 0, 'pady': 1}
        # radio buttons
        self.selected_value = tk.IntVar()
        ttk.Radiobutton(
            self,
            text='拆分',
            value=0,
            variable=self.selected_value,
            command=self.change_frame).grid(column=0, row=0, **options)

        ttk.Radiobutton(
            self,
            text='合并',
            value=1,
            variable=self.selected_value,
            command=self.change_frame).grid(column=1, row=0, **options)

        self.grid(column=0, row=0, sticky='w', **options)

        # initialize frames
        self.frames = {}
        self.frames[0] = SplitConverterFrame(
            container)
        self.frames[1] = MergeConverterFrame(
            container)

        self.change_frame()

    def change_frame(self):
        self.frame = self.frames[self.selected_value.get()]
        self.frame.reset()
        self.frame.tkraise()
