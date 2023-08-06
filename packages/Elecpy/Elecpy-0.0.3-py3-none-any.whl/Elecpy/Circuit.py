"""
该模块用来管理电路，主要包括以下几个类：
1. 电路
2. 元件图
3. 电路图
"""
from Elecpy.Diagram import *
from Elecpy.GUIElements import *
from Elecpy.Analysis import *
from Elecpy.Default import *
import copy
import tkinter.font as tkFont
from Elecpy.File import *
from Elecpy.Backup import *


class Element:
    """
    class: 元素，即电路图上最基本的部分
    """
    def __init__(self,
                 default_data=None,
                 source_data=None):
        """
        method:
        :param default_data: 默认数据
        :param source_data: 源数据，dict数据
        """
        """源数据"""
        # 创建默认数据
        if default_data is None:
            self.default_data = {'id': '', 'designator': '', 'crd_x': 0, 'crd_y': 0, 'angle': 0, 'visible': True}
        else:
            self.default_data = copy.deepcopy(default_data)
        # 如果给定数据
        if source_data:
            self.source_data = source_data
            for key in self.default_data:
                if key not in self.source_data.keys():
                    self.source_data[key] = self.default_data[key]
        # 如果没有给定数据，则创建一个默认数据
        else:
            self.source_data = self.default_data
        # 元素的外框(宽, 高)
        self.square = [0, 0]
        # 画布
        self.canvas = None
        # 选择情况
        self.slct = None
        # 右键菜单
        self.rt_menu = None
        # 编辑窗口
        self.edit_win = None

    def edit(self,
             **data):
        """
        method: 数据
        :param data:
        :return:
        """
        for key in data:
            if key in self.default_data.keys():
                self.source_data[key] = data[key]

    def get_data(self,
                 data=None):
        """
        method:
        :param data:
        :return:
        """
        # 如果data为空，返回self.__source_data
        if data is None:
            return self.source_data
        # 如果data不为空，则返回data指定的数据
        else:
            if data in self.source_data.keys():
                return self.source_data[data]
            else:
                print('This data is not exist!')
                return None

    def display(self,
                canvas=None,
                crd_x=None,
                crd_y=None,
                angle=None):
        """
        method: 显示图形，可以是线条，也可以是图片
        :return:
        :param canvas:
        :param crd_x:
        :param crd_y:
        :param angle:
        """
        if canvas:
            self.canvas = canvas
        if crd_x is None and 'crd_x' in self.source_data.keys():
            crd_x = self.source_data['crd_x']
        if crd_y is None and 'crd_x' in self.source_data.keys():
            crd_y = self.source_data['crd_y']
        if angle is None and 'crd_x' in self.source_data.keys():
            angle = self.source_data['angle']
        # 如果存在self.canvas，清理之前绘制的文本
        if self.canvas:
            self.clear()
        return crd_x, crd_y, angle

    def move(self,
             to_crd):
        """
        method: 移动
        :param to_crd: 目标位置
        :return:
        """
        x_bias = to_crd[0] - self.source_data['crd_x']
        y_bias = to_crd[1] - self.source_data['crd_y']
        self.source_data['crd_x'] = to_crd[0]
        self.source_data['crd_y'] = to_crd[1]
        self.canvas.move(self.source_data['id'], x_bias, y_bias)

    def rotate(self):
        """
        method: 顺时针选择90度
        :return:
        """
        self.source_data['angle'] += 90
        self.display()

    def clear(self):
        """
        method: 删除之前的显示，
        :return:
        """
        # 如果self.canvas存在
        if self.canvas:
            self.canvas.delete(self.source_data['id'])

    def select(self, crd):
        """
        method: 判断选择
        :param crd: 点坐标
        :return:
        """
        # 判断元素是否被选中
        if abs(crd[0] - int(self.source_data['crd_x'])) < self.square[0] / 2 and \
                abs(crd[1] - int(self.source_data['crd_y'])) < self.square[1] / 2:
            self.slct = True
        else:
            self.slct = False
        self.display()
        return self.slct

    def edit_window(self,
                    save_func=None):
        """
        method: 编辑窗口
        :param save_func: 保存按键的回调函数
        :return:
        """
        EditPage(self.edit_win.frame, func_save=save_func)


class Text(Element):
    """
    class: 文本
    """

    def __init__(self,
                 text_data=None):
        """
        method: 创建一个文本
        :param text_data: 文本数据
        """
        super().__init__(default_data=dft_text_data,
                         source_data=text_data)
        self.square = self.__get_square()

    def edit(self,
             **text_data):
        """
        method: 编辑文本，如果text_data为空，则不做任何编辑
        :param text_data: 文本参数，如text_id, master_id, content等
        """
        super().edit(**text_data)
        self.square = self.__get_square()

    def __get_square(self):
        """
        method: 获取文本的外轮廓
        :return:
        """
        # 判断文本外轮廓的尺寸
        text_width = 0
        if '\n' not in self.source_data['content']:
            text_width = len(self.source_data['content'])
        else:
            for text in self.source_data['content'].split('\n'):
                if text_width < len(text):
                    text_width = len(text)
        return text_width * int(self.source_data['font_size']), (self.source_data['content'].count('\n') + 1) * \
               int(self.source_data['font_size'])

    def display(self,
                canvas=None,
                crd_x=None,
                crd_y=None,
                angle=None):
        """
        method: 显示文本
        :param canvas: 画布
        :param crd_x: 给定的文本x坐标, 缺省时，按self.text_data['crd_x']绘制
        :param crd_y: 给定的文本y坐标, 缺省时，按self.text_data['crd_y']绘制
        :param angle: 角度
        :return:
        """
        crd_x, crd_y, angle = super().display(canvas,
                                              crd_x,
                                              crd_y,
                                              angle, )
        if self.source_data['visible']:
            """绘制文本"""
            # 根据文本是否被选择决定文本颜色
            if self.slct:
                lcolor = 'blue'
            else:
                lcolor = 'black'
            # 如果有给定坐标，按给定值显示文本
            font = tkFont.Font(family=self.source_data['font_family'],
                               size=self.source_data['font_size'],
                               weight=self.source_data['font_weight'],
                               slant=self.source_data['font_slant'],
                               underline=self.source_data['font_underline'],
                               overstrike=self.source_data['font_overstrike'])

            self.canvas.create_text(crd_x,
                                    crd_y,
                                    text=self.source_data['content'],
                                    font=font,
                                    tag=self.source_data['id'],
                                    fill=lcolor,
                                    activefill='blue')


class Part(Element):
    """
    class: 元件本身
    """

    def __init__(self,
                 part_nm,
                 part_data=None):
        """
        method:
        :return:
        """
        super().__init__(default_data=dft_comps_data[part_nm],
                         source_data=part_data)
        self.tmnls_vol = None
        self.max_vol = None
        self.tmnls_crd = None
        # 电压方向
        self.vol_dir = True
        # 电流方向
        self.cur_dir = True

    def display(self,
                canvas=None,
                crd_x=None,
                crd_y=None,
                angle=None,
                bias_x=None,
                bias_y=None):
        """
        method:
        :return:
        """
        crd_x, crd_y, angle = super().display(canvas,
                                              crd_x,
                                              crd_y,
                                              angle)
        """绘制元件"""
        # 绘制元件本身
        if self.source_data['id'].split('-')[0] == 'resistor':
            comp_data = draw_resistor_rect(id=self.source_data['id'],
                                           cnt_crd=(crd_x, crd_y),
                                           angle=angle,
                                           canvas=self.canvas,
                                           slct=self.slct,
                                           tmnls_vol=self.tmnls_vol,
                                           max_vol=self.max_vol)
            self.square = comp_data['square']
            self.tmnls_crd = comp_data['tmnls_crd']
        elif self.source_data['id'].split('-')[0] == 'capacitor':
            comp_data = draw_capacitor(id=self.source_data['id'],
                                       cnt_crd=(crd_x, crd_y),
                                       angle=angle,
                                       canvas=self.canvas,
                                       slct=self.slct,
                                       tmnls_vol=self.tmnls_vol,
                                       max_vol=self.max_vol)
            self.square = comp_data['square']
            self.tmnls_crd = comp_data['tmnls_crd']
        elif self.source_data['id'].split('-')[0] == 'inductor':
            comp_data = draw_inductor(id=self.source_data['id'],
                                      cnt_crd=(crd_x, crd_y),
                                      angle=angle,
                                      canvas=self.canvas,
                                      slct=self.slct,
                                      tmnls_vol=self.tmnls_vol,
                                      max_vol=self.max_vol)
            self.square = comp_data['square']
            self.tmnls_crd = comp_data['tmnls_crd']
        elif self.source_data['id'].split('-')[0] == 'voltage_dc':
            comp_data = draw_source_dc(id=self.source_data['id'],
                                       cnt_crd=(crd_x, crd_y),
                                       angle=angle,
                                       canvas=self.canvas,
                                       slct=self.slct,
                                       tmnls_vol=self.tmnls_vol,
                                       max_vol=self.max_vol)
            self.square = comp_data['square']
            self.tmnls_crd = comp_data['tmnls_crd']
        elif self.source_data['id'].split('-')[0] == 'voltage_ac':
            comp_data = draw_source_ac(id=self.source_data['id'],
                                       cnt_crd=(crd_x, crd_y),
                                       angle=angle,
                                       canvas=self.canvas,
                                       slct=self.slct,
                                       tmnls_vol=self.tmnls_vol,
                                       max_vol=self.max_vol)
            self.square = comp_data['square']
            self.tmnls_crd = comp_data['tmnls_crd']
        elif self.source_data['id'].split('-')[0] == 'current_dc':
            comp_data = draw_source_dc(id=self.source_data['id'],
                                       cnt_crd=(crd_x, crd_y),
                                       angle=angle,
                                       canvas=self.canvas,
                                       slct=self.slct,
                                       tmnls_vol=self.tmnls_vol,
                                       max_vol=self.max_vol)
            self.square = comp_data['square']
            self.tmnls_crd = comp_data['tmnls_crd']
        elif self.source_data['id'].split('-')[0] == 'current_ac':
            comp_data = draw_source_ac(id=self.source_data['id'],
                                       cnt_crd=(crd_x, crd_y),
                                       angle=angle,
                                       canvas=self.canvas,
                                       slct=self.slct,
                                       tmnls_vol=self.tmnls_vol,
                                       max_vol=self.max_vol)
            self.square = comp_data['square']
            self.tmnls_crd = comp_data['tmnls_crd']
        elif self.source_data['id'].split('-')[0] == 'diode':
            comp_data = draw_diode(id=self.source_data['id'],
                                   cnt_crd=(crd_x, crd_y),
                                   angle=angle,
                                   canvas=self.canvas,
                                   slct=self.slct,
                                   tmnls_vol=self.tmnls_vol,
                                   max_vol=self.max_vol)
            self.square = comp_data['square']
            self.tmnls_crd = comp_data['tmnls_crd']
        elif self.source_data['id'].split('-')[0] == 'switch':
            comp_data = draw_switch(id=self.source_data['id'],
                                    cnt_crd=(crd_x, crd_y),
                                    angle=angle,
                                    canvas=self.canvas,
                                    slct=self.slct,
                                    tmnls_vol=self.tmnls_vol,
                                    max_vol=self.max_vol)
            self.square = comp_data['square']
            self.tmnls_crd = comp_data['tmnls_crd']
        elif self.source_data['id'].split('-')[0] == 'ground':
            comp_data = draw_ground(id=self.source_data['id'],
                                    cnt_crd=(crd_x, crd_y),
                                    angle=angle,
                                    canvas=self.canvas,
                                    slct=self.slct)
            self.square = comp_data['square']
            self.tmnls_crd = comp_data['tmnls_crd']
        else:
            raise TypeError('Unknown comp_nm(component name)！！')

        # 绘制端子的圆圈
        draw_tmnl_circle(self.source_data['id'], self.tmnls_crd, canvas=self.canvas)

    def move(self,
             to_crd):
        """
        method: 将元件移动至坐标to_crd
        :param to_crd:
        :return:
        """
        # 调用父类的move
        super().move(to_crd)
        # 元件移动后，需要显示一次，从而将.tmnls_crd刷新一次
        self.display()

    def get_valfomula_str(self):
        """
        method: 获取元件值的公式表达的字符串，如100*sin(50*2*pi*t+20)
        :return:
        """
        part_data = self.get_data()
        if part_data['id'].split('-')[0] == 'resistor':
            multi, value = get_multi_value(part_data['value'])
            return str(value) + str(multi) + 'Ω'
        elif part_data['id'].split('-')[0] == 'capacitor':
            multi, value = get_multi_value(part_data['value'])
            return str(value) + str(multi) + 'F'
        elif part_data['id'].split('-')[0] == 'inductor':
            multi, value = get_multi_value(part_data['value'])
            return str(value) + str(multi) + 'H'
        elif part_data['id'].split('-')[0] == 'voltage_dc':
            multi, value = get_multi_value(part_data['amp'])
            return str(value) + str(multi) + 'V'
        elif part_data['id'].split('-')[0] == 'current_dc':
            multi, value = get_multi_value(part_data['amp'])
            return str(value) + str(multi) + 'A'
        elif part_data['id'].split('-')[0] == 'voltage_ac':
            return str(part_data['amp']) + '*sin(' + str(part_data['freq']) + '*pi*t+' + str(part_data['phase']) + ') V'
        elif part_data['id'].split('-')[0] == 'current_ac':
            return str(part_data['amp']) + '*sin(' + str(part_data['freq']) + '*pi*t+' + str(part_data['phase']) + ') A'
        else:
            return ''

    def tmnl_select(self,
                    crd):
        """
        method: 判断元件端子是否被点(crd)选择，如果被选择，读取端子号，如果未选择，返回False
        :param crd: 点(x, y)坐标
        :return: 选中: 端子号(1, 2,..), 未选中: False
        """
        # 点捕获
        crd = point_capture(crd)
        # 判断端子是否被捕获，如果被捕获，读取端子号，如果未捕获，返回False
        tmnl_slct = False
        for i, tmnl_crd in enumerate(self.tmnls_crd):
            if crd == tmnl_crd:
                tmnl_slct = str(i + 1)
        return tmnl_slct

    def get_tmnl_crd(self,
                     tmnl):
        """
        method: 获取元件端子的绝对坐标
        :param tmnl: 端子号，1, 2,...
        :return: tmnl为1, 2,...时，返回端子号指定的坐标
        """
        return self.tmnls_crd[int(tmnl) - 1]

    def get_tmnl_net(self,
                     tmnl):
        """
        method: 获取端子网络id
        :param tmnl: 端子号, int
        """
        return self.source_data['node' + str(tmnl)]


