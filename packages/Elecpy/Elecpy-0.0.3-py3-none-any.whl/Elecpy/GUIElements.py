# coding=utf-8
"""
该模块中的类涵盖了GUI可能用到的各种复合控件，如主界面、滚动画布、目录框、按钮区等
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import *
import tkinter.filedialog as fdlg
import tkinter.messagebox as msg
from math import *
import numpy as np
import pandas as pd


class CirPage:
    """
    类：电路页面，包括三个区域：编辑区域、工具条区域、电路图区域，每个区域是一个Frame对象
    """
    def __init__(self,
                 win_title='Elecpy GUI by Aiqy',
                 geometry=None):
        """
        method: 创建主页面
        :param win_title: 窗口标题
        :param geometry: 窗口几何尺寸, [例]"1200x900"
        """
        """创建window"""
        self.window = tk.Tk()
        self.window.title(win_title)
        if geometry is None:
            self.window.state('zoomed')
            self.window.update()
            self.win_width = self.window.winfo_width()
            self.win_height = self.window.winfo_height()
            geometry = str(self.win_width) + 'x' + str(self.win_height)
        else:
            self.win_width = int(geometry.split('x')[0])
            self.win_height = int(geometry.split('x')[1])
        self.window.geometry(geometry)

        """创建各区域的LabelFrame"""
        # 文件操作区域
        self.frame_title = tk.LabelFrame(self.window, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                         height=32,
                                         width=self.win_width)
        self.frame_title.grid(row=0, column=0)
        self.frame_title.grid_propagate(0)

        # 工具条区域
        self.frame_tools = tk.LabelFrame(self.window, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                         height=32,
                                         width=self.win_width)
        self.frame_tools.grid(row=1, column=0)
        self.frame_tools.grid_propagate(0)

        # 电路图区域
        self.frame_wrk = tk.LabelFrame(self.window, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                       height=self.win_height - 64,
                                       width=self.win_width)
        self.frame_wrk.grid(row=2, column=0)
        self.frame_wrk.grid_propagate(0)

    def maintain(self):
        """
        method: 保持该主页面, 即window的.mainloop()方法
        :return: 无
        """
        self.window.mainloop()

    def destroy(self):
        """
        method: 删除自己
        :return: 无
        """
        self.window.destroy()


class MainPage:
    """
    类：主页面，包括五个区域：标题区域、项目区域、工作区域、详细区域、状态区域，每个区域是一个Frame对象
    """
    def __init__(self,
                 win_title='Elecpy GUI by Aiqy',
                 page_title=None,
                 geometry=None):
        """
        method: 创建主页面
        :param win_title: 窗口标题
        :param page_title: 页面标题
        :param geometry: 窗口几何尺寸, [例]"1200x900"
        """
        """创建window"""
        self.window = tk.Tk()
        self.window.title(win_title)
        if geometry is None:
            self.window.state('zoomed')
            self.window.update()
            self.win_width = self.window.winfo_width()
            self.win_height = self.window.winfo_height()
            geometry = str(self.win_width) + 'x' + str(self.win_height)
        else:
            self.win_width = int(geometry.split('x')[0])
            self.win_height = int(geometry.split('x')[1])
        self.window.geometry(geometry)

        """创建各区域的LabelFrame"""
        # 标题区域
        self.frame_title = tk.LabelFrame(self.window, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                         height=self.win_height / 20,
                                         width=self.win_width)
        self.frame_title.grid(row=0, column=0, columnspan=3)
        self.frame_title.grid_propagate(0)

        # 项目区域
        self.frame_prj = tk.LabelFrame(self.window, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                       height=self.win_height * 17 / 20,
                                       width=self.win_width / 10)
        self.frame_prj.grid(row=1, column=0)
        self.frame_prj.grid_propagate(0)

        # 工作区域
        self.frame_wrk = tk.LabelFrame(self.window, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                       height=self.win_height * 17 / 20,
                                       width=self.win_width * 7 / 10)
        self.frame_wrk.grid(row=1, column=1)
        self.frame_wrk.grid_propagate(0)

        # 详细区域
        self.frame_dtl = tk.LabelFrame(self.window, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                       height=self.win_height * 17 / 20,
                                       width=self.win_width / 5)
        self.frame_dtl.grid(row=1, column=2)
        self.frame_dtl.grid_propagate(0)

        # 状态区域
        self.frame_status = tk.LabelFrame(self.window, bg='#F0F0F0', text=None, font=('仿宋', 12),
                                          height=self.win_height / 10,
                                          width=self.win_width)
        self.frame_status.grid(row=2, column=0, columnspan=3)
        self.frame_status.grid_propagate(0)

        """在标题区域(frame_title)上的操作"""
        if page_title is not None:
            self.title = tk.Label(self.frame_title, text=page_title, anchor='center', font=('微软雅黑', 35),
                                  height=1, width=46, bg='#F0F0F0', fg='green')
            self.title.grid(row=0, column=0)

    def maintain(self):
        """
        method: 保持该主页面, 即window的.mainloop()方法
        :return: 无
        """
        self.window.mainloop()

    def destroy(self):
        """
        method: 删除自己
        :return: 无
        """
        self.window.destroy()


class CompPage:
    """
    class: 创建一个元件页面
    """
    def __init__(self,
                 width=None,
                 height=None):
        """
        method: 创建一个窗口高度和宽度为width和height的显示元件的页面，如果width和height没有给定，则窗口全屏
        :param width: 窗口宽度
        :param height: 窗口高度
        """
        """创建窗口"""
        self.root = tk.Tk()
        self.root.title('Component')
        if width and height:
            geometry = str(width) + 'x' + str(height)
        else:
            self.root.state('zoomed')
            self.root.update()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            geometry = str(width) + 'x' + str(height)
        self.root.geometry(geometry)
        self.frame = tk.LabelFrame(self.root, bg='#F0F0F0', text=None, font=('仿宋', 12), height=height, width=width)
        self.frame.grid(row=0, column=0, columnspan=3)
        self.frame.grid_propagate(0)

    def maintain(self):
        """
        method: 保持该主页面, 即window的.mainloop()方法
        :return: 无
        """
        self.root.mainloop()

    def destroy(self):
        """
        method: 删除自己
        :return: 无
        """
        self.root.destroy()


class NormalPage:
    """
    class: 创建一个普通页面，提供frame
    """
    def __init__(self,
                 title='Normal',
                 width=None,
                 height=None):
        """
        method: 创建一个窗口高度和宽度为width和height的显示元件的页面，如果width和height没有给定，则窗口全屏
        :param title: 标题
        :param width: 窗口宽度
        :param height: 窗口高度
        """
        """创建窗口"""
        self.root = tk.Toplevel()
        self.root.title(title)
        if width and height:
            geometry = str(width) + 'x' + str(height)
        else:
            self.root.state('zoomed')
            self.root.update()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            geometry = str(width) + 'x' + str(height)
        self.root.geometry(geometry)
        self.frame = tk.LabelFrame(self.root, bg='#F0F0F0', text=None, font=('仿宋', 12), height=height, width=width)
        self.frame.grid(row=0, column=0, columnspan=3)
        self.frame.grid_propagate(0)

    def maintain(self):
        """
        method: 保持该主页面, 即window的.mainloop()方法
        :return: 无
        """
        self.root.mainloop()

    def destroy(self):
        """
        method: 删除自己
        :return: 无
        """
        self.root.destroy()


class EditPage:
    """
    class: 用作显示数据并可编辑数据的页面
    """
    def __init__(self,
                 data,
                 func_save=None):
        """
        method: 编辑窗口
        :param data:
        :param func_save
        """
        self.data = None
        self.page = NormalPage(title='Edit',
                               width=300,
                               height=500)
        self.edit = DataEdit(self.page.frame,
                             data=data,
                             func_save=func_save)

    def command(self,
                func_save):
        """
        method: 配置保存按键回调函数
        :param func_save:
        :return:
        """
        self.edit.command(func_save=func_save)

    def maintain(self):
        """
        method: 窗口保持
        :return:
        """
        self.page.maintain()


class RightClickMenu:
    """
    class: 右键弹出窗口
    """
    def __init__(self,
                 master,
                 x,
                 y,
                 label_func=None):
        """
        method: 右键弹出窗口
        :param master: 窗口所在的master，可以是frame或canvas
        :param x:
        :param y:
        :param label_func:
        """


class ButtonsArea:
    """
    class: 创建一个放置若干按钮的区域
    """
    def __init__(self,
                 pframe=None,
                 row=0,
                 column=0,
                 wdg_width=None,
                 wdg_height=None,
                 btn_lst=None,
                 btn_width=None,
                 btn_height=None,
                 num_per_row=3):
        """
        method: 创建一个区域，放置一系列的正方形按钮
        :param pframe: 父Frame
        :param row: grid()的row
        :param column: grid()的column
        :param wdg_width: 控件的width，缺省时，与父Frame对象的width相等
        :param wdg_height: 控件的height，缺省时，与父Frame对象的height相等
        :param btn_lst: 按钮列表
        :param btn_width: 按钮宽度
        :param btn_height: 按钮高度
        :param num_per_row: 每行的按钮数
        """
        # 获取父Frame对象
        self.pframe = pframe

        # 获取父Frame的width和height
        self.pframe.update()
        pfrm_width = self.pframe.winfo_width()
        pfrm_height = self.pframe.winfo_height()

        # 获取底层Frame的width和height
        if wdg_width is None or wdg_width > pfrm_width:
            wdg_width = pfrm_width
        if wdg_height is None or wdg_height > pfrm_height:
            wdg_height = pfrm_height - 5

        # 创建底层Frame
        self.bframe = tk.Frame(master=pframe, height=wdg_height, width=wdg_width)
        self.bframe.grid(row=row, column=column)
        self.bframe.grid_propagate(0)

        # 按钮列表和按钮对象列表
        if btn_lst is None:
            self.btn_lst = ['示例按钮']
        else:
            self.btn_lst = btn_lst
        self.btn_obj = {}

        """开始"""
        for idx, btn in enumerate(btn_lst):
            btn_obj = ttk.Button(master=self.bframe, text=btn, width=btn_width[idx])
            btn_obj.grid(row=int(idx/num_per_row), column=int(idx) % num_per_row)
            self.btn_obj[btn] = btn_obj

    def command(self,
                btn_nm='示例按钮',
                cal_func=None):
        """
        method: 设置button回调函数
        :param btn_nm: 按钮名称, str
        :param cal_func: 回调函数名
        :return: 无
        """
        if btn_nm in self.btn_lst:
            self.btn_obj[btn_nm].config(command=cal_func)

    def disable(self,
                btn_lst=None):
        """
        method:
        :param btn_lst:
        :return:
        """
        if btn_lst is None:
            btn_lst = self.btn_lst
        for btn_nm in btn_lst:
            self.btn_obj[btn_nm].config(state=tk.DISABLED)

    def enable(self,
               btn_lst=None):
        """
        method:
        :param btn_lst:
        :return:
        """
        if btn_lst is None:
            btn_lst = self.btn_lst
        for btn_nm in btn_lst:
            self.btn_obj[btn_nm].config(state=tk.NORMAL)

    def destroy(self):
        """
        method: 删除自己
        """
        self.bframe.destroy()


class DataEdit:
    """
    class: 数据显示和编辑编辑控件，包括一个2列的表格(左列为名称右列为值)
    """
    def __init__(self,
                 pframe=None,
                 row=0,
                 column=0,
                 wdg_width=None,
                 wdg_height=None,
                 func_save=None,
                 data=None):
        """
        method: 构造InfoDisp对象的基本框架，包括一个空白的表格区域和3个按键
        :param pframe: 父Frame对象，放置该控件组合
        :param row: 该控件组合在pframe上grid()的row
        :param column: 该控件组合在pframe上grid()的column
        :param wdg_width: 控件的width，缺省时，与父Frame对象的width相等
        :param wdg_height: 控件的height，缺省时，与父Frame对象的height相等
        :param func_save: "保存"按键回调函数
        :param data: 显示的数据，dict
        """
        # 获取父Frame对象
        self.pframe = pframe

        # 获取父Frame的width和height
        self.pframe.update()
        pfrm_width = self.pframe.winfo_width()
        pfrm_height = self.pframe.winfo_height()

        # 获取本控件组合的基层Frame的width和height
        if wdg_width is None or wdg_width > pfrm_width:
            wdg_width = pfrm_width
        if wdg_height is None or wdg_height > pfrm_height:
            wdg_height = pfrm_height

        # 创建基层Frame
        self.frame = tk.LabelFrame(master=pframe, height=wdg_height, width=wdg_width)
        self.frame.grid(row=row, column=column)
        self.frame.grid_propagate(0)

        # 表格框架和按钮框架尺寸
        tbl_frm_width = wdg_width - 5
        btn_frm_heigh = 30
        tbl_frm_height = wdg_height - 20 - btn_frm_heigh

        # 创建表格框架
        self.table_frm = tk.Frame(master=self.frame, height=tbl_frm_height, width=tbl_frm_width)
        self.table_frm.grid(row=0, column=0)
        self.table_frm.grid_propagate(0)

        # 创建按钮框架
        self.btn_frm = tk.Frame(master=self.frame, height=btn_frm_heigh, width=tbl_frm_width)
        self.btn_frm.grid(row=1, column=0)
        self.btn_frm.grid_propagate(0)

        # 表格单列宽度
        self.tab_col_width = ceil(tbl_frm_width / 16)
        # 按键宽度
        self.btn_width = floor(tbl_frm_width / 24) - 1

        # 创建按键（编辑、保存、返回）
        self.btn_save = tk.Button(self.btn_frm, text='Save', width=self.btn_width, font=('楷体', 12))
        self.btn_save.grid(row=0, column=0)
        self.btn_save.config(command=self.save_data)

        """对象变量创建"""
        # 表格的两列分别由不同的控件组成，"名称"一列是由Label组成， "值"一列是由Entry组成
        # 使用两个dict变量分别记录这两列的控件，分别操作
        self.table_nm = {}
        self.table_vl = {}
        # Entry变量
        self.entry_var = {}
        # btn_save回调函数
        self.func_save = func_save

        # 读取数据
        self.data = {}

        # 显示数据
        self.disp_data(data)

    def disp_data(self,
                  data):
        """
        method: 编辑数据
        :param data: 数据，dict
        """
        # 如果info_data不为空，则显示其内容
        if data is not None:
            for idx, key in enumerate(data):
                if key == 'id' or key == 'crd_x' or key == 'crd_y' or key == 'angle' or key == 'node1' or key == \
                        'node2' or key == 'vol_dir' or key == 'cur_dir':
                    continue
                self.table_nm[key] = tk.Label(self.table_frm, text=key, width=self.tab_col_width,
                                              relief=tk.RIDGE, bd=1)
                if data[key] is True:
                    self.entry_var[key] = tk.StringVar(value='True')
                elif data[key] is False:
                    self.entry_var[key] = tk.StringVar(value='False')
                elif type(data[key]) == float:
                    self.entry_var[key] = tk.DoubleVar(value=data[key])
                elif type(data[key]) == int:
                    self.entry_var[key] = tk.IntVar(value=data[key])
                else:
                    self.entry_var[key] = tk.StringVar(value=data[key])

                self.table_vl[key] = tk.Entry(self.table_frm,
                                              width=self.tab_col_width - 3,
                                              textvariable=self.entry_var[key])

                self.table_nm[key].grid(row=idx, column=0)
                self.table_nm[key].grid_propagate(0)
                self.table_vl[key].grid(row=idx, column=1)
                self.table_vl[key].grid_propagate(0)

    def save_data(self):
        """
        method: 保存数据, 随后显示数据
        """
        for key in self.entry_var:
            self.data[key] = self.entry_var[key].get()
        if self.func_save:
            self.func_save()

    def command(self,
                func_save):
        """
        method: 配置保存按键回调函数
        :param func_save:
        :return:
        """
        self.func_save = func_save


class ScrollCanvas:
    """
    class: 带有Scrollbar的Canvas, 称为ScrollCanvas控件。
    该ScrollCanvas可被放置在tkinter.Frame控件(赋值给pFrame参数)上，当ScrollCanvas控件的外观尺寸小于Canvas的实际尺寸时，出现
    Scrollbar，否则，没有Scrollbar。
    [内部结构]: 先创建一个底层Frame作为底，在该底层Frame上放置Canvas和Scrollbar，关联后两者。
    """
    def __init__(self,
                 pframe=None,
                 row=0,
                 column=0,
                 wdg_width=None,
                 wdg_height=None,
                 cav_width=None,
                 cav_height=None,
                 grid=None):
        """
        method: 创建一个ScrollCanvas
        :param pframe: 放置该ScrollCanvas的父Frame对象
        :param row: 底层Frame对象grid()中的row
        :param column: 底层Frame对象grid()中的column
        :param wdg_width: ScrollCanvas控件的width，缺省时，与父Frame对象的width相等
        :param wdg_height: ScrollCanvas控件的height，缺省时，与父Frame对象的height相等
        :param cav_width: Canvas对象的width
        :param cav_height: Canvas对象的height
        :param grid: 是否有网格
        """
        """variables confirm"""
        # 确定self.__pframe
        self.__pframe = pframe

        # 获取父frame的width和height
        self.__pframe.update()
        pfrm_width = self.__pframe.winfo_width()
        pfrm_height = self.__pframe.winfo_height()

        # 获取底层Frame的width和height
        if wdg_width is None:
            wdg_width = pfrm_width - 10
        if wdg_height is None:
            wdg_height = pfrm_height - 25

        # 确定self.__scrollregion
        if cav_width is None:
            cav_width = wdg_width
        if cav_height is None:
            cav_height = wdg_height
        self.__cav_width = cav_width
        self.__cav_height = cav_height
        self.__scrollregion = (0, 0, cav_width, cav_height)

        """main process"""
        # 创建底层Frame
        self.__frame = tk.Frame(self.__pframe, width=wdg_width, height=wdg_height)
        self.__frame.grid(row=row, column=column)
        # create 1 canvas and 2 scrollbar on the frame
        self.canvas = tk.Canvas(self.__frame, width=wdg_width, height=wdg_height,
                                scrollregion=self.__scrollregion, bg='white')
        self.canvas.grid(row=0, column=0)
        if cav_width > wdg_width:
            self.canvas.config(width=wdg_width - 20)
            x_sbar = tk.Scrollbar(self.__frame, orient=tk.HORIZONTAL, width=20)
            self.canvas.config(xscrollcommand=x_sbar.set)
            x_sbar.config(command=self.canvas.xview)
            x_sbar.grid(row=1, column=0, sticky=tk.EW)
        if cav_height > wdg_height:
            self.canvas.config(height=wdg_height - 20)
            y_sbar = tk.Scrollbar(self.__frame, orient=tk.VERTICAL, width=20)
            self.canvas.config(yscrollcommand=y_sbar.set)
            y_sbar.config(command=self.canvas.yview)
            y_sbar.grid(row=0, column=1, sticky=tk.NS)

        # 绘制网格
        self.creat_grid(grid=grid)

        # 鼠标滚轮事件回调函数
        def mouse_wheel(event):
            a = int(-event.delta / 60)
            self.canvas.yview_scroll(a, 'units')

        # shift+鼠标滚轮事件回调函数
        def shift_mouse_wheel(event):
            a = int(-event.delta / 60)
            self.canvas.xview_scroll(a, 'units')

        self.canvas.bind("<MouseWheel>", mouse_wheel, add='+')
        self.canvas.bind("<Shift-MouseWheel>", shift_mouse_wheel, add='+')

    def creat_grid(self,
                   grid=None):
        """
        method: 绘制网格
        :param grid: 网格参数，None: 无网格，任意自然数：网格大小
        :return: 无
        """
        if grid:
            for i in range(1, int(self.__cav_width/grid)):
                for j in range(1, int(self.__cav_height / grid)):
                    self.canvas.create_oval(i*grid-1, j*grid-1, i*grid+1, j*grid+1, width=1, outline='#0696F7')

    def destroy(self):
        """
        method: 清除
        :return:
        """
        self.__frame.destroy()


class ScrollFrame(ScrollCanvas):
    """
    class: 带有Scrollbar的Frame, 继承自class ScrollCanvas, 在其Canvas上创建了一个Frame
    创建一个有Scrollbar的Frame，该ScrollFrame放置在其父Frame上，当该ScrollFrame的尺寸大于父Frame时，出现Scrollbar，否则
    ，没有Scrollbar
    [详细]：参见class ScrollCanvas。
    """
    def __init__(self,
                 pframe=None,
                 row=0,
                 column=0,
                 wdg_width=None,
                 wdg_height=None,
                 frm_width=None,
                 frm_height=None):
        """
        method: 创建一个ScrollFrame
        :param row: 放置该ScrollCanvas的父Frame对象
        :param row: 底层Frame对象grid()中的row
        :param column: 底层Frame对象grid()中的column
        :param wdg_width: ScrollCanvas控件的width，缺省时，与父Frame对象的width相等
        :param wdg_height: ScrollCanvas控件的height，缺省时，与父Frame对象的height相等
        :param frm_width: Frame对象的width
        :param frm_height: Frame对象的height
        """
        scroll_canvas = super().__init__(pframe=pframe,
                                         row=row,
                                         column=column,
                                         wdg_width=wdg_width,
                                         wdg_height=wdg_height,
                                         cav_width=frm_width,
                                         cav_height=frm_height).canvas
        win = scroll_canvas.create_window()
        self.frame = tk.Frame(win,
                              width=frm_width,
                              height=frm_height)


class Contents:
    """
    class: 目录显示控件
    树状显示目录结构
    [详细]：先创建一个底层Frame作为底，在该底层Frame上放置ttk.TreeView对象，显示内容。
    """
    def __init__(self,
                 pframe=None,
                 row=0,
                 column=0,
                 wdg_width=None,
                 wdg_height=None,
                 cont_data=None,
                 open_flag=None):
        """
        构造方法：创建一个显示目录
        :param pframe: 父Frame, tkinter.Frame
        :param row: grid()的row, int
        :param column: grid()的column, int
        :param wdg_width: 控件的width，缺省时，与父Frame对象的width相等, int
        :param wdg_height: 控件的height，缺省时，与父Frame对象的height相等, int
        :param cont_data: 目录数据, pandas.DataFrame
        :param open_flag: 折叠标志，列表的每个元素对应cont_data的一个列，False表示折叠，True表示打开，
        list([False, True, ...])
        """
        """变量传递"""
        self.pframe = pframe
        if cont_data is not None:
            # 由于TreeView显示的顺序和DataFrame数据中的排序相反，故先降序排列
            self.cont_data = cont_data.sort_index(ascending=False)
        else:
            self.cont_data = pd.DataFrame({'一级': ['一级1', '一级1', '一级1', '一级1', '一级1', '一级1'],
                                           '二级': ['二级1', '二级1', '二级1', '二级1', '二级1', '二级1'],
                                           '三级': ['三级1', '三级1', '三级1', '三级1', '三级2', '三级2'],
                                           '四级': ['四级1', '四级1', '四级2', '四级2', '四级3', '四级3'],
                                           '五级': ['五级1', '五级2', '五级3', '五级4', '五级5', '五级5']})
        self.cont_data.sort_values(by=list(self.cont_data.keys()))
        # 折叠标志处理
        if open_flag is None:
            open_flag = []
            length = len(self.cont_data.keys())
            for i in range(length):
                if i == length-2:
                    open_flag.append(False)
                else:
                    open_flag.append(True)

        """变量定义"""
        self.work_area = None

        # 获取父Frame的width和height
        self.pframe.update()
        pfrm_width = self.pframe.winfo_width()
        pfrm_height = self.pframe.winfo_height()

        # 获取底层Frame的width和height
        if wdg_width is None or wdg_width > pfrm_width - 10:
            wdg_width = pfrm_width - 10
        if wdg_height is None or wdg_height > pfrm_height - 20:
            wdg_wheight = pfrm_height - 20

        # 创建底层Frame
        self.frame = tk.LabelFrame(self.pframe, width=wdg_width, height=wdg_height, font=('仿宋', 12), text='电路目录')
        self.frame.grid(row=row, column=column)
        self.frame.grid_propagate(0)

        # 读取变电站列表并显示列表名称
        self.tree = ttk.Treeview(master=self.frame, show='tree')
        self.tree.column('#0', width=wdg_width-10)
        self.tree.grid(row=row, column=column)

        tree_list = {}
        for col in self.cont_data.columns:
            tree_list[col] = []

        for idx in self.cont_data.index:
            name = ''
            for i, col in enumerate(self.cont_data.columns):
                parent_name = name
                name = self.cont_data.loc[idx, col]
                if name not in tree_list[col]:
                    tree_list[col].append(name)
                    self.tree.insert(parent=parent_name, index=0, iid=name, text=name, open=open_flag[i])

    def command(self,
                cal_func=None):
        """
        method: 命令回调函数定义
        :param cal_func: 回调函数，选中目录中的某个项目时，执行该函数
        """
        def treeslct_func(event):
            tree_focus = self.tree.focus()
            cal_func(tree_focus)

        # 选中Tree的某个item后的response
        if cal_func is not None:
            self.tree.bind(sequence='<<TreeviewSelect>>', func=treeslct_func)
        else:
            self.tree.unbind(sequence='<<TreeviewSelect>>')

    def destroy(self):
        """
        method: 删除该控件
        """
        self.frame.destroy()


class MenuArea:
    """
    class: 菜单区域
    """
    def __init__(self,
                 pframe=None,
                 row=0,
                 column=0,
                 menu_cont=None,
                 cal_func=None):
        """
        method: 创建一个菜单区域，包括若干菜单
        :param pframe: 父Frame控件, tkinter.Frame
        :param menu_cont: 菜单内容, dict({'菜单1': list(['子菜单1', '子菜单2', ...]),
        '菜单2': list(['子菜单1', '子菜单2', ...])})
        :param cal_func: 回调函数, dict({'子菜单1': cal_func1, '子菜单2': cal_func2, ...})
        """
        # 在父Frame上创建底层Frame
        self.bframe = tk.Frame(pframe, width=200, height=100, relief=tk.RAISED, bg='green')
        self.bframe.grid(row=row, column=column)
        # 菜单内容
        self.menu_cont = menu_cont
        # 回调函数
        if cal_func is None:
            cal_func = {}

        menu_obj = {}

        if self.menu_cont:
            for i, menu_nm in enumerate(self.menu_cont):
                menu_btn = tk.Menubutton(self.bframe, text=menu_nm, underline=0)
                menu_btn.grid(row=0, column=i)
                menu_obj[menu_nm] = tk.Menu(menu_btn, tearoff=0)
                menu_btn.config(menu=menu_obj[menu_nm])
                for j, sub_menu_nm in enumerate(self.menu_cont[menu_nm]):
                    if sub_menu_nm in cal_func.keys():
                        menu_obj[menu_nm].add_command(label=sub_menu_nm, command=cal_func[sub_menu_nm], underline=0)

                    else:
                        menu_obj[menu_nm].add_command(label=sub_menu_nm, command=None, underline=0)


if __name__ == '__main__':
    new_win = tk.Tk()

