import os
import tkinter as tk
from tkinter.messagebox import showerror
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from tkinter.filedialog import *


class MergeConverterFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 0, 'pady': 1}

        self.split_path = 'your_split_file_path'  # 分割文件路径
        self.merge_path = 'your_merge_file_path'  # 合并文件路径

        self.frame = ttk.Frame(self)  # 创建框架标签
        self.initFrame(self.frame, **options)
        self.frame.grid(column=0, row=2, sticky="nsew", **options)

        # add padding to the frame and show it
        self.grid(column=0, row=1, sticky="nsew", **options)

    def initFrame(self, container, **options):
        labFrame = ttk.LabelFrame(container, text="选择文件夹")  # 创建框架标签
        labFrame.grid(row=1, column=0, sticky='w', **options)

        self.textEntry = tk.StringVar()
        self.textneedEntry = tk.StringVar()
        self.textmesgEntry = tk.StringVar()

        # 选择目录
        label = ttk.Label(labFrame, text='选择目录')
        label.pack(side=LEFT, padx=2)
        self.loca_text = ttk.Entry(labFrame, textvariable=self.textEntry, width=25)
        self.loca_text.pack(side=LEFT, fill=X, padx=2)
        loca = ttk.Button(labFrame, text="打开目录", command=self.openDir)
        loca.pack(side=LEFT, padx=2)
        frame1 = ttk.Frame(container)
        frame1.grid(row=2, column=0, sticky='w', **options)
        label = ttk.Label(frame1, text='填写合并文件名称')
        label.grid(row=0, column=0, sticky='w', **options)
        self.textneed = ttk.Entry(frame1, textvariable=self.textneedEntry, width=25)
        self.textneed.grid(row=0, column=1, sticky='w', **options)

        # colors = self.container.style.colors

        coldata = [
            {"text": "文件", "stretch": True, "minwidth": 1050},
        ]

        rowdata = [
        ]

        self.dt = Tableview(
            master=container,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            pagesize=10,
            autoalign=True,
            autofit=True,
            searchable=False,
            bootstyle=PRIMARY,
            stripecolor=(None, None),
        )
        self.dt.grid(row=3, column=0, sticky='w', **options)

        frame = ttk.Frame(self)
        frame.grid(row=4, column=0, sticky='w', **options)
        self.loca_need = ttk.Button(frame, text="合并", command=self.merge)
        self.loca_need.grid(row=4, column=0, sticky='w', **options)
        self.textmesg = ttk.Entry(frame, textvariable=self.textmesgEntry, width=38)
        self.textmesg.grid(row=4, column=1, sticky='w', **options)

    def getFiles(self):
        self.file_list = os.listdir(self.split_path)  # 获取分割文件列表
        self.file_list.sort()  # 按文件名排序
        for file in self.file_list:
            self.dt.insert_row(values=[file])
            self.dt.load_table_data()

    def openDir(self):
        self.split_path = askdirectory()  # 选择目录，返回目录名
        self.merge_path = self.split_path
        if self.split_path.strip() != '':
            self.dt.delete_rows()
            self.textEntry.set(self.split_path)  # 设置变量outputpath的值
            self.loca_text.configure(state="normal")
            self.loca_text.icursor(len(self.textEntry.get()) - 1)  # 将光标转移到第2个字符前
            self.loca_text.focus_set()  # 将焦点转移到文本框
            self.loca_text.configure(state="readonly")
            self.getFiles()
        else:
            self.textmesgEntry.set("do not choose Dir")

    def merge(self):
        self.file_list = []
        mfile = self.textneedEntry.get() if self.textneedEntry.get() else "merge.tmp"
        rows = self.dt.get_rows()
        for row in rows:
            self.file_list.append(row.values[0])
        try:
            with open(self.merge_path+"\\"+mfile, 'wb') as f:
                for split_file in self.file_list:
                    split_file_path = os.path.join(self.split_path, split_file)  # 获取分割文件的完整路径
                    with open(split_file_path, 'rb') as part:
                        f.write(part.read())  # 在合并文件中写入分割文件的内容
            self.textmesgEntry.set("合并成功")
        except Exception as e:
            self.textmesgEntry.set(e)

    def reset(self):
        pass