class Wire(Element):
    """
    class: 导线本身
    """

    def __init__(self,
                 wire_data=None,
                 comp_objs=None):
        """
        method: 创建一个Wire对象
        :param wire_data:
        :param comp_objs:
        """
        super().__init__(default_data=dft_wire_data,
                         source_data=wire_data)

        # 元件对象，用于实现元件移动和旋转时，导线跟随的效果，dict{'comp_id1': Component, ..}
        self.comp_objs = comp_objs
        # 导线电压
        self.wire_vol = '0V'
        # 导线电流
        self.wire_cur = '0A'

        if wire_data is None:
            print('The wire is empty!! Call method .draw() to draw one!!')

    def tmnl_select(self,
                    crd):
        """
        method: 判断元件端子被选中
        :param crd: 坐标
        :return: comp_id, tmnl
        """
        for key in self.comp_objs:
            tmnl = self.comp_objs[key].tmnl_select(crd)
            if tmnl:
                return key, tmnl

    def display(self,
                canvas=None,
                crd_x=None,
                crd_y=None,
                comp_objs=None,
                bias_x=None,
                bias_y=None):
        """
        method: 显示导线
        :param canvas: 画布
        :param crd_x:
        :param crd_y:
        :param comp_objs: 元件对象字典, dict{'comp_id1': Component, ...}，用于实现元件移动旋转时导线跟随功能
        :param bias_x:
        :param bias_y:
        """
        super().display(canvas)
        if comp_objs:
            self.comp_objs = comp_objs
        # 获取导线的起点、中间点和终点的坐标
        line_pcrds = self.get_sta_tmnl_crd()
        line_pcrds += self.__get_mid_pcrds()
        line_pcrds += self.get_end_tmnl_crd()
        # 获取导线的线条粗细和颜色
        if self.slct:
            color = 'blue'
            width = 4
        else:
            color = 'black'
            width = 2

        """绘制导线"""
        # 显示导线本身
        self.canvas.create_line(line_pcrds, tags=self.source_data['id'], fill=color, width=width, activewidth=4,
                                activefill='blue')

    def __get_sta_comp_obj(self):
        """
        method: 获取导线起点端子对应的元件对象，返回Component对象
        :return: 导线起点端子对应的元件对象，Component对象
        """
        return self.comp_objs[self.source_data['sta_comp']]

    def __get_end_comp_obj(self):
        """
        method: 获取导线终点端子对应的元件对象，返回Component对象
        :return: 导线终点端子对应的元件对象，Component对象
        """
        return self.comp_objs[self.source_data['end_comp']]

    def get_sta_tmnl_crd(self):
        """
        method: 获取起点的坐标，tuple(x, y)
        :return: 起点坐标，tuple(x, y)
        """
        return self.__get_sta_comp_obj().get_tmnl_crd(self.source_data['sta_tmnl'])

    def get_end_tmnl_crd(self):
        """
        method: 获取终点的坐标，tuple(x, y)
        :return: 终点坐标，tuple(x, y)
        """
        return self.__get_end_comp_obj().get_tmnl_crd(self.source_data['end_tmnl'])

    def __get_mid_pcrds(self):
        """
        mdthod: 获取中间点的坐标, tuple(x1, y1, x2, y2, ...)
        :return: 中间点坐标序列, tuple(x1, y1, x2, y2, ...)
        """
        line_pcrds = ()
        i = 1
        x = 0
        for key in self.source_data.keys():
            if key == 'mid_p' + str(i) + '_x':
                x = int(self.source_data[key])
            elif key == 'mid_p' + str(i) + '_y':
                y = int(self.source_data[key])
                line_pcrds += (x, y)
                i += 1
        return line_pcrds

    def select(self, crd=None):
        """
        method: 判断导线本身（不包含其文本部分）是否被点crd=(x, y)选中, 如果选中导线，则self.__slct = True，并返回True
        若未选中导线，则self.__slct=False，并返回False；若选中状态发生变化，则刷新一次显示
        :param crd: 点坐标(x, y)
        :return: 选中: True, 未选中: False
        """
        # 记录起点坐标sta_crd、中间点和终点坐标的列表crd_lst
        sta_crd = self.get_sta_tmnl_crd()
        crd_lst = self.__get_mid_pcrds() + self.get_end_tmnl_crd()
        # 按每条线段进行逐个判别
        self.slct = None
        for i in range(0, int(len(crd_lst) / 2)):
            x0 = sta_crd[0]
            y0 = sta_crd[1]
            x1 = crd_lst[i * 2]
            y1 = crd_lst[i * 2 + 1]
            if y0 == y1:
                if max(x0, x1) >= crd[0] >= min(x0, x1) and y0 + 2 >= crd[1] >= y0 - 2:
                    self.slct = True
                    break
            elif x0 == x1:
                if max(y0, y1) >= crd[1] >= min(y0, y1) and x0 + 2 >= crd[0] >= x0 - 2:
                    self.slct = True
                    break
            else:
                a = (x1 - x0) / (y0 - y1)
                b = (x0 * y1 - x1 * y0) / (y0 - y1)
                if max(x0, x1) >= crd[0] >= min(x0, x1) and max(y0, y1) >= crd[1] >= min(y0, y1) and \
                        10 >= crd[0] + a * crd[1] + b >= -10:
                    self.slct = True
                    break
            sta_crd = (x1, y1)

        self.display()
        return self.slct

    def get_comp_tmnl(self):
        """
        method: 获取导线两端连接的元件id和端子号
        :return: ((sta_comp_id, sta_comp_tmnl), (end_comp_id, end_comp_tmnl))
        """
        return (self.source_data['sta_comp'], self.source_data['sta_tmnl']), \
               (self.source_data['end_comp'], self.source_data['end_tmnl'])


class Graph(Element):
    """
    class: 图形
    """

    def __init__(self,
                 grph_nm,
                 grph_data=None):
        """
        method: 创建一个图形
        :param grph_nm: 图形名称
        :param grph_data:
        """
        super().__init__(default_data=dft_graph_data[grph_nm],
                         source_data=grph_data)

    def display(self,
                canvas=None,
                crd_x=None,
                crd_y=None,
                angle=None):
        """
        method:
        :param canvas:
        :param crd_x:
        :param crd_y:
        :param angle:
        :return:
        """
        crd_x, crd_y, angle = super().display(canvas,
                                              crd_x,
                                              crd_y,
                                              angle)
        if self.source_data['visible']:
            """绘制元件"""
            # 绘制元件本身
            if self.source_data['id'].split('-')[0] == 'arrow':
                comp_data = draw_arrow(id=self.source_data['id'],
                                       cnt_crd=(crd_x, crd_y),
                                       angle=angle,
                                       canvas=self.canvas,
                                       slct=self.slct,
                                       tail_len=self.source_data['tail_len'],
                                       arrw_len=self.source_data['arrw_len'],
                                       arrw_wid=self.source_data['arrw_wid'])
                self.square = comp_data['square']
            elif self.source_data['id'].split('-')[0] == 'pn':
                comp_data = draw_pn(id=self.source_data['id'],
                                    cnt_crd=(crd_x, crd_y),
                                    angle=angle,
                                    canvas=self.canvas,
                                    slct=self.slct,
                                    distance=self.source_data['distance'],
                                    size=self.source_data['size'],
                                    color=self.source_data['color'])
                self.square = comp_data['square']
            else:
                raise TypeError('Unknow graph')


