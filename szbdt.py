#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by ： Liu Xiang
Email to   ： liuxiangxyd@163.com
Started Date：30 May 2018

一、镀锌、喷涂线槽计算公式
1. 槽身成本=[2*(高+折边)+宽]*长*槽厚*槽吨价*密度/1,000,000
2. 槽盖成本=(宽+2*折边)*长*盖厚*盖吨价*密度/1,000,000
3. 喷涂费 = (高+宽)*4*长*每平米喷涂费/1,000
4. 镀锌每条毛利率=（1-每条成本价/每条销售价）*100%
5. 喷涂每条毛利率=（1-每条喷涂成本价/每条喷涂销售价）*100%
6-11: 上述两个公式修改一下，有可能改变运行误差。
4. 镀锌每条毛利率%=（每条销售价-每条成本价）*100/每条销售价
5. 喷涂每条毛利率%=（每条喷涂销售价-每条喷涂成本价）*100/每条喷涂销售价
注意：取小数点后2位。

常用数据，节省输入时间，方便用户选择，避免错误数据输入：
第一排为：
长: [2],宽:[60,80,100,150,200],高:[40,60,80,100],折边:[10,15,20],密度:[7.85],
第二排为：
    吨价（槽,盖）:[5150,5200,5250,5350,5800,6150],
    厚（槽,盖）:[0.35,0.45,0.6,0.7,0.8,0.9,1.0,1.2],
    每平米喷涂费:[0,5.5,6.5,9,10],

后面的上浮率为
    上浮率%:[0,5,6,7,8,9,10,11,12,13,14,15]

二、图形界面采用内部模块 tkinter 设计样式

三、Python源码采用pyInstaller工具进行编译发布

    pyinstaller -F -w -i myicon.ico

    注意：请在32位的Python环境下运行，兼容性比较好，可以在Windows7/10 32bit/64bit OS下运行。
    64位Python环境下发布的执行文件只能在64位操作系统下运行。

四、执行文件 bdt.exe，图标文件 myicon.ico

五、运行方式
1. 直接点击执行文件 bdt.exe
   这时显示的公司名称为缺省公司名称：深圳市八达通线管桥架有限公司
2. 在DOS命令行下，运行 C:\bdt>bdt 《新公司名》
   这时显示的是《新公司名》
3. 建立快捷键，在快捷键的目标（T）中，增加新公司名，如
   C:bdt\bdt.exe XXXX公司
   以后就点击这个快捷键就可以了。
4. 如果希望改变图标按钮，可以修改myicon.ico的图形，与执行文件放在一个目录下。

TODO：
（1）输入数据格式检查，是否为正确的数字格式？
（2）关键数字修改，是否自动计算结果？

