import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from tkinter.filedialog import *

# import pandas as pd

class SplitConverterFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)

        # field options
        options = {'padx': 0, 'pady': 1}

        self.split_size = 10  # 分割大小，单位为MB

        self.frame = ttk.Frame(self)
        self.initFrame(self.frame, **options)
        self.frame.grid(column=0, row=2, sticky="nsew", **options)
        self.frame.grid(column=0, row=2, sticky='w', **options)

        # add padding to the frame and show it
        self.grid(column=0, row=1, sticky="nsew", **options)

    def initFrame(self, container, **options):
        labFrame = ttk.LabelFrame(container, text="选择文件")  # 创建框架标签
        labFrame.grid(row=1, column=0, sticky='w', **options)

        self.textEntry = tk.StringVar()
        self.textneedEntry = tk.StringVar()
        self.textmesgEntry = tk.StringVar()

        # 选择目录
        label = ttk.Label(labFrame, text='选择拆分文件')
        label.pack(side=LEFT, padx=2)
        self.loca_text = ttk.Entry(labFrame, textvariable=self.textEntry, width=25)
        self.loca_text.pack(side=LEFT, fill=X, padx=2)
        loca = ttk.Button(labFrame, text="打开目录", command=self.openDir)
        loca.pack(side=LEFT, padx=2)

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

        self.dt.grid(row=2, column=0, sticky='w', **options)
        frame = ttk.Frame(self)
        frame.grid(row=4, column=0, sticky='w', **options)
        self.loca_need = ttk.Button(frame, text="拆分", command=self.splits)
        self.loca_need.grid(row=0, column=0, sticky='w', **options)
        self.textmesg = ttk.Entry(frame, textvariable=self.textmesgEntry, width=38)
        self.textmesg.grid(row=0, column=1, sticky='w', **options)

    def file_size(self, file_path):
        return os.path.getsize(file_path)  # 文件总大小，单位为字节

    def split_num(self, file_path):
        return self.file_size(file_path) // (self.split_size * 1024 * 1024) + 1  # 分割数量

    def splits(self):
        rows = self.dt.get_rows()
        for row in rows:
            self.spilt(row.values[0])
        self.textmesgEntry.set("拆分完成")

    def spilt(self, file_path):
        num = self.split_num(file_path)
        if num <= 1:
            return

        dir = os.path.dirname(file_path)
        baseName = os.path.basename(file_path)
        name, type = os.path.splitext(baseName)

        try:
            self.textmesgEntry.set(os.access(file_path, os.W_OK))
            with open(file_path, 'rb') as f:
                for i in range(num):
                    file_name = f'{dir}//{name}_{i}{type}'  # 分割后的文件名，以原文件名为前缀，加上部分编号
                    with open(file_name, 'wb') as fp:
                        b = f.read(self.split_size * 1024 * 1024)
                        fp.write(b)  # 每次读取分割大小的字节并写入文件中
                        fp.flush()
                        fp.close()
        except Exception as e:
            self.textmesgEntry.set(e)

    def openDir(self):
        filePaths = askopenfilenames()  # 选择目录，返回目录名
        for filePath in filePaths:
            if filePath.strip() != '':
                self.textEntry.set(filePath)  # 设置变量outputpath的值
                self.loca_text.configure(state="normal")
                self.loca_text.icursor(len(self.textEntry.get()) - 1)  # 将光标转移到第2个字符前
                self.loca_text.focus_set()  # 将焦点转移到文本框
                self.loca_text.configure(state="readonly")
                self.dt.insert_row(values=[filePath])
                self.dt.load_table_data()

    def reset(self):
        pass

    # def Data_split(self, filename, file_num, header=True):
    #     if header:
    #         # 设置每个文件需要有的行数,初始化为1000W
    #         chunksize = 10000
    #         data1 = pd.read_table(filename, chunksize=chunksize, sep=',', encoding='gbk')
    #         # print(data1)
    #         # num表示总行数
    #         num = 0
    #         for chunk in data1:
    #             num += len(chunk)
    #         # print(num)
    #         # chunksize表示每个文件需要分配到的行数
    #         chunksize = round(num / file_num + 1)
    #         # print(chunksize)
    #         # 分离文件名与扩展名os.path.split(filename)
    #         head, tail = os.path.split(filename)
    #         data2 = pd.read_table(filename, chunksize=chunksize, sep=',', encoding='gbk')
    #         i = 0
    #         for chunk in data2:
    #             chunk.to_csv('{0}_{1}{2}'.format(head, i, tail), header=None, index=False)
    #             self.textmesgEntry.set('保存第{0}个数据'.format(i))
    #             i += 1
    #     else:
    #         # 获得每个文件需要的行数
    #         chunksize = 10000
    #         data1 = pd.read_table(filename, chunksize=chunksize, header=None, sep=',')
    #         num = 0
    #         for chunk in data1:
    #             num += len(chunk)
    #             chunksize = round(num / file_num + 1)
    # 
    #             head, tail = os.path.split(filename)
    #             data2 = pd.read_table(filename, chunksize=chunksize, header=None, sep=',')
    #             i = 0
    #             for chunk in data2:
    #                 chunk.to_csv('{0}_{1}{2}'.format(head, i, tail), header=None, index=False)
    #                 self.textmesgEntry.set('保存第{0}个数据'.format(i))
    #                 i += 1