class Component:
    """
    class: 元件
    """

    def __init__(self,
                 comp_nm,
                 comp_data=None):
        """
        method: 元件（包含元件本身、文本、图片等）
        :param comp_nm: 元件名称
        :param comp_data: 元件数据
        """
        self.source_data = None
        self.part_obj = None
        self.text_objs = {}
        self.grph_objs = {}
        if comp_data:
            self.source_data = comp_data
            self.part_obj = Part(part_nm=comp_nm, part_data=comp_data['part_data'])
            for key in comp_data['texts_data']:
                self.text_objs[key] = Text(text_data=comp_data['texts_data'][key])
            for key in comp_data['grphs_data']:
                self.grph_objs[key] = Graph(grph_nm=comp_data['grphs_data'][key]['id'].split('-')[0],
                                            grph_data=comp_data['grphs_data'][key])
        else:
            self.part_obj = Part(comp_nm)
            part_id = self.part_obj.get_data('id')
            self.text_objs['default'] = Text()
            self.text_objs['default'].edit(id='default-' + part_id,
                                           content=self.part_obj.get_data('designator') + '\n' +
                                                   self.part_obj.get_valfomula_str(),
                                           crd_x=self.part_obj.get_data('crd_x') + 20,
                                           crd_y=self.part_obj.get_data('crd_y') + 20)

            self.grph_objs['dft_vol'] = Graph(grph_nm='pn')
            # 确定正负号的方向
            vol_agl = self.part_obj.get_data('angle') + 180 * (not self.part_obj.vol_dir)
            self.grph_objs['dft_vol'].edit(id='pn-' + part_id,
                                           crd_x=self.part_obj.get_data('crd_x'),
                                           crd_y=self.part_obj.get_data('crd_y') + 10,
                                           angle=vol_agl)
            # GND不需要显示电压
            if part_id.split('-')[0] == 'ground':
                self.grph_objs['dft_vol'].edit(visible=False)

            self.grph_objs['dft_cur'] = Graph(grph_nm='arrow')
            # 确定箭头的方向
            if 'vol' in self.part_obj.get_data('id') or 'cur' in self.part_obj.get_data('id'):
                cur_agl = self.part_obj.get_data('angle') + 180 * self.part_obj.cur_dir
            else:
                cur_agl = self.part_obj.get_data('angle') + 180 * (not self.part_obj.cur_dir)

            self.grph_objs['dft_cur'].edit(id='arrow-' + part_id,
                                           crd_x=self.part_obj.get_data('crd_x'),
                                           crd_y=self.part_obj.get_data('crd_y') + 30,
                                           angle=cur_agl)
            # GND不需要显示电流
            if part_id.split('-')[0] == 'ground':
                self.grph_objs['dft_cur'].edit(visible=False)
            self.source_data = {'part_data': self.part_obj.get_data(),
                                'texts_data': {'default': self.text_objs['default'].get_data()},
                                'grphs_data': {'dft_vol': self.grph_objs['dft_vol'].get_data(),
                                               'dft_cur': self.grph_objs['dft_cur'].get_data()}}

        # 被选中情况
        self.slct = {'part': False, 'text': '', 'grph': ''}
        self.__file = File()
        self.rt_menu = None

    def open(self,
             path=None,
             file=None):
        """
        method: 打开元件文件，及.cmp文件，读取数据并放入self.comp_data
        :param path: 文件路径
        :param file: 文件名称，带.cmp
        :return:
        """
        # 读取文件，得到数据
        comp_data = self.__file.open_cmpfile(path, file)
        # 调用编辑方法，修改self.comp_data
        self.source_data = comp_data

    def save(self,
             filepath=None):
        """
        method: 保存，如果filepath给定，则将self.comp_data保存入filepath中，如果filepath未给定，而self.comp_data是从某个文件
        中读出的，则将self.comp_data保存入该文件，如果filepath未给定，且self.comp_data不是从某个文件中读出的，则报错
        :param filepath: 文件全路径
        :return:
        """
        # 将数据保存在
        self.__file.save_cmpfile(self.source_data, filepath)

    def edit(self,
             part_id=None,
             text_id=None,
             grph_id=None,
             **data):
        """
        method: 编辑元件，根据text_id或grph_id指定编辑的是哪个文本或哪个图形，如果text_id和grph_id全都缺省，则由self.slct
        确定编辑的是哪个文本、哪个图形或元件本身，如果self.slct没有选中任何一个元素，则编辑功能并不发生
        :param part_id: 元件id，缺省时，以self.slct为准
        :param text_id: 文本id，缺省时，以self.slct为准
        :param grph_id: 图形id，缺省时，以self.slct为准
        :param data: 被编辑元件的各个元素(part、text、graph)的参数，如id、designator
        :return:
        """
        if text_id is None:
            text_id = self.slct['text']
        elif grph_id is None:
            grph_id = self.slct['grph']
        elif part_id is None:
            part_id = self.slct['part']

        if text_id:
            self.__edit_text(text_id=text_id,
                             **data)
        elif grph_id:
            self.__edit_graph(grph_id=grph_id,
                              **data)
        elif part_id:
            self.__edit_part(**data)

    def delete(self,
               text_id=None,
               grph_id=None):
        """
        method: 删除元件或其元素，根据text_id或grph_id指定删除的是哪个文本或哪个图形，默认文本和默认图形不能单独删除
        如果text_id和grph_id全都缺省，则由self.slct确定删除的是哪个文本、哪个图形或元件本身，如果self.slct没有选中任何一个元素
        ，则删除功能并不发生
        :param text_id: 文本id，缺省时，以self.slct为准
        :param grph_id: 图形id，缺省时，以self.slct为准
        :return:
        """
        # 确定的被删除的文本或图形的id
        if text_id is None:
            text_id = self.slct['text']
        elif grph_id is None:
            grph_id = self.slct['grph']

        if text_id:
            if text_id != 'default':
                self.text_objs.pop(text_id)
                self.source_data['texts_data'].pop(text_id)
        elif grph_id:
            if grph_id != 'dft_vol' and grph_id != 'dft_cur':
                self.text_objs.pop(grph_id)
                self.source_data['grphs_data'].pop(grph_id)

    def __edit_part(self,
                    **data):
        """
        method: 编辑元件，将self.comp_data中的相关参数（部分）修改为用户指定的值
        :param data: 元件信息，dict数据，具体见Default模块
        """
        # 只有没调用self.display前，才能修改id
        if self.part_obj.canvas is not None and 'id' in data.keys():
            print('Edition of id is not permitted!!')
            data.pop('id')
        self.part_obj.edit(**data)

        # 如果元件修改了id，则文本和图形都要相应修改
        if 'id' in data.keys():
            self.text_objs['default'].edit(id='default-' + self.source_data['part_data']['id'])
            self.grph_objs['dft_vol'].edit(id='pn-' + self.source_data['part_data']['id'])
            self.grph_objs['dft_cur'].edit(id='arrow-' + self.source_data['part_data']['id'])
        # 如果元件修改了designator，则文本需要修改其内容
        if 'designator' in data.keys():
            self.text_objs['default'].edit(content=self.part_obj.get_data('designator') + '\n' +
                                                   self.part_obj.get_valfomula_str())

    def __edit_text(self,
                    text_id=None,
                    **text_data):
        """
        method: 单独修改文本，只能修改其visible、content、font_family、font_size、font_weight、font_slant、font_underline、
        font_overstrike这几个参数，而id需通过.edit_comp()方法修改，crd_x和crd_y需通过.move()方法修改
        :param text_id:
        :param text_data: 文本数据， content, visible
        :return:
        """
        if text_id is None:
            text_id = self.slct['text']
        if text_id is None:
            print('No object is selected!')
            return
        for key in text_data:
            if key == 'visible' or key == 'content' or key == 'font_family' or key == 'font_size' or \
                    key == 'font_weight' or key == 'font_slant' or key == 'font_underline' or key == 'font_overstrike':
                self.text_objs[text_id].edit(key=text_data[key])

    def __edit_graph(self,
                     grph_id=None,
                     **grph_data):
        """
        method: 编辑图形
        :param grph_id:
        :param grph_data:
        :return:
        """
        if grph_id is None:
            grph_id = self.slct['grph']
        if not grph_id:
            print("No component's graph object is selected!")
            return
        self.grph_objs[grph_id].edit(**grph_data)

    def get_databk(self,
                   data=None):
        """
        method: 获取元件的某个数据data，data应该是self.source_data的某个键值，当data缺省时，返回整个self.source_data
        :param data: 想要获取的数据名称
        :return: 参数值
        """
        # 如果data为空，返回self.__comp_data
        if data is None:
            return self.source_data
        # 如果data不为空，则返回data指定的数据
        else:
            if data in self.source_data.keys():
                return self.source_data[data]
            else:
                print('This data is not exist!')
                return None

    def get_elm_data(self):
        """
        method: 获取元件的某个元素(part、text、graph)的数据，返回一个字典，元素由self.slct指定
        :return: self.slct指定的某元素的数据，dict
        """
        if self.slct['text']:
            return self.text_objs[self.slct['text']].get_data()
        elif self.slct['grph']:
            return self.grph_objs[self.slct['grph']].get_data()
        elif self.slct['part']:
            return self.part_obj.get_data()
        else:
            return None

    def add_text(self,
                 **text_data):
        """
        method: 添加text对象
        :return:
        """
        # 遵照text_data的部分指示创建一个新的文本对象
        txt_obj = Text(text_data)
        # 修改文本的坐标
        crd_x = self.part_obj.get_data('crd_x') + 20
        crd_y = self.part_obj.get_data('crd_y')
        num = len(self.text_objs)
        crd_y += (num + 1) * 10
        txt_obj.edit(crd_x=crd_x, crd_y=crd_y)
        self.text_objs[text_data['id']] = txt_obj
        # 将新文本的数据添加self.source_data中
        self.source_data['texts_data'][text_data['id']] = txt_obj.get_data()
        # 新添加的文本显示出来
        txt_obj.display()

    def del_text(self,
                 id=None):
        """
        method: 删除文本
        :param id:
        :return:
        """
        if id is None:
            id = self.slct['text']
            if id not in self.text_objs.keys():
                print('No text was deleted!')
                return
            elif id == 'default':
                print('The default text can not be deleted!')
                return
        self.text_objs[id].clear()
        self.text_objs.pop(id)
        self.source_data['texts_data'].pop(id)
        for key in self.text_objs:
            self.text_objs[key].display()

    def display(self,
                canvas=None,
                crd_x=None,
                crd_y=None,
                angle=None):
        """
        method: 将元件显示在画布上
        :param canvas: 画布
        :param crd_x: 给定的元件x坐标, 缺省时，按self.comp_data['crd_x']绘制
        :param crd_y: 给定的元件y坐标, 缺省时，按self.comp_data['crd_y']绘制
        :param angle: 给定的元件角度，缺省时，按self.comp_data['angle']绘制
        :return:
        """
        self.part_obj.display(canvas, crd_x, crd_y, angle)
        for key in self.text_objs:
            self.text_objs[key].display(canvas, crd_x, crd_y, angle)
        for key in self.grph_objs:
            self.grph_objs[key].display(canvas, crd_x, crd_y, angle)

    def clear(self):
        """
        method: 清除元件显示，用作刷新显示
        """
        self.part_obj.clear()
        for key in self.text_objs:
            self.text_objs[key].clear()
        for key in self.grph_objs:
            self.grph_objs[key].clear()

    def select(self,
               crd=None):
        """
        method: 判断元件本身及其文本是否被点crd=(x, y)选择
        :return: 选中：True, 未选中: False
        """
        # 判断元件文本是否被选中
        self.slct['text'] = ''
        for key in self.text_objs:
            if self.text_objs[key].select(crd):
                self.slct['text'] = key
                return True
        # 如果元件本身未被选中，则判断元件图形是否被选中
        self.slct['grph'] = ''
        for key in self.grph_objs:
            if self.grph_objs[key].select(crd):
                self.slct['grph'] = key
                return True
        # 如果元件本身未被选中，则判读元件本身是否被选中
        self.slct['part'] = self.part_obj.select(crd)
        # 返回最终选择结果
        return self.slct['part']

    def move(self,
             to_crd=None):
        """
        method: 平移元件或其文本
        :param to_crd: 目标坐标
        """
        # 点捕获，即目标点是离散的点，间隔距离可由函数point_capture()设置
        to_crd = point_capture(to_crd)
        if to_crd:
            # 记住现在的坐标
            now_x = self.part_obj.get_data('crd_x')
            now_y = self.part_obj.get_data('crd_y')
            x_bias = to_crd[0] - now_x
            y_bias = to_crd[1] - now_y
            if self.slct['text']:
                self.text_objs[self.slct['text']].move(to_crd)
            elif self.slct['grph']:
                self.grph_objs[self.slct['grph']].move(to_crd)
            elif self.slct['part']:
                self.part_obj.move(to_crd)
                for key in self.text_objs:
                    txt_to_crd = (self.text_objs[key].get_data('crd_x') + x_bias,
                                  self.text_objs[key].get_data('crd_y') + y_bias)
                    self.text_objs[key].move(txt_to_crd)
                for key in self.grph_objs:
                    gph_to_crd = (self.grph_objs[key].get_data('crd_x') + x_bias,
                                  self.grph_objs[key].get_data('crd_y') + y_bias)
                    self.grph_objs[key].move(gph_to_crd)

    def rotate(self):
        """
        method: 顺时针旋转元件90度
        :return: None
        """
        if self.slct['part']:
            self.part_obj.rotate()
            self.grph_objs['dft_vol'].rotate()
            cnt_x, cnt_y = coord_mirr_rota(orig_crd=(self.grph_objs['dft_vol'].source_data['crd_x'],
                                                     self.grph_objs['dft_vol'].source_data['crd_y']),
                                           cnt_crd=(self.part_obj.source_data['crd_x'],
                                                    self.part_obj.source_data['crd_y']),
                                           angle=90)
            self.grph_objs['dft_vol'].move(to_crd=(cnt_x, cnt_y))

            self.grph_objs['dft_cur'].rotate()
            cnt_x, cnt_y = coord_mirr_rota(orig_crd=(self.grph_objs['dft_cur'].source_data['crd_x'],
                                                     self.grph_objs['dft_cur'].source_data['crd_y']),
                                           cnt_crd=(self.part_obj.source_data['crd_x'],
                                                    self.part_obj.source_data['crd_y']),
                                           angle=90)
            self.grph_objs['dft_cur'].move(to_crd=(cnt_x, cnt_y))

    def editable_data(self):
        """
        method: 可编辑的数据，根据元件的不同，各不相同
        :return:
        """
        comp_nm = self.source_data['part_data']['id'].split('-')[0]
        if comp_nm == 'resistor':
            return {'designator': self.source_data['part_data']['designator'],
                    'value': self.source_data['part_data']['value']}
        elif comp_nm == 'capacitor':
            return {'designator': self.source_data['part_data']['designator'],
                    'value': self.source_data['part_data']['value'],
                    'Uc': self.source_data['part_data']['Uc']}
        elif comp_nm == 'inductor':
            return {'designator': self.source_data['part_data']['designator'],
                    'value': self.source_data['part_data']['value'],
                    'Il': self.source_data['part_data']['Il']}
        elif comp_nm == 'diode':
            return {'designator': self.source_data['part_data']['designator'],
                    'Ir': self.source_data['part_data']['Ir'],
                    'Vf': self.source_data['part_data']['Vf']}
        elif comp_nm == 'voltage_dc' or comp_nm == 'current_dc':
            return {'designator': self.source_data['part_data']['designator'],
                    'amp': self.source_data['part_data']['value']}
        elif comp_nm == 'voltage_ac' or comp_nm == 'current_ac':
            return {'designator': self.source_data['part_data']['designator'],
                    'amp': self.source_data['part_data']['amp'],
                    'freq': self.source_data['part_data']['freq'],
                    'phase': self.source_data['part_data']['phase']}

    def edit_window(self):
        """
        method: 编辑窗口
        :return:
        """
        edit_page = EditPage(data=self.editable_data())

        def func_save():
            """
            func: 保存按键执行函数
            :return:
            """
            edit_page.page.root.destroy()
            self.__edit_part(**edit_page.edit.data)
            self.display()

        edit_page.command(func_save=func_save)
        edit_page.maintain()

    def change_ref_dir(self):
        """
        method: 更改参考方向
        :return:
        """
        # 如果选中元件的图像
        if self.slct['grph']:
            # 如果选中的是参考电压图形，则更改其电压参考方向
            if self.slct['grph'] == 'dft_vol':
                if self.source_data['part_data']['vol_dir'] is True:
                    self.source_data['part_data']['vol_dir'] = False
                else:
                    self.source_data['part_data']['vol_dir'] = True
            # 如果选中的是参考电流图形，则更改其电流参考方向
            elif self.slct['grph'] == 'dft_cur':
                if self.source_data['part_data']['cur_dir'] is True:
                    self.source_data['part_data']['cur_dir'] = False
                else:
                    self.source_data['part_data']['cur_dir'] = True
            # 图像旋转2次90度，即相当于反向
            self.grph_objs[self.slct['grph']].rotate()
            self.grph_objs[self.slct['grph']].rotate()

    def pop_rt_menu(self, x, y):
        """
        method: 右键菜单栏
        :return:
        """
        if self.slct['part']:
            self.rt_menu = tk.Menu(self.part_obj.canvas, tearoff=0)

            self.rt_menu.add_command(label='Edit', command=self.edit_window)
            self.rt_menu.add_separator()
            ref_vol_visible = tk.IntVar(value=self.grph_objs['dft_vol'].get_data('visible'))

            def set_refvol_visible():
                if ref_vol_visible.get():
                    self.__edit_graph(grph_id='dft_vol', visible=True)
                else:
                    self.__edit_graph(grph_id='dft_vol', visible=False)
                self.grph_objs['dft_vol'].display()

            self.rt_menu.add_checkbutton(label='ref_vol', variable=ref_vol_visible, command=set_refvol_visible)

            ref_cur_visible = tk.IntVar(value=self.grph_objs['dft_cur'].get_data('visible'))

            def set_refcur_visible():
                if ref_cur_visible.get():
                    self.__edit_graph(grph_id='dft_cur', visible=True)
                else:
                    self.__edit_graph(grph_id='dft_cur', visible=False)
                self.grph_objs['dft_cur'].display()

            self.rt_menu.add_checkbutton(label='ref_cur', variable=ref_cur_visible, command=set_refcur_visible)
            self.rt_menu.add_separator()

            self.rt_menu.post(x, y + 88)

    def tmnl_select(self,
                    crd):
        """
        method: 判断元件端子是否被点(crd)选择，如果被选择，读取端子号，如果未选择，返回False
        :param crd: 点(x, y)坐标
        :return: 选中: 端子号(1, 2,..), 未选中: False
        """
        return self.part_obj.tmnl_select(crd)

    def get_tmnl_crd(self,
                     tmnl):
        """
        method: 获取元件端子的绝对坐标
        :param tmnl: 端子号，1, 2,...
        :return: tmnl为1, 2,...时，返回端子号指定的坐标
        """
        return self.part_obj.get_tmnl_crd(tmnl)

    def get_tmnl_net(self,
                     tmnl):
        """
        method: 获取端子网络id
        :param tmnl: 端子号, int
        """
        return self.part_obj.get_tmnl_net(tmnl)