"""

__author__ = "Liu Xiang"
from tkinter import *
import tkinter.messagebox as messagebox
from tkinter.ttk import Combobox
from sys import argv
from os.path import exists

# Global variables 全局变量定义设置
# 1-可选输入框中的名称和选项列表，采用dict数据格式保存
lbl_name = {'长':[2],
            '宽':[60, 80, 100, 150, 200],
            '高':[40, 60, 80, 100],
            '折边':[10, 15, 20],
            '密度':[7.85],
            '槽吨价':[5150, 5200, 5250, 5350, 5800, 6150],
            '盖吨价':[5150, 5200, 5250, 5350, 5800, 6150],
            '槽厚':[0.35, 0.45, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2],
            '盖厚':[0.35, 0.45, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2],
            '喷涂费':[0, 5.5, 6.5, 9, 10],
            '槽身成本价':[],
            '槽身销售价':[],
            '上浮率%':[0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            '槽盖成本价':[],
            '槽盖销售价':[],
            '上浮率2%':[0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            '每条成本价':[],
            '每条销售价':[],
            '毛利率%':[],
            '喷涂成本':[],
            '每条喷涂':[],
            '上浮率3%':[0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            '每条喷涂线槽成本':[],
            '线槽销售价':[],
            '毛利率2':[]
            }

# 输入框常用长度设置
entry_len = 7
# 计算结果缺省长度设置
result_len = 13
# 列数常数设置
ncolumn = 5
# 显示缺省公司名称设置
defaultCompany = '深圳市八达通线管桥架有限公司'
# 可选字体选项，用以区分关键结果显示和其他类型
defaultFont=[("Times New Roman", 14), ("Calibri", 16), ("Arial", 18)]

# 关键类定义如下Application
class Application(Frame):
    """The Main Application, 初始化关键类，界面显示，公式运行等"""
    # 分割线，输入行数，和高度值
    def separator(self, rows, heights):
        # 行分隔符，输入行数（分隔符位置），高度值（大小）
        sep = Frame(height=heights, bd=1, relief=GROOVE, colormap="new")
        sep.grid(row=rows, sticky=W+E+N+S)

    def column_sep(self, columns, widths):
        # TODO : 列分隔符，输入列数（分隔符位置），宽度（大小）
        colsep = Frame(width=widths, bd=1, relief=SUNKEN)
        colsep.grid(column=columns, sticky=W+E+N+S)

    def __init__(self, master=None):
        # 初始化应用程序
        Frame.__init__(self, master)
        self.grid()    # self.pack()

        self.separator(rows=0, heights=17)
        # self.column_sep(columns=0,widths=15)
        Frame1 = Frame(master, bg="#CCCCCC")  # , width=1000, height=400)
        Frame1.grid(row=1, column=0, sticky=W+E+N+S)

        self.separator(rows=6, heights=7)
        Frame2 = Frame(master, bg="#999999")  # ,width=1000, height=600)
        Frame2.grid(row=7, column=0, sticky=W+E+N+S)

        self.separator(rows=14, heights=7)
        Frame3 = Frame(master, bg="#666666")  # ,width=1000, height=400)
        Frame3.grid(row=15, column=0, sticky=W+E+N+S)  # rowspan=3, columnspan=2,
        self.separator(rows=18, heights=17)

        # 输入提示栏标签
        keys = list(lbl_name.keys())
        # 布局 前10个输入框的提示标识。
        for i in range(10):
            i_tmp = i // ncolumn
            Label(Frame1, text=keys[i], width=7).grid(column=2*(i-i_tmp*ncolumn),
                  row=2*i_tmp+1)
        # Label(Frame1, text="请选择或输入上述参数，然后点击“确认”按钮...",
        #      font=defaultFont[0], fg="red",
        #      relief=RIDGE).grid(column=0, row=5, columnspan=6)
        # 布局 输出镀锌线槽结果栏的标签提示
        for i in range(10, 13):
            Label(Frame2, text=keys[i], width=9).grid(column=2*i-20, row=7)
        for i in range(13, 15):
            Label(Frame2, text=keys[i], width=9).grid(column=2*i-26, row=9)
        # 特殊对待"上浮率%"，多个上浮率采用同一个
        Label(Frame2, text=keys[12], width=9).grid(column=2*15-26, row=9)
        for i in range(16, 19):
            Label(Frame2, text=keys[i], width=9).grid(column=2*i-32, row=11)

        # tmp = Label(Frame2, text="请选择或输入上浮率，然后点击“镀锌销售价格”...",
        #           font=defaultFont[0],  fg="red", relief=RIDGE)
        # tmp.grid(column=0, row=13, columnspan=6)

        # 布局 输出喷涂线槽结果栏的标签提示
        Label(Frame3, text=keys[19], width=9+5).grid(column=2*19-38, row=15)
        Label(Frame3, text=keys[20], width=9).grid(column=2*20-38, row=15)
        # 特别对待"上浮率%"
        Label(Frame3, text=keys[12], width=9).grid(column=2*21-38, row=15)
        Label(Frame3, text=keys[22], width=9+5).grid(column=2*22-44, row=17)
        Label(Frame3, text=keys[23], width=9).grid(column=2*23-44, row=17)
        # 特别对待“毛利率%”
        Label(Frame3, text=keys[18], width=9).grid(column=2*24-44, row=17)

        # tmp = Label(Frame3, text="请选择或输入上浮率，然后点击“喷涂销售价格”...",
        #            font=defaultFont[0], fg="red", relief=RIDGE)
        # tmp.grid(column=0, row=19, columnspan=6)

        self.csj = StringVar()    # 槽身成本价格
        self.cgj = StringVar()    # 槽盖成本价格
        self.hjcb = StringVar()   # 合计成本价格
        self.csxsj = StringVar()  # 槽身销售价格
        self.cgxsj = StringVar()  # 槽盖销售价格
        self.hjxsj = StringVar()  # 合计销售价格
        self.ptf = StringVar()    # 喷涂成本价
        self.ptcb = StringVar()   # 每条喷涂线槽成本
        self.ptxsj = StringVar()  # 每条喷涂线槽销售价
        self.maolv1 = StringVar()  # 镀锌销售毛利率%
        self.maolv2 = StringVar()  # 喷涂销售毛利率%

        self.createEntry(Frame1)  # 设置UI界面
        self.createResult(Frame2)
        self.createPentu(Frame3)

    def createEntry(self, frm):
        # 第一行 输入框选择信息标识，采用tkinter.Combobox
        self._lengthInput = Combobox(frm, width=entry_len)
        self._lengthInput['values'] = lbl_name['长']
        self._lengthInput.current(0)  # set the selected item
        self._lengthInput.grid(column=1, row=1)

        self._widthInput = Combobox(frm, width=entry_len)
        self._widthInput['values'] = lbl_name['宽']
        self._widthInput.current(0)
        self._widthInput.grid(column=3, row=1)

        self._heightInput = Combobox(frm, width=entry_len)
        self._heightInput['values'] = lbl_name['高']
        self._heightInput.current(0)
        self._heightInput.grid(column=5, row=1)

        self._zbInput = Combobox(frm, width=entry_len)
        self._zbInput['values'] = lbl_name['折边']
        self._zbInput.current(0)
        self._zbInput.grid(column=7, row=1)

        self._mdInput = Combobox(frm, width=entry_len)
        self._mdInput['values'] = lbl_name['密度']
        self._mdInput.current(0)
        self._mdInput.grid(column=9, row=1)

        # 第二行输入框选择信息标识，采用tkinter.Combobox
        self._cdjInput = Combobox(frm, width=entry_len)
        self._cdjInput['values'] = lbl_name['槽吨价']
        self._cdjInput.current(0)
        self._cdjInput.grid(column=1, row=3)

        self._gdjInput = Combobox(frm, width=entry_len)
        self._gdjInput['values'] = lbl_name['盖吨价']
        self._gdjInput.current(0)
        self._gdjInput.grid(column=3, row=3)

        self._chInput = Combobox(frm, width=entry_len)
        self._chInput['values'] = lbl_name['槽厚']
        self._chInput.current(0)
        self._chInput.grid(column=5, row=3)

        self._ghInput = Combobox(frm, width=entry_len)
        self._ghInput['values'] = lbl_name['盖厚']
        self._ghInput.current(0)
        self._ghInput.grid(column=7, row=3)

        self._ptfInput = Combobox(frm, width=entry_len)
        self._ptfInput['values'] = lbl_name['喷涂费']
        self._ptfInput.current(3)
        self._ptfInput.grid(column=9, row=3)

        # 按钮“确认”, 计算每条槽身和槽盖的成本价格
        self.alertButton = Button(frm, text='确定', width=12, fg="red",
                                  font=defaultFont[0], command=self.calPrice)
        self.alertButton.grid(row=5, column=8, columnspan=2, sticky=E)

        # "Help" button
        self.helpButton = Button(frm, text='帮助', width=12, fg="red",
                                 font=defaultFont[0], command=self.helpinfo)
        self.helpButton.grid(row=5, column=0, columnspan=2, sticky=W)

    def createResult(self, frm):
        # Frame2 输出镀锌线槽结果栏数据显示区域
        self._lblcsj = Label(frm, bg="white", fg="red", width=result_len,
                             textvariable=self.csj, relief=RAISED)
        self._lblcsj.grid(column=1, row=7)  # 镀锌槽身成本价格

        self._lblcgj = Label(frm, bg="white", fg="red", width=result_len,
                             textvariable=self.cgj, relief=RAISED)
        self._lblcgj.grid(column=1, row=9)  # 镀锌槽盖成本价格

        self._lblhjcb = Label(frm, bg="white", fg="red", width=result_len-4,
                              font=defaultFont[0], textvariable=self.hjcb, relief=RAISED)
        self._lblhjcb.grid(column=1, row=11)  # 镀锌成本价格

        self._lblcsxsj = Label(frm, bg="white", fg="red", width=result_len,
                               textvariable=self.csxsj, relief=RAISED)
        self._lblcsxsj.grid(column=3, row=7)  # 镀锌槽身销售价格

        self._lblcgxsj = Label(frm, bg="white", fg="red", width=result_len,
                               textvariable=self.cgxsj, relief=RAISED)
        self._lblcgxsj.grid(column=3, row=9)  # 镀锌槽盖销售价格

        self._lblhjxsj = Label(frm, bg="white", fg="red", width=result_len-4,
                               font=defaultFont[0], textvariable=self.hjxsj, relief=RAISED)
        self._lblhjxsj.grid(column=3, row=11)  # 镀锌销售价格

        self._lbldxmlv = Label(frm, bg="white", fg="blue", width=entry_len+3,
                               font=defaultFont[0], textvariable=self.maolv1, relief=FLAT)
        self._lbldxmlv.grid(column=6, row=11)  # 镀锌销售毛利率%

        # 毛利率输入栏： csratio 槽身，cgratio 槽盖
        self._csrInput = Combobox(frm, width=entry_len+5)
        self._csrInput['values'] = lbl_name['上浮率%']
        self._csrInput.current(6)
        self._csrInput.grid(column=6, row=7)

        self._cgrInput = Combobox(frm, width=entry_len+5)
        self._cgrInput['values'] = lbl_name['上浮率%']
        self._cgrInput.current(6)
        self._cgrInput.grid(column=6, row=9)

        # 按钮“计算镀锌销售价格”
        self.saleButton = Button(frm, text='镀锌销售价格', width=12, height=1,
                                 font=defaultFont[0], fg="red", command=self.salePrice)
        self.saleButton.grid(column=8, row=9, columnspan=2, rowspan=4, sticky=E+S)

    def createPentu(self, frm):
        # 输出喷涂线槽结果栏数据显示区域
        # 1. 喷涂成本价
        self._lblptj = Label(frm, bg="white", fg="red", width=result_len,
                             textvariable=self.ptf, relief=RAISED)
        self._lblptj.grid(column=1, row=15)
        # 2. 每条喷涂线槽成本价
        self._lblptcb = Label(frm, bg="white", fg="red", width=result_len-4,
                              font=defaultFont[0], textvariable=self.ptcb, relief=RAISED)
        self._lblptcb.grid(column=1, row=17)
        # 3. 每条喷涂线槽销售价格
        self._lblptxsj = Label(frm, bg="white", fg="red", width=result_len-4,
                               font=defaultFont[0], textvariable=self.ptxsj, relief=RAISED)
        self._lblptxsj.grid(column=3, row=17, rowspan=2)
        # 4. 喷涂上浮率输入栏
        self._ptrInput = Combobox(frm, width=entry_len)
        self._ptrInput['values'] = lbl_name['上浮率%']
        self._ptrInput.current(6)
        self._ptrInput.grid(column=6, row=15)
        # 5. 喷涂销售毛利率%
        self._lblptmlv = Label(frm, bg="white", fg="blue", width=entry_len,
                               font=defaultFont[0], textvariable=self.maolv2, relief=FLAT)
        self._lblptmlv.grid(column=6, row=17)

        # 按钮“计算喷涂销售价格”
        self.saleButton = Button(frm, text='喷涂销售价格', width=12,
                                 font=defaultFont[0], fg="red", command=self.calPentu)
        self.saleButton.grid(column=7, row=15, columnspan=2, rowspan=3, sticky=E+S)

    def calPrice(self):
        # Frame2 中计算镀锌成本价格
        try:
            _length = float(self._lengthInput.get())
            _width = float(self._widthInput.get())
            _height = float(self._heightInput.get())
            _zb = float(self._zbInput.get())

            _md = float(self._mdInput.get())
            _cdj = float(self._cdjInput.get())
            _gdj = float(self._gdjInput.get())
            _ch = float(self._chInput.get())
            _gh = float(self._ghInput.get())

            self._csj_f = (2*(_height+_zb)+_width)*_length*_ch*_cdj*_md/1000000
            self._cgj_f = (_width+2*_zb)*_length*_gh*_gdj*_md/1000000
            self._hjcb_f = self._csj_f + self._cgj_f   # 镀锌合计成本价格

            self.csj.set(format(self._csj_f, '.2f'))
            self.cgj.set(format(self._cgj_f, '.2f'))
            self.hjcb.set(format(self._hjcb_f, '.2f'))
        except ValueError as ve:
            self.errinfo("错误信息", ve)

    def salePrice(self):
        # Frame2 中计算镀锌销售价格
        self.calPrice()
        try:
            self._csxsj_f = self._csj_f * (1+float(self._csrInput.get())/100)
            self._cgxsj_f = self._cgj_f * (1+float(self._cgrInput.get())/100)
            self._hjxsj_f = self._csxsj_f + self._cgxsj_f   # 镀锌合计销售价格

            self._dxmlv_f = (self._hjxsj_f-self._hjcb_f)*100/self._hjxsj_f

            self.csxsj.set(format(self._csxsj_f, '.2f'))
            self.cgxsj.set(format(self._cgxsj_f, '.2f'))
            self.hjxsj.set(format(self._hjxsj_f, '.2f'))
            self.maolv1.set(format(self._dxmlv_f, '.2f'))
        except ValueError as ve:
            self.errinfo("错误信息", ve)


    def calPentu(self):
        # Frame3 中计算喷涂成本价格
        self.salePrice()
        try:
            _length = float(self._lengthInput.get())
            _width  = float(self._widthInput.get())
            _height = float(self._heightInput.get())
            _ptf = float(self._ptfInput.get())
            # 1 喷涂加工成本价格，有公式
            self._ptf_f = (_height+_width)*4*_length*_ptf/1000
            self.ptf.set(format(self._ptf_f, '.2f'))
            # 2 每条喷涂线槽成本价格=喷涂成本+镀锌成本
            self._ptcb_f = self._hjcb_f + self._ptf_f
            self.ptcb.set(format(self._ptcb_f, '.2f'))
            # 3 Frame3 中计算每条喷涂线槽销售价格=喷涂线槽成本*（1+上浮率%）
            self._ptxsj_f = self._ptcb_f * (1+float(self._ptrInput.get())/100)
            self.ptxsj.set(format(self._ptxsj_f, '.2f'))
            # 4 喷涂销售毛利率
            self._ptmlv_f = (self._ptxsj_f-self._ptcb_f)*100/self._ptxsj_f
            #(1.0-self._ptcb_f/self._ptxsj_f)*100
            self.maolv2.set(format(self._ptmlv_f, '.2f'))
            
        except ValueError as ve:
            self.errinfo("错误信息", ve)

    def errinfo(self, title, msg):
        messagebox.showerror(title, msg)

    def helpinfo(self):
        messagebox.showinfo("帮助信息",
        "运行方式：\n\
            1. bdt \n\
               公司名称显示为缺省的公司名。 \n\
            2. bdt 公司名称 \n\
               更改公司名称为  公司名称")


if __name__ == '__main__':
    apptitle = defaultCompany
    if len(argv) > 1:
        _, apptitle = argv
    """if apptitle.lower() in ['-h','--help','-help','-?']:
        print(""
              运行方式：
              1. szbdt
                 公司名称显示为缺省的公司名：深圳市八达通线管桥架有限公司
              2. szbdt 公司名称
                 更改公司名称为  ‘新公司名’
              3. szbdt -help
                 显示本帮助信息。
              "")
        apptitle = defaultCompany"""

    root = Tk()
    root.resizable(width=False, height=False)
    app = Application(root)
    # 设置窗口标题:
    app.master.title(apptitle)
    # app.master.maxsize(800,600)
    if exists(r"~/liuxiang0/szbdt/myicon.ico"):
        root.iconbitmap(r"~/liuxiang0/szbdt/myicon.ico")
    # 主消息循环:
    app.mainloop()