class Resistor(Component):
    """
    class: 电阻
    """
    def __init__(self,
                 comp_data=None):
        """
        method: 创建电阻元件
        :param comp_data: 元件数据
        """
        super().__init__(comp_nm='R',
                         comp_data=comp_data)

    def edit_part(self,
                  **data):
        """
        method: 修改元件数据
        :param data:
        :return:
        """
        if data['id'].split('-')[0] != 'R':
            raise TypeError('The form of resistor id must be "R-?"!')
        super().edit_part(**data)


class Capacitor(Component):
    """
    class: 电容
    """
    def __init__(self,
                 comp_data=None):
        """
        method: 创建电阻元件
        :param comp_data: 元件数据
        """
        super().__init__(comp_nm='C',
                         comp_data=comp_data)

    def edit_part(self,
                  **data):
        """
        method: 修改元件数据
        :param data:
        :return:
        """
        if data['id'].split('-')[0] != 'C':
            raise TypeError('The form of resistor id must be "C-?"!')
        super().edit_part(**data)


class Inductor(Component):
    """
    class: 电感
    """
    def __init__(self,
                 comp_data=None):
        """
        method: 创建电感元件
        :param comp_data: 元件数据
        """
        super().__init__(comp_nm='L',
                         comp_data=comp_data)

    def edit_part(self,
                  **data):
        """
        method: 修改元件数据
        :param data:
        :return:
        """
        if data['id'].split('-')[0] != 'L':
            raise TypeError('The form of resistor id must be "L-?"!')
        super().edit_part(**data)


class Diode(Component):
    """
    class: 二极管
    """
    def __init__(self,
                 comp_data=None):
        """
        method: 创建二极管元件
        :param comp_data: 元件数据
        """
        super().__init__(comp_nm='D',
                         comp_data=comp_data)

    def edit_part(self,
                  **data):
        """
        method: 修改元件数据
        :param data:
        :return:
        """
        if data['id'].split('-')[0] != 'D':
            raise TypeError('The form of resistor id must be "D-?"!')
        super().edit_part(**data)


class VolAC(Component):
    """
    class: 交流电压源
    """
    def __init__(self,
                 comp_data=None):
        """
        method: 创建交流电压源元件
        :param comp_data: 元件数据
        """
        super().__init__(comp_nm='Uac',
                         comp_data=comp_data)

    def edit_part(self,
                  **data):
        """
        method: 修改元件数据
        :param data:
        :return:
        """
        if data['id'].split('-')[0] != 'Uac':
            raise TypeError('The form of resistor id must be "Uac-?"!')
        super().edit_part(**data)


class VolDC(Component):
    """
    class: 直流电压源
    """
    def __init__(self,
                 comp_data=None):
        """
        method: 创建直流电压源元件
        :param comp_data: 元件数据
        """
        super().__init__(comp_nm='Udc',
                         comp_data=comp_data)

    def edit_part(self,
                  **data):
        """
        method: 修改元件数据
        :param data:
        :return:
        """
        if data['id'].split('-')[0] != 'Udc':
            raise TypeError('The form of resistor id must be "Udc-?"!')
        super().edit_part(**data)


class CurAC(Component):
    """
    class: 交流电流源
    """
    def __init__(self,
                 comp_data=None):
        """
        method: 创建交流电流源元件
        :param comp_data: 元件数据
        """
        super().__init__(comp_nm='Iac',
                         comp_data=comp_data)

    def edit_part(self,
                  **data):
        """
        method: 修改元件数据
        :param data:
        :return:
        """
        if data['id'].split('-')[0] != 'Iac':
            raise TypeError('The form of resistor id must be "Iac-?"!')
        super().edit_part(**data)


class CurDC(Component):
    """
    class: 直流电流源
    """
    def __init__(self,
                 comp_data=None):
        """
        method: 创建直流电流源元件
        :param comp_data: 元件数据
        """
        super().__init__(comp_nm='Idc',
                         comp_data=comp_data)

    def edit_part(self,
                  **data):
        """
        method: 修改元件数据
        :param data:
        :return:
        """
        if data['id'].split('-')[0] != 'Idc':
            raise TypeError('The form of resistor id must be "Idc-?"!')
        super().edit_part(**data)


class Connector:
    """
    class: 连接器，由Wire和Text组成
    """
    def __init__(self,
                 conn_data=None,
                 comp_objs=None):
        """
        method:
        :param conn_data: 连接器数据
        :param comp_objs: 元件对象
        """
        self.wire_obj = None
        self.text_objs = {}
        self.source_data = None
        # 如果创建的时候给定数据
        if conn_data:
            self.source_data = conn_data
            self.wire_obj = Wire(wire_data=conn_data['wire_data'], comp_objs=comp_objs)
            for key in conn_data['texts_data']:
                self.text_objs[key] = Text(text_data=conn_data['texts_data'][key])
        else:
            self.wire_obj = Wire(comp_objs=comp_objs)
            self.text_objs['default'] = Text()
            self.source_data = {'wire_data': self.wire_obj.get_data(),
                                'texts_data': {'default': self.text_objs['default'].get_data()}}

        # 被选中情况
        self.slct = {'wire': False, 'text': ''}

    def edit_wire(self,
                  **data):
        """
        method: 编辑元件，将self.comp_data中的相关参数（部分）修改为用户指定的值
        :param data: 元件信息，dict数据，具体见Default模块
        """
        # 如果已经调用self.display显示了，则不能修改id参数，其他参数可以修改
        if self.wire_obj.canvas is not None and 'id' in data.keys():
            print('Edition of id is not permitted!!')
            data.pop('id')
        self.wire_obj.edit(**data)
        # 如果修改了id参数，则文本部分需要修改
        if 'id' in data.keys():
            self.text_objs['default'].edit(content=self.source_data['wire_data']['id'])

    def edit_text(self,
                  text_id,
                  content):
        """
        method: 修改文本的内容
        :param text_id:
        :param content:
        :return:
        """
        if text_id == 'default':
            print('This text is not editable!!')
        else:
            self.text_objs[text_id].edit(content=content)

    def delete(self,
               text_id=None):
        """
        method: 删除元件或其元素，根据text_id或grph_id指定删除的是哪个文本或哪个图形，默认文本和默认图形不能单独删除
        如果text_id和grph_id全都缺省，则由self.slct确定删除的是哪个文本、哪个图形或元件本身，如果self.slct没有选中任何一个元素
        ，则删除功能并不发生
        :param text_id: 文本id，缺省时，以self.slct为准
        :return:
        """
        # 确定的被删除的文本或图形的id
        if text_id is None:
            text_id = self.slct['text']

        if text_id:
            if text_id != 'default':
                self.text_objs.pop(text_id)
                self.source_data['texts_data'].pop(text_id)

    def tmnl_select(self,
                    crd):
        """
        method: 端子选择
        :param crd:
        :return:
        """
        return self.wire_obj.tmnl_select(crd)

    def get_databk(self,
                   data=None):
        """
        method: 获取导线的某个数据data，data应该是self.source_data的某个键值，当data缺省时，返回整个self.source_data
        :param data: 想要获取的数据名称
        :return: 参数值
        """
        # 如果data为空，返回self.__comp_data
        if data is None:
            return self.source_data
        # 如果data不为空，则返回data指定的数据
        else:
            if data in self.source_data.keys():
                return self.source_data[data]
            else:
                print('This data is not exist!')
                return None

    def add_text(self,
                 **text_data):
        """
        method: 添加text对象
        :return:
        """
        # 遵照text_data的部分指示创建一个新的文本对象
        txt_obj = Text(text_data)
        # 修改文本的坐标
        num = len(self.text_objs)
        crd_x = self.text_objs['default'].get_data('crd_x')
        crd_y = self.text_objs['default'].get_data('crd_y') + (num + 1) * 10
        txt_obj.edit(crd_x=crd_x, crd_y=crd_y)
        self.text_objs[text_data['id']] = txt_obj
        # 将新文本的数据添加self.source_data中
        self.source_data['texts_data'][text_data['id']] = txt_obj.get_data()

    def __del_text(self,
                   text_id):
        """
        method: 删除文本
        :param text_id:
        :return:
        """
        if text_id == 'default':
            print('The default text can not be deleted!')
        else:
            self.text_objs[text_id].clear()
            self.text_objs.pop(text_id)
            self.source_data['texts_data'].pop(text_id)

    def display(self,
                canvas=None):
        """
        method: 将元件显示在画布上
        :param canvas: 画布
        :return:
        """
        self.wire_obj.display(canvas)
        for key in self.text_objs:
            self.text_objs[key].display(canvas)

    def clear(self):
        """
        method: 清除导线显示，用作刷新显示
        """
        self.wire_obj.clear()
        for key in self.text_objs:
            self.text_objs[key].clear()

    def select(self,
               crd=None):
        """
        method: 判断元件本身及其文本是否被点crd=(x, y)选择
        :return: 选中：True, 未选中: False
        """
        # 判断导线文本是否被选中
        self.slct['text'] = ''
        for key in self.text_objs:
            if self.text_objs[key].select(crd):
                self.slct['text'] = key
                return True
        # 如果导线文本未被选中，则判读导线本身是否被选中
        if not self.slct['text']:
            self.slct['wire'] = self.wire_obj.select(crd)
        return self.slct['wire']

    def move(self,
             to_crd=None):
        """
        method: 平移导线文本
        :param to_crd: 目标坐标
        """
        # 点捕获，即目标点是离散的点，间隔距离可由函数point_capture()设置
        to_crd = point_capture(to_crd)
        if self.slct['text']:
            self.text_objs[self.slct['text']].move(to_crd)

    def get_comp_tmnl(self):
        """
        method: 获取起点、终点的元件及其端子号
        :return:
        """
        return self.wire_obj.get_comp_tmnl()


class Circuit:
    """
    class: 电路
    """
    def __init__(self,
                 cir_name=None,
                 cir_data=None):
        """
        method:
        :param cir_name: 电路名称
        :param cir_data: 电路数据
        """
        # 电路名称
        self.cir_name = None
        # 源数据
        self.source_data = None
        # 文件中保存的数据
        self.file_data = None
        # 右键弹出目录
        self.rt_menu = None
        # 元件对象 集合
        self.comp_objs = {}
        # 导线对象 集合
        self.conn_objs = {}
        # 文本对象 集合
        self.text_objs = {}
        # 图形对象 集合
        self.grph_objs = {}

        # 画布
        self.canvas = None

        # File对象，用于完成.cir和.cmp文件的读写功能
        self.file_obj = File()

        # 电路名
        if cir_name:
            self.cir_name = cir_name
        else:
            self.cir_name = 'New Circuit'

        # 电路分析工具
        self.calculation = Calculation()

        # 创建电路
        if cir_data:
            self.__build_cir(cir_data)
        else:
            self.source_data = {'cir_config': copy.deepcopy(dft_cir_config),
                                'comps_data': {},
                                'conns_data': {},
                                'texts_data': {},
                                'grphs_data': {}}

    def __build_cir(self,
                    cir_data):
        """
        method: 创建电路
        :param cir_data: 电路数据
        :return:
        """
        self.source_data = cir_data
        for key in cir_data['comps_data']:
            self.comp_objs[key] = Component(comp_nm=key.split('-')[0],
                                            comp_data=cir_data['comps_data'][key])
        for key in cir_data['conns_data']:
            self.conn_objs[key] = Connector(conn_data=cir_data['conns_data'][key],
                                            comp_objs=self.comp_objs)
        for key in cir_data['texts_data']:
            self.text_objs[key] = Text(text_data=cir_data['texts_data'][key])
        for key in cir_data['grphs_data']:
            self.text_objs[key] = Graph(grph_nm=key.split('-')[0],
                                        grph_data=cir_data['grphs_data'][key])

    def display(self,
                canvas=None):
        """
        method: 显示
        :param canvas:
        :return:
        """
        if canvas:
            self.canvas = canvas
        if self.canvas:
            for key in self.comp_objs:
                self.comp_objs[key].display(self.canvas)
            for key in self.conn_objs:
                self.conn_objs[key].display(self.canvas)
            for key in self.text_objs:
                self.text_objs[key].display(self.canvas)
            for key in self.grph_objs:
                self.grph_objs[key].display(self.canvas)
        else:
            print('The canvas is needed!')

    def add_component(self,
                      comp_nm,
                      func,
                      **comp_data):
        """
        method: 添加元件
        :param comp_nm: 元件名称
        :param func: 完成添加元件后调用的函数
        :param comp_data:
        :return:
        """
        # 创建新添加元件的对象
        comp_obj = Component(comp_nm)
        # 编辑元件
        comp_obj.edit(part_id=True,
                      id=self.gen_comp_id(comp_nm))
        comp_obj.display(self.canvas)
        self.comp_objs[comp_obj.get_databk('part_data')['id']] = comp_obj
        self.source_data['comps_data'][comp_obj.get_databk('part_data')['id']] = comp_obj.get_databk()

    def select(self, crd):
        """
        method: 判断所有的元件、导线、文本、图形被选中的情况
        :param crd:
        :return:
        """
        for key in self.comp_objs:
            if self.comp_objs[key].select(crd):
                return True
        for key in self.conn_objs:
            if self.conn_objs[key].select(crd):
                return True
        for key in self.text_objs:
            if self.text_objs[key].select(crd):
                return True
        for key in self.grph_objs:
            if self.grph_objs[key].select(crd):
                return True
        return False

    def move(self, to_crd):
        """
        method: 移动被选中的元件或其文本、图形到to_crd坐标
        :param to_crd:
        :return:
        """
        for key in self.comp_objs:
            self.comp_objs[key].move(to_crd)
        for key in self.conn_objs:
            self.conn_objs[key].move(to_crd)
        for key in self.text_objs:
            self.text_objs[key].move(to_crd)
        for key in self.grph_objs:
            self.grph_objs[key].move(to_crd)

    def rotate(self):
        """
        method: 旋转可以旋转的元件或图形
        :return:
        """
        for key in self.comp_objs:
            self.comp_objs[key].rotate()
        for key in self.grph_objs:
            self.grph_objs[key].rotate()

    def delete(self):
        """
        method: 删除电路中的元件或其文本、图形；导线或其文本
        :return:
        """
        self.__del_component()
        self.__del_connector()

    def __del_component(self):
        """
        method: 删除被选中的元件或其文本、图形
        :return:
        """
        for key in self.comp_objs:
            # 如果被选中的是元件本身，则判断该元件是否有连接，如果有，则后台输出无法删除的提示，如果没有，则删除该元件
            if self.comp_objs[key].slct['part']:
                if self.comp_objs[key].get_databk('part_data')['node1'] or \
                        self.comp_objs[key].get_databk('part_data')['node2']:
                    print('The compnent has connects, can not be delected!')
                else:
                    self.comp_objs[key].clear()
                    self.comp_objs.pop(key)
                    self.source_data['comps_data'].pop(key)
                    return
            else:
                # 由各个元件自己删除隶属自己的被选中的文本或图像，如果无被选中的文本或图像，则不执行删除功能
                self.comp_objs[key].delete()

    def __del_connector(self):
        """
        method: 删除被选中的导线或其文本
        当删除导线时，在self.conn_objs中删除导线的对象，删除导线完成后，还要判断导线删除之前连接元件端子上的导线数量，如果为零，
        则修改该元件self.source_data['comps_data']['node1']或self.source_data['comps_data']['node2']为None
        """
        for key in self.conn_objs:
            # 如果选中的是导线本身，则删除导线，且修改导线两侧连接的元件的端子信息
            if self.conn_objs[key].slct['wire']:
                # 找到导线两端的元件id和端子号
                wire_data = self.conn_objs[key].get_databk('wire_data')
                comp1_id = wire_data['sta_comp']
                comp1_tmnl = wire_data['sta_tmnl']
                comp2_id = wire_data['end_comp']
                comp2_tmnl = wire_data['end_tmnl']
                # 计算元件comp_id的端子comp_tmnl上连接的现存的导线数目，当为1时，说明此次删除后端子上无导线，故端子网络为None
                if self.count_wire_num(comp1_id, comp1_tmnl) == 1:
                    if comp1_id.split('-')[0] != 'ground':
                        comp_data = {('node' + comp1_tmnl): None}
                        self.comp_objs[comp1_id].edit(part_id=True,
                                                      **comp_data)
                if self.count_wire_num(comp2_id, comp2_tmnl) == 1:
                    if comp2_id.split('-')[0] != 'ground':
                        comp_data = {('node' + comp2_tmnl): None}
                        self.comp_objs[comp2_id].edit(part_id=True,
                                                      **comp_data)
                # 将导线wire_id的显示消除
                self.conn_objs[key].clear()
                # 将self.wire_objs的导线wire_id的对象删除
                self.conn_objs.pop(key)
                # 刷新self.cir_data
                self.source_data['conns_data'].pop(key)
                return
            else:
                self.conn_objs[key].delete()

    def clear(self):
        """
        method: 清空电路图，即所有元件、导线、文本、图形隐藏
        :return:
        """
        for key in self.comp_objs:
            self.comp_objs[key].clear()
        for key in self.conn_objs:
            self.conn_objs[key].clear()
        for key in self.text_objs:
            self.text_objs[key].clear()
        for key in self.grph_objs:
            self.grph_objs[key].clear()

    def blank_pop_rt_menu(self, x, y):
        """
        method: 电路空白处右键菜单栏
        :return:
        """
        self.rt_menu = tk.Menu(self.canvas, tearoff=0)

        ref_vol_visible = tk.IntVar(value=self.source_data['cir_config']['ref_vol_visible'])

        def set_refvol_visible():
            if ref_vol_visible.get():
                self.source_data['cir_config']['ref_vol_visible'] = True
            else:
                self.source_data['cir_config']['ref_vol_visible'] = False
            for key in self.comp_objs:
                self.comp_objs[key].edit(grph_id='dft_vol', visible=self.source_data['cir_config']['ref_vol_visible'])
            self.display()

        self.rt_menu.add_checkbutton(label='ref_vol', variable=ref_vol_visible, command=set_refvol_visible)

        ref_cur_visible = tk.IntVar(value=self.source_data['cir_config']['ref_cur_visible'])

        def set_refcur_visible():
            if ref_cur_visible.get():
                self.source_data['cir_config']['ref_cur_visible'] = True
            else:
                self.source_data['cir_config']['ref_cur_visible'] = False
            for key in self.comp_objs:
                self.comp_objs[key].edit(grph_id='dft_cur', visible=self.source_data['cir_config']['ref_cur_visible'])
            self.display()

        self.rt_menu.add_checkbutton(label='ref_cur', variable=ref_cur_visible, command=set_refcur_visible)

        self.rt_menu.post(x, y + 88)

    def pop_rt_menu(self, x, y):
        """
        method:
        :param x:
        :param y:
        :return:
        """
        for key in self.comp_objs:
            self.comp_objs[key].pop_rt_menu(x, y)
        if not self.select(crd=(x, y)):
            self.blank_pop_rt_menu(x, y)

    def count_wire_num(self,
                       comp_id=None,
                       tmnl=None):
        """
        method: 计数元件comp_id的端子tmnl(1, 2, ...)上连接的导线的数量
        :param comp_id: 元件id
        :param tmnl: 元件端子号
        :return: 元件comp_id的端子tmnl上的导线数量
        """
        num = 0
        for key in self.conn_objs:
            if self.conn_objs[key].get_comp_tmnl()[0][0] == comp_id and \
                    self.conn_objs[key].get_comp_tmnl()[0][1] == tmnl:
                num += 1
            if self.conn_objs[key].get_comp_tmnl()[1][0] == comp_id and \
                    self.conn_objs[key].get_comp_tmnl()[1][1] == tmnl:
                num += 1
        return num

    def get_net_comptmnl(self):
        """
        method: 获得网络-元件端子表，{net1:[(comp1,tmnl1), (comp2, tmnl2)], net2:[]}
        """
        net_nodes = {}
        for key in self.comp_objs:
            id = self.comp_objs[key].get_databk('part_data')['id']
            if id.split('-')[0] == 'ground':
                continue
            node1 = self.comp_objs[key].get_databk('part_data')['node1']
            node2 = self.comp_objs[key].get_databk('part_data')['node2']
            if node1 is not None and node1 != 0:
                if node1 not in net_nodes.keys():
                    net_nodes[node1] = [(id, 1)]
                else:
                    net_nodes[node1].append((id, 1))
            if node2 is not None and node2 != 0:
                if node2 not in net_nodes.keys():
                    net_nodes[node2] = [(id, 2)]
                else:
                    net_nodes[node2].append((id, 2))
        return net_nodes

    def get_net_conn(self):
        """
        method: 获取网络-连接器表, {net1: [conn1, conn2, ...], net2: [conn1, conn2, ...]}
        :return:
        """
        net_conn = {}
        for key in self.conn_objs:
            id = self.conn_objs[key].get_databk('wire_data')['id']
            net_id = self.conn_objs[key].get_databk('wire_data')['net_id']
            if net_id is not None and net_id != 0:
                if net_id not in net_conn.keys():
                    net_conn[net_id] = [id]
                else:
                    net_conn[net_id].append(id)
        return net_conn

    def refresh_net_id(self):
        """
        method: 刷新网络id
        :return:
        """
        net_nodes = self.get_net_comptmnl()
        for idx, key in enumerate(net_nodes):
            for comp, tmnl in net_nodes[key]:
                data = {'node' + str(tmnl): idx + 1}
                self.comp_objs[comp].edit(part_id=True, **data)

        net_conns = self.get_net_conn()
        for idx, key in enumerate(net_nodes):
            for conn in net_conns[key]:
                data = {'net_id': idx + 1}
                self.conn_objs[conn].edit_wire(**data)

    def compile(self):
        """
        method: 编译电路，包括判断元件连接是否完成，网络节点号是否连续，编译完成返回True
        :return: True: 编译完成，电路课用于仿真
        """
        # 判断元件的连接是否缺失
        if not self.judge_connect_lack():
            showwarning(title='warning', message='Check the Connection')
            return False
        # 判断net_id，刷新net_id
        if not self.judge_net_id():
            self.refresh_net_id()
        # 判断comp_id，弹出窗口
        if not self.judge_comps_designator():
            showwarning(title='warning', message='Check the designator of compnent!!')
            return False
        return True

    def get_netlist(self):
        """
        method: 获得netlist
        :return:
        """
        if not self.compile():
            return False
        # 获取netlist
        netlist = []
        for key in self.comp_objs:
            if key.split('-')[0] == 'ground':
                continue
            comp_data = copy.deepcopy(self.comp_objs[key].get_databk('part_data'))
            remove_key = ['id', 'crd_x', 'crd_y', 'angle']
            for key in remove_key:
                comp_data.pop(key)
            netlist.append(comp_data)
        return netlist

    def judge_comp_designator(self,
                              designator):
        """
        method: 判断某元件的designator是否正常
        :param designator: 元件designator
        :return:
        """
        if designator.count('-') != 1:
            return False
        if not str.isdecimal(designator.split('-')[1]):
            return False
        return True

    def judge_comps_designator(self):
        """
        method: 判断元件的designator是否正常，包括是否没有是否重名
        :return: True: 正常， False: 异常
        """
        # 获取designator列表
        designator_list = self.get_comp_designator_lst()
        # 判断
        for designator in designator_list:
            if not self.judge_comp_designator(designator):
                return False
        # 判断元件是否重名
        for designator in designator_list:
            if designator_list.count(designator) > 1:
                return False
        return True

    def judge_connect_lack(self):
        """
        method: 判断元件是否缺失连接
        :return:
        """
        # 判断net_id是否存在None
        for key in self.comp_objs:
            if self.comp_objs[key].get_databk('part_data')['node1'] is None:
                print(self.comp_objs[key].get_databk('part_data')['node1'])
                return False
            if self.comp_objs[key].get_databk('part_data')['node2'] is None:
                print(self.comp_objs[key].get_databk('part_data')['node2'])
                return False
        return True

    def judge_net_id(self):
        """
        method: 判断电路的net是否正常，包括net_id是否存在
        :return: True: net_id正常， False: net_id异常
        """
        # 判断net_id是否连续
        net_id_list = self.get_net_id_lst()
        for idx, data in enumerate(net_id_list):
            if idx + 1 not in net_id_list:
                return False
        return True

    def open(self,
             path,
             file):
        """
        method: 打开电路文件(.cir)
        :param path: 路径名称
        :param file: 文件名称，带后缀名.cir
        :return:
        """
        # 读取电路源文件
        source_data = self.file_obj.open_cirfile(path, file)
        # 将文件中的数据记录下来
        self.file_data = copy.deepcopy(source_data)
        # 调用.__build_cir()方法创建电路
        self.__build_cir(source_data)
        # 修改电路名称cir_name
        self.cir_name = file.split('.')[0]

    def save(self,
             filepath=None):
        """
        method: 将self.cir_data保存在文件中，当filepath给定时，保存在filepath中，类似于新建文件的save和save as，以及打开文件
        的save as；当filepath未给定时，保存在self.path_file中，类似于打开文件的save
        :param filepath: 文件全路径, 文件带后缀名.cir
        :return:
        """
        # 将文件中的数据记录下来
        self.file_data = copy.deepcopy(self.source_data)
        self.file_obj.save_cirfile(cir_data=self.source_data,
                                   filepath=filepath)

    def close(self):
        """
        method: 关闭文件
        :return:
        """
        self.clear()
        self.file_obj.source_cirfilepath = None
        self.comp_objs = {}
        self.conn_objs = {}
        self.text_objs = {}
        self.grph_objs = {}
        self.source_data = {'cir_config': copy.deepcopy(dft_cir_config),
                            'comps_data': {},
                            'conns_data': {},
                            'texts_data': {},
                            'grphs_data': {}}
        self.file_data = None

    def get_comp_id_lst(self,
                        comp_nm=None):
        """
        method: 获取某一种元件的list
        若comp_nm为空，则返回所有元件的id
        若comp_nm为某个元件类别，则返回该种元件类别的所以元件的id
        :param comp_nm: 元件名称
        """
        comp_id_lst = []
        for idx, key in enumerate(self.comp_objs):
            if comp_nm == self.comp_objs[key].get_databk('part_data')['id'].split('-')[0]:
                comp_id_lst.append(self.comp_objs[key].get_databk('part_data')['id'])
        return comp_id_lst

    def gen_comp_id(self,
                    comp_nm=None):
        """
        method: 生成一个元件id
        :param comp_nm: 元件名称
        """
        comp_id_lst = self.get_comp_id_lst(comp_nm=comp_nm)
        i = 1
        while 1:
            if comp_nm + '-' + str(i) not in comp_id_lst:
                break
            i += 1
        return comp_nm + '-' + str(i)

    def get_comp_designator_lst(self,
                                comp_nm=None):
        """
        method: 获取所有元件或元件comp_nm的designator的列表
        :param comp_nm: 元件名称
        :return:
        """
        comp_designator_lst = []
        for key in self.comp_objs:
            if key.split('-')[0] != 'ground':
                comp_designator_lst.append(self.comp_objs[key].get_databk('part_data')['designator'])
        if comp_nm is not None:
            new_comp_designator_lst = []
            for comp_dsg in comp_designator_lst:
                if comp_dsg.split('-')[0] == comp_nm:
                    new_comp_designator_lst.append(comp_dsg)
            return new_comp_designator_lst
        else:
            return comp_designator_lst

    def gen_comp_designator(self,
                            comp_nm):
        """
        method: 给元件comp_nm生成一个designator
        :param comp_nm: 元件名称
        :return:
        """
        comp_id_lst = self.get_comp_designator_lst(comp_nm=comp_nm)
        i = 1
        while 1:
            if comp_nm + '-' + str(i) not in comp_id_lst:
                break
            i += 1
        return comp_nm + '-' + str(i)

    def create_comps_designator(self):
        """
        method: 创建元件designator
        :return:
        """
        for key in self.comp_objs:
            designator = self.comp_objs[key].get_databk('part_data')['designator']
            if not self.judge_comp_designator(designator):
                self.comp_objs[key].edit(part_id=True,
                                         designator=self.gen_comp_designator(comp_nm=designator.split('-')[0]))
        self.display()

    def get_wire_id_lst(self):
        """
        method: 获取导线id的list
        """
        wire_id_lst = []
        for key in self.conn_objs:
            wire_id_lst.append(self.conn_objs[key].get_databk('wire_data')['id'])
        return wire_id_lst

    def gen_wire_id(self):
        """
        method: 生成一个导线id
        """
        wire_id_lst = self.get_wire_id_lst()
        i = 1
        while 1:
            if 'wire-' + str(i) not in wire_id_lst:
                break
            i += 1
        return 'wire-' + str(i)

    def gen_net_id(self,
                   comp1_obj=None,
                   comp1_tmnl=None,
                   comp2_obj=None,
                   comp2_tmnl=None):
        """
        method: 给一个新的连接生成一个网络id，用于创建一条导线时，自动生成一个网络id的功能
        :param comp1_obj: 元件1对象
        :param comp1_tmnl: 元件1端子号
        :param comp2_obj: 元件2对象
        :param comp2_tmnl: 元件2端子号
        :return:
        """
        # 如果导线起始端已经有网络了，则新生成的网络为该网络
        sta_net = comp1_obj.get_tmnl_net(comp1_tmnl)
        end_net = comp2_obj.get_tmnl_net(comp2_tmnl)
        if sta_net is not None and end_net is None:
            return comp1_obj.get_tmnl_net(comp1_tmnl)
        # 如果导线终点端已经有网络了，则新生成的网络为该网络
        elif end_net is not None and sta_net is None:
            return comp2_obj.get_tmnl_net(comp2_tmnl)
        # 如果导线起始端和终点端都有网络了，则新生成的网络使用起始端的网络，如果终点端的网络不同，则全部改为该网络
        elif sta_net is not None and end_net is not None:
            if sta_net == end_net:
                return sta_net
            else:
                return False
        # 如果起点和终点都没有网络，则创建新的网络id
        else:
            net_id_lst = self.get_net_id_lst()
            i = 1
            while 1:
                if i not in net_id_lst:
                    break
                i += 1
            return i

    def change_net_id(self,
                      old_net_id,
                      new_net_id):
        """
        method: 将所有元件及导线的网络id由old_net_id改为new_net_id
        :param old_net_id: 旧网络id
        :param new_net_id: 新网络id
        :return:
        """
        # 修改元件的网络id
        for comp_obj in self.comp_objs:
            if comp_obj.get_databk('node1') == old_net_id:
                comp_obj.edit(node1=new_net_id)
            if comp_obj.get_databk('node2') == old_net_id:
                comp_obj.edit(node2=new_net_id)
        # 修改导线的网络id
        for wire_obj in self.conn_objs:
            if wire_obj.get_databk('net_id') == old_net_id:
                wire_obj.edit(net_id=new_net_id)

    def get_net_id_lst(self):
        """
        method: 获取网络id的list
        """
        net_id_lst = []
        for key in self.comp_objs:
            net_id1 = self.comp_objs[key].get_databk('part_data')['node1']
            if net_id1 not in net_id_lst and net_id1 is not None and net_id1 != 0 and net_id1 != 'None':
                net_id_lst.append(net_id1)
            net_id2 = self.comp_objs[key].get_databk('part_data')['node2']
            if net_id2 not in net_id_lst and net_id2 is not None and net_id2 != 0 and net_id2 != 'None':
                net_id_lst.append(net_id2)
        net_id_lst.sort()
        return net_id_lst


class CircuitGUI(Circuit):
    """
    class: 电路GUI
    """
    def __init__(self):
        """
        method: 初始化
        """
        super().__init__()

        # Scroll Canvas
        self.scr_can = None
        # 根窗口
        self.root_win = None
        # 操作台
        self.oper_bar = None
        # 显示打开文件的路径的Label控件
        self.filepath_diplay = None
        # 工具条
        self.tool_bar = None

    def add_component(self,
                      comp_nm,
                      func,
                      **comp_data):
        """
        method: 添加元件
        :param comp_nm: 元件名称
        :param func: 完成添加元件后调用的函数
        :param comp_data:
        :return:
        """
        # 创建新添加元件的对象
        comp_obj = Component(comp_nm)
        # 编辑元件
        comp_obj.edit(part_id=True,
                      id=self.gen_comp_id(comp_nm))
        comp_obj.display(self.canvas)
        comp_obj.move(to_crd=(0, 0))
        comp_obj.slct['part'] = True

        def motion(event):
            # 控件坐标转化为画布坐标
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            comp_obj.move(to_crd=(event_x, event_y))

        def button_1(event):
            # 新元件的对象放入self.comp_objs中
            self.comp_objs[comp_obj.get_databk('part_data')['id']] = comp_obj
            self.source_data['comps_data'][comp_obj.get_databk('part_data')['id']] = comp_obj.get_databk()
            quit_method()
            func()

        def button_3(event):
            comp_obj.clear()
            quit_method()
            func()

        def space(event):
            comp_obj.rotate()

        def quit_method():
            """
            func: 离开该方法, 将bind取消
            """
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
            self.canvas.unbind("<Escape>")
            self.canvas.unbind("<space>")

        self.canvas.focus_set()
        self.canvas.bind("<Motion>", motion)
        self.canvas.bind("<Button-1>", button_1)
        self.canvas.bind("<Button-3>", button_3)
        self.canvas.bind("<Escape>", button_3)
        self.canvas.bind("<space>", space)

    def add_connector(self,
                      func):
        """
        method: 添加连接器
        :param func: 完成添加导线后调用的函数
        :return:
        """
        conn_obj = Connector(comp_objs=self.comp_objs)
        # 导线起点的comp_id，端子号
        sta_id_tmnl = None
        # 导线终点的comp_id, 端子号
        end_id_tmnl = None
        # 中间点的坐标tuple
        mid_points = []
        # 起点的坐标
        sta_x = None
        sta_y = None
        # 左固定点的坐标
        left_x = None
        left_y = None
        # 终点的坐标
        end_x = None
        end_y = None
        # 绘制过程导线的宽度
        tmp_w = 2

        self.canvas.config(cursor='crosshair')

        def button_1(event):
            nonlocal sta_id_tmnl, end_id_tmnl, mid_points, sta_x, sta_y, left_x, left_y, end_x, end_y, tmp_w
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            comp_id_tmnl = conn_obj.tmnl_select((event_x, event_y))
            # 起点
            if comp_id_tmnl and sta_id_tmnl is None:
                print('start point')
                sta_id_tmnl = comp_id_tmnl
                # 获取起点坐标
                crd = point_capture(crd=(event_x, event_y))
                sta_x = crd[0]
                sta_y = crd[1]
                left_x = sta_x
                left_y = sta_y
            # 终点
            elif sta_id_tmnl and comp_id_tmnl:
                print('end point')
                # 记录终点的元件id, 元件端子号
                end_id_tmnl = comp_id_tmnl
                # 获取终点坐标
                crd = point_capture(crd=(event_x, event_y))
                end_x = crd[0]
                end_y = crd[1]
            # 中间点
            elif comp_id_tmnl is None and sta_id_tmnl is not None and end_id_tmnl is not None:
                print('middle point')
                crd = point_capture(crd=(event_x, event_y))
                if crd:
                    mid_points.append(crd[0])
                    mid_points.append(crd[1])
                    self.canvas.create_line(left_x, left_y, crd[0], crd[1], width=tmp_w, tags='temp1')
                    left_x = crd[0]
                    left_y = crd[1]

        def motion(event):
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            nonlocal sta_id_tmnl, end_id_tmnl, left_x, left_y, end_x, end_y
            # 如果起点有了，终点还没有
            if sta_id_tmnl and end_id_tmnl is None:
                crd = point_capture(crd=(event_x, event_y))
                if crd:
                    self.canvas.delete('temp')
                    self.canvas.create_line(left_x, left_y, crd[0], crd[1], width=tmp_w, tags='temp')
            # 如果起点和终点都有了
            elif sta_id_tmnl and end_id_tmnl:
                crd = point_capture(crd=(event_x, event_y))
                if crd:
                    self.canvas.delete('temp')
                    self.canvas.create_line(left_x, left_y, crd[0], crd[1], width=tmp_w, tags='temp')
                    self.canvas.create_line(end_x, end_y, crd[0], crd[1], width=tmp_w, tags='temp')

        def button_3(event):
            self.canvas.config(cursor='arrow')
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Button-3>")
            nonlocal sta_id_tmnl, end_id_tmnl, mid_points
            # 如果终点没有绘制就单击鼠标右键，则已有的导线全部删除
            if end_id_tmnl is None:
                print('terminate')
                self.canvas.delete('temp')
                sta_id_tmnl = None
                end_id_tmnl = None
                mid_points = []
            # 如果起点和终点都已存在，则已有的导线保存
            elif sta_id_tmnl and end_id_tmnl:
                # 求得新导线的net_id
                net_id = self.gen_net_id(comp1_obj=self.comp_objs[sta_id_tmnl[0]],
                                         comp1_tmnl=sta_id_tmnl[1],
                                         comp2_obj=self.comp_objs[end_id_tmnl[0]],
                                         comp2_tmnl=end_id_tmnl[1])
                if net_id is False:
                    print('Can not connect these two terminals!')
                    self.canvas.delete('temp1')
                    self.canvas.delete('temp')
                    return
                # 导线数据编辑
                print(sta_id_tmnl)
                print(end_id_tmnl)
                conn_obj.source_data['wire_data']['sta_comp'] = sta_id_tmnl[0]
                conn_obj.source_data['wire_data']['sta_tmnl'] = sta_id_tmnl[1]
                conn_obj.source_data['wire_data']['end_comp'] = end_id_tmnl[0]
                conn_obj.source_data['wire_data']['end_tmnl'] = end_id_tmnl[1]
                for i in range(int(len(mid_points) / 2)):
                    conn_obj.source_data['wire_data']['mid_p' + str(i + 1) + '_x'] = mid_points[2 * i]
                    conn_obj.source_data['wire_data']['mid_p' + str(i + 1) + '_y'] = mid_points[2 * i + 1]

                data = {'node' + str(sta_id_tmnl[1]): net_id}
                self.comp_objs[sta_id_tmnl[0]].edit(part_id=True, **data)
                data = {'node' + str(end_id_tmnl[1]): net_id}
                self.comp_objs[end_id_tmnl[0]].edit(part_id=True, **data)
                # 将临时导线删除，显示新导线
                self.canvas.delete('temp1')
                self.canvas.delete('temp')
                sta_id_tmnl = None
                end_id_tmnl = None
                mid_points = []
                # 默认文本放置在导线起始位置向下向右偏20的位置
                sta_x, sta_y = conn_obj.wire_obj.get_sta_tmnl_crd()
                conn_obj.text_objs['default'].edit(id='default',
                                                   content=conn_obj.wire_obj.get_data('id'),
                                                   visible=False,
                                                   crd_x=sta_x + 20,
                                                   crd_y=sta_y + 20)
                # 修改wire的id
                conn_id = self.gen_wire_id()
                conn_obj.edit_wire(id=conn_id,
                                   designator=conn_id,
                                   net_id=net_id)
                # 将新的连接器添加进self.conn_objs中
                self.conn_objs[conn_id] = conn_obj
                # 将新的连接器的数据添加进self.cource_data中
                self.source_data['conns_data'][conn_id] = conn_obj.get_databk()
                # 显示新的连接器
                conn_obj.display(self.canvas)
            # 右键后，执行func()函数
            func()

        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", button_1)
        self.canvas.bind("<Motion>", motion)
        self.canvas.bind("<Button-3>", button_3)

    def launch(self):
        """
        method: 启动
        :return:
        """
        self.root_win = CirPage()
        self.oper_bar = ButtonsArea(pframe=self.root_win.frame_title,
                                    btn_lst=['New', 'Open', 'Save', 'SaveAs', 'Close', 'Designator', 'Compile',
                                             'Netlist', 'Run', 'Plot'],
                                    wdg_width=600,
                                    btn_width=[4, 5, 5, 6, 5, 10, 7, 7, 5, 6],
                                    btn_height=1,
                                    num_per_row=20)
        self.oper_bar.disable(btn_lst=['Save', 'SaveAs', 'Close', 'Designator', 'Compile', 'Netlist', 'Run', 'Plot'])
        self.oper_bar.command(btn_nm='New',
                              cal_func=self.state_new)
        self.oper_bar.command(btn_nm='Open',
                              cal_func=lambda x=self.canvas: self.ask_open(canvas=x))
        self.oper_bar.command(btn_nm='Save',
                              cal_func=self.ask_save)
        self.oper_bar.command(btn_nm='SaveAs',
                              cal_func=self.ask_save_as)
        self.oper_bar.command(btn_nm='Close',
                              cal_func=self.close)

        def create_designator():
            self.create_comps_designator()
            self.state_normal()

        self.oper_bar.command(btn_nm='Designator',
                              cal_func=create_designator)

        def comp():
            if self.compile():
                showinfo(title='Information', message='Compile finished!!')
            self.state_normal()

        self.oper_bar.command(btn_nm='Compile',
                              cal_func=comp)

        def disp_netlist():
            page = NormalPage(title='Netlist', width=700, height=500)
            for idx, comp in enumerate(self.get_netlist()):
                label = ttk.Label(page.frame, text=str(comp), justify=tk.LEFT)
                label.grid(row=idx, column=0)
            self.state_normal()

        self.oper_bar.command(btn_nm='Netlist',
                              cal_func=disp_netlist)

        def run():
            netlist = self.get_netlist()
            if netlist:
                self.calculation.add_netlist(netlist,
                                             cir_config=self.source_data['cir_config'])
                self.calculation.main_window()
            self.state_normal()

        self.oper_bar.command(btn_nm='Run',
                              cal_func=run)
        """self.oper_bar.command(btn_nm='Plot',
                              cal_func=self.calculation.plot_config_window)"""

        self.filepath_diplay = ttk.Label(self.root_win.frame_title)
        self.filepath_diplay.grid(row=0, column=1)
        self.filepath_diplay.grid_propagate(0)

        self.tool_bar = ButtonsArea(pframe=self.root_win.frame_tools,
                                    btn_lst=['R', 'C', 'L', 'D', 'Udc', 'Uac', 'Idc', 'Iac', 'GND', 'Wire'],
                                    wdg_width=500,
                                    btn_width=[3, 3, 3, 3, 5, 5, 5, 5, 5, 6],
                                    btn_height=1,
                                    num_per_row=20)
        self.tool_bar.disable()
        self.tool_bar.command(btn_nm='R',
                              cal_func=lambda x='resistor': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='C',
                              cal_func=lambda x='capacitor': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='L',
                              cal_func=lambda x='inductor': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='D',
                              cal_func=lambda x='diode': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Udc',
                              cal_func=lambda x='voltage_dc': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Uac',
                              cal_func=lambda x='voltage_ac': self.state_place_comp(comp_nm=x))
        """self.tool_bar.command(btn_nm='Idc',
                              cal_func=lambda x='current_dc': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Iac',
                              cal_func=lambda x='current_ac': self.state_place_comp(comp_nm=x))"""
        self.tool_bar.command(btn_nm='GND',
                              cal_func=lambda x='ground': self.state_place_comp(comp_nm=x))
        self.tool_bar.command(btn_nm='Wire', cal_func=self.state_draw_conn)
        self.root_win.maintain()

    def state_normal(self):
        """
        method: 普通模式
        :return:
        """
        # 鼠标左键单击回调函数
        def button_1(event):
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            self.select(crd=(event_x, event_y))

        def b1_motion(event):
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            self.move(to_crd=(event_x, event_y))
            self.display()

        def button_3(event):
            event_x = int(self.canvas.canvasx(event.x))
            event_y = int(self.canvas.canvasy(event.y))
            self.pop_rt_menu(event.x, event.y)

        def delete(event):
            self.delete()

        def space(event):
            self.rotate()
            self.display()

        def direct_key(event):
            self.change_ref_dir()

        def control_w(event):
            self.state_draw_conn()

        def control_s(event):
            self.ask_save()

        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", button_1)
        self.canvas.bind("<Button-3>", button_3)
        self.canvas.bind("<B1-Motion>", b1_motion)
        self.canvas.bind("<Delete>", delete)
        self.canvas.bind("<space>", space)
        self.canvas.bind("<Up>", direct_key)
        self.canvas.bind("<Down>", direct_key)
        self.canvas.bind("<Left>", direct_key)
        self.canvas.bind("<Right>", direct_key)
        self.canvas.bind("<Control-w>", control_w)
        self.canvas.bind("<Control-s>", control_s)

    def state_new(self):
        """
        method: 创建一个新的电路
        :return:
        """
        # 关闭之前的文件
        self.close()
        # 将文件中的数据记录下来
        self.file_data = copy.deepcopy(self.source_data)
        self.scr_can = ScrollCanvas(self.root_win.frame_wrk, grid=20)
        self.canvas = self.scr_can.canvas
        self.state_normal()
        self.tool_bar.enable()
        self.oper_bar.enable(['Save', 'SaveAs', 'Close', 'Designator', 'Compile', 'Netlist', 'Run', 'Plot'])

    def state_draw_conn(self):
        """
        method: 绘制导线状态
        :return:
        """
        self.add_connector(self.state_normal)

    def state_place_comp(self,
                         comp_nm):
        """
        method: 放置元件状态
        :param comp_nm: 元件名称
        :return:
        """
        self.add_component(comp_nm=comp_nm,
                           func=self.state_normal)

    def ask_open(self,
                 canvas):
        """
        method: 打开文件
        :return:
        """
        pathfile = fdlg.askopenfilename(defaultextension='.cir',
                                        filetypes=[('.cir', '*.cir'), ('.cmp', '*.cmp')])
        if pathfile:
            self.state_new()
            self.cir_name = os.path.basename(pathfile).replace('.cir', '')
            self.open(path=os.path.dirname(pathfile),
                      file=os.path.basename(pathfile))
            self.display(canvas)
            self.state_normal()
            self.filepath_diplay.config(text=self.file_obj.source_cirfilepath)

    def ask_save(self):
        """
        method: 保存文件
        :return:
        """
        if self.scr_can:
            if self.file_obj.source_cirfilepath:
                self.save()
            else:
                pathfile = fdlg.asksaveasfilename(defaultextension='.cir',
                                                  filetypes=[('.cir', '*.cir'), ('.cmp', '*.comp')])
                if pathfile:
                    self.save(filepath=pathfile)
        else:
            msg.showerror(title='warning!', message='The circuit is not exist!')
        self.state_normal()

    def ask_save_as(self):
        """
        method: 保存文件
        :return:
        """
        if self.scr_can:
            pathfile = fdlg.asksaveasfilename(defaultextension='.cir',
                                              filetypes=[('.cir', '*.cir'), ('.cmp', '*.comp')])
            self.save(filepath=pathfile)
        else:
            msg.showerror(title='warning!', message='The circuit is not exist!')
        self.state_normal()

    def close(self):
        """
        method: 关闭文件
        :return:
        """
        answer = False
        if self.file_data != self.source_data and self.file_data is not None:
            answer = askyesnocancel(title='warning', message='The file has been changed, do you want to save?')
        if answer is True:
            self.ask_save()
        elif answer is False:
            super().close()
            self.tool_bar.disable()
            self.oper_bar.disable(['Save', 'SaveAs', 'Close', 'Designator', 'Compile', 'Netlist', 'Run', 'Plot'])
            self.filepath_diplay.config(text='')
            if self.scr_can:
                self.scr_can.destroy()

    def change_ref_dir(self):
        """
        method: 更改参考方向
        :param x:
        :param y:
        :return:
        """
        for key in self.comp_objs:
            self.comp_objs[key].change_ref_dir()


if __name__ == '__main__':
    cir_gui = CircuitGUI()
    cir_gui.launch()
