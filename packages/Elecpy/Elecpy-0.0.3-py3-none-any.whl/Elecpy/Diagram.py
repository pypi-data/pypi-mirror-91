# coding=utf-8
"""
该模块包含了在tkinter的Canvas控件上绘制电路元件图的函数，如draw_transistor, draw_capacitor, draw_inductor等
"""
import tkinter as tk
from Elecpy.Tools import *
import tkinter.font as tkFont


def draw_tmnl_circle(id='t?',
                     tmnls_crd=((0, 0), (0, 0)),
                     canvas=None):
    """
    func: 绘制一个元件的端子处的圆形
    :param id: 元件id
    :param tmnls_crd: 元件端子的坐标, tuple((x1, y1), (x2, y2))
    :param canvas: 画布
    :return: None
    """
    for crd in tmnls_crd:
        cen_x = crd[0]
        cen_y = crd[1]
        canvas.create_oval(cen_x - 2, cen_y - 2, cen_x + 2, cen_y + 2, outline='black', fill='black',
                           width=1, activefill='green', activeoutline='green', activewidth=8, tag=id)


def draw_resistor_rect(id='R?',
                       cnt_crd=None,
                       angle=0,
                       canvas=None,
                       slct=False,
                       tmnls_vol=None,
                       max_vol=None):
    """
    func: 绘制电阻, 矩形型
    :param id: 电阻id，默认R?
    :param value: 电阻阻值，单位Ω
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param tmnls_vol:
    :param max_vol: 整个电路中的最大电压
    :return:
    """
    """输入变量"""
    if tmnls_vol is None:
        tmnls_vol = ('0V', '0V')
    if max_vol is None:
        max_vol = '100V'
    if cnt_crd is None:
        cnt_crd = (400, 400)

    """绘制参数定义"""
    # 电阻中间部分的长度和宽度
    length = 40
    width = 10
    # 引脚长度
    pin_length = 20
    # 线条和颜色
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        rect_color = 'blue'
    else:
        lwidth = 2
        if float(tmnls_vol[0].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if float(tmnls_vol[1].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            rect_color = 'red'
        else:
            rect_color = 'black'
    # 图形外方框
    square_x = length / 2
    square_y = width / 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y),
                                         cnt_crd=(0, 0),
                                         angle=angle)

    """绘制过程"""
    # 绘制中间的矩形
    # to_agl是90的偶数倍，flag=0，反之，flag=1
    x0 = cnt_crd[0] - (length / 2)
    y0 = cnt_crd[1] - (width / 2)
    x1 = cnt_crd[0] + (length / 2)
    y1 = cnt_crd[1] + (width / 2)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_rectangle(x0, y0, x1, y1, outline=rect_color, tags=id, width=lwidth)

    # 绘制引脚1
    x1_0 = cnt_crd[0] - (length / 2 + pin_length)
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0] - (length / 2)
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin1_color, width=lwidth, tags=id)

    # 绘制引脚2
    x2_0 = cnt_crd[0] + (length / 2 + pin_length)
    y2_0 = cnt_crd[1]
    x2_1 = cnt_crd[0] + (length / 2)
    y2_1 = cnt_crd[1]
    x2_0, y2_0 = coord_mirr_rota(orig_crd=(x2_0, y2_0), cnt_crd=cnt_crd, angle=angle)
    x2_1, y2_1 = coord_mirr_rota(orig_crd=(x2_1, y2_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x2_0, y2_0, x2_1, y2_1, fill=pin2_color, width=lwidth, tags=id)

    """返回开关两端子的坐标"""
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': ((x1_0, y1_0), (x2_0, y2_0))}


def draw_resistor_wave(id='R?',
                       cnt_crd=None,
                       angle=0,
                       canvas=None,
                       slct=False,
                       tmnls_vol=None,
                       max_vol=None):
    """
    func: 绘制电阻, 波浪折线型
    :param id: 电阻id，默认R?
    :param value: 电阻阻值，单位Ω
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param tmnls_vol:
    :param max_vol: 整个电路中的最大电压
    :return:
    """
    """输入变量"""
    if tmnls_vol is None:
        tmnls_vol = ('0V', '0V')
    if max_vol is None:
        max_vol = '100V'
    if cnt_crd is None:
        cnt_crd = (400, 400)

    """绘制参数定义"""
    # 电阻中间部分的长度和宽度
    length = 40
    width = 15
    # 波浪线数量
    wave_num = 4
    # 引脚长度
    pin_length = 20
    # 线条和颜色
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        wave_color = 'blue'
    else:
        lwidth = 2
        if float(tmnls_vol[0].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if float(tmnls_vol[1].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            wave_color = 'red'
        else:
            wave_color = 'black'
    # 图形外方框
    square_x = length / 2
    square_y = width / 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y),
                                         cnt_crd=(0, 0),
                                         angle=angle)

    """绘制过程"""
    # 绘制中间的波浪折线
    wave_len = int(length/wave_num)
    for i in range(wave_num):
        x0 = cnt_crd[0] - int(length / 2) + i * wave_len
        y0 = cnt_crd[1]
        x1 = x0 + int(wave_len / 4)
        y1 = y0 - int(width/2)
        x2 = x0 + int(wave_len * 3 / 4)
        y2 = y0 + int(width/2)
        x3 = x0 + wave_len
        y3 = y0
        x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
        x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
        x2, y2 = coord_mirr_rota(orig_crd=(x2, y2), cnt_crd=cnt_crd, angle=angle)
        x3, y3 = coord_mirr_rota(orig_crd=(x3, y3), cnt_crd=cnt_crd, angle=angle)
        canvas.create_line(x0, y0, x1, y1, x2, y2, x3, y3, fill=wave_color, tags=id, width=lwidth)

    # 绘制引脚1
    x1_0 = cnt_crd[0] - (length / 2 + pin_length)
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0] - (length / 2)
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin1_color, width=lwidth, tags=id)

    # 绘制引脚2
    x2_0 = cnt_crd[0] + (length / 2 + pin_length)
    y2_0 = cnt_crd[1]
    x2_1 = cnt_crd[0] + (length / 2)
    y2_1 = cnt_crd[1]
    x2_0, y2_0 = coord_mirr_rota(orig_crd=(x2_0, y2_0), cnt_crd=cnt_crd, angle=angle)
    x2_1, y2_1 = coord_mirr_rota(orig_crd=(x2_1, y2_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x2_0, y2_0, x2_1, y2_1, fill=pin2_color, width=lwidth, tags=id)

    """返回开关两端子的坐标"""
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': ((x1_0, y1_0), (x2_0, y2_0))}


def draw_capacitor(id='C?',
                   cnt_crd=None,
                   angle=0,
                   canvas=None,
                   slct=False,
                   tmnls_vol=None,
                   max_vol=None):
    """
    func: 绘制电容
    :param id:
    :param value:
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param tmnls_vol:
    :param max_vol:
    :return:
    """
    """输入变量"""
    if cnt_crd is None:
        cnt_crd = (400, 400)
    if max_vol is None:
        max_vol = '100V'
    if tmnls_vol is None:
        tmnls_vol = ('0V', '0V')

    """绘图变量"""
    # 两极间的距离
    dstn = 10
    # 极板长度
    len = 30
    # 引脚长度
    pin_len = 15
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
    else:
        lwidth = 2
        if float(tmnls_vol[0].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if float(tmnls_vol[1].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'

    """绘制"""
    # 绘制中间的双竖
    x0 = cnt_crd[0] - (dstn / 2)
    y0 = cnt_crd[1] - (len / 2)
    x1 = cnt_crd[0] - (dstn / 2)
    y1 = cnt_crd[1] + (len / 2)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin1_color, tags=id, width=lwidth)

    x0 = cnt_crd[0] + (dstn / 2)
    y0 = cnt_crd[1] - (len / 2)
    x1 = cnt_crd[0] + (dstn / 2)
    y1 = cnt_crd[1] + (len / 2)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin2_color, tags=id, width=lwidth)

    # 绘制引脚1
    x1_0 = cnt_crd[0] - (dstn / 2 + pin_len)
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0] - (dstn / 2)
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin1_color, width=lwidth, tags=id)

    # 绘制引脚2
    x2_0 = cnt_crd[0] + (dstn / 2 + pin_len)
    y2_0 = cnt_crd[1]
    x2_1 = cnt_crd[0] + (dstn / 2)
    y2_1 = cnt_crd[1]
    x2_0, y2_0 = coord_mirr_rota(orig_crd=(x2_0, y2_0), cnt_crd=cnt_crd, angle=angle)
    x2_1, y2_1 = coord_mirr_rota(orig_crd=(x2_1, y2_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x2_0, y2_0, x2_1, y2_1, fill=pin2_color, width=lwidth, tags=id)

    # square数据，用来确定选中设备的区域
    square_x = dstn/2
    square_y = len/2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    """返回开关两端子的坐标"""
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': ((x1_0, y1_0), (x2_0, y2_0))}


def draw_inductor(id='R?',
                  cnt_crd=None,
                  angle=0,
                  canvas=None,
                  slct=False,
                  tmnls_vol=None,
                  max_vol=None):
    """
    func: 绘制电感
    :param id: 电感id，默认L?
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param tmnls_vol:
    :param max_vol: 整个电路中的最大电压
    :return:
    """
    """输入变量"""
    if tmnls_vol is None:
        tmnls_vol = ('0V', '0V')
    if max_vol is None:
        max_vol = '100V'
    if cnt_crd is None:
        cnt_crd = (400, 400)

    """绘制参数定义"""
    # 电感中间部分的长度和宽度
    length = 60
    # 波浪线数量
    wave_num = 4
    # 引脚长度
    pin_length = 10
    # 线条和颜色
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        wave_color = 'blue'
    else:
        lwidth = 1.5
        if float(tmnls_vol[0].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if float(tmnls_vol[1].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            wave_color = 'red'
        else:
            wave_color = 'black'
    # 图形外方框
    square_x = length / 2
    square_y = int(length/wave_num)
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    """绘制过程"""
    # 绘制中间的波浪折线
    wave_len = int(length/wave_num)
    for i in range(wave_num):
        x0 = cnt_crd[0] - int(length / 2) + i * wave_len
        y0 = cnt_crd[1] - wave_len / 2
        x1 = x0 + wave_len
        y1 = cnt_crd[1] + wave_len / 2
        x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
        x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
        canvas.create_arc(x0, y0, x1, y1, start=angle, extent=180, outline=wave_color, tags=id, width=lwidth,
                          style=tk.ARC)

    # 绘制引脚1
    x1_0 = cnt_crd[0] - (length / 2 + pin_length)
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0] - (length / 2)
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin1_color, width=lwidth, tags=id)

    # 绘制引脚2
    x2_0 = cnt_crd[0] + (length / 2 + pin_length)
    y2_0 = cnt_crd[1]
    x2_1 = cnt_crd[0] + (length / 2)
    y2_1 = cnt_crd[1]
    x2_0, y2_0 = coord_mirr_rota(orig_crd=(x2_0, y2_0), cnt_crd=cnt_crd, angle=angle)
    x2_1, y2_1 = coord_mirr_rota(orig_crd=(x2_1, y2_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x2_0, y2_0, x2_1, y2_1, fill=pin2_color, width=lwidth, tags=id)

    """返回开关两端子的坐标"""
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': ((x1_0, y1_0), (x2_0, y2_0))}


def draw_source_dc(id='Udc?',
                   cnt_crd=None,
                   angle=0,
                   canvas=None,
                   slct=False,
                   tmnls_vol=None,
                   max_vol=None):
    """
    func: 绘制直流电源
    :param id: 电源id，默认DC?
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param tmnls_vol:
    :param max_vol: 整个电路中的最大电压
    :return:
    """
    """输入变量"""
    if tmnls_vol is None:
        tmnls_vol = ('0V', '0V')
    if max_vol is None:
        max_vol = '100V'
    if cnt_crd is None:
        cnt_crd = (400, 400)

    """绘制参数定义"""
    # 圆形半径
    radius = 20
    # 引脚长度
    pin_length = 20
    # 线条和颜色
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        circle_color = 'blue'
    else:
        lwidth = 1.5
        if float(tmnls_vol[0].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if float(tmnls_vol[1].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            circle_color = 'red'
        else:
            circle_color = 'black'
    # 图形外方框
    square_x = radius * 2
    square_y = radius * 2

    """绘制过程"""
    # 绘制中间的圆形
    x0 = cnt_crd[0] - radius
    y0 = cnt_crd[1] - radius
    x1 = cnt_crd[0] + radius
    y1 = cnt_crd[1] + radius
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_oval(x0, y0, x1, y1, outline=circle_color, width=lwidth, tags=id)

    # 绘制+、-号
    x0 = cnt_crd[0] - radius / 2
    y0 = cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    canvas.create_text(x0, y0, text='+', tags=id, fill=circle_color)
    x0 = cnt_crd[0] + radius / 2
    y0 = cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    canvas.create_text(x0, y0, text='-', tags=id, fill=circle_color)

    # 绘制引脚1
    x1_0 = cnt_crd[0] - (radius + pin_length)
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0] - radius
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin1_color, width=lwidth, tags=id)

    # 绘制引脚2
    x2_0 = cnt_crd[0] + (radius + pin_length)
    y2_0 = cnt_crd[1]
    x2_1 = cnt_crd[0] + radius
    y2_1 = cnt_crd[1]
    x2_0, y2_0 = coord_mirr_rota(orig_crd=(x2_0, y2_0), cnt_crd=cnt_crd, angle=angle)
    x2_1, y2_1 = coord_mirr_rota(orig_crd=(x2_1, y2_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x2_0, y2_0, x2_1, y2_1, fill=pin2_color, width=lwidth, tags=id)

    """返回开关两端子的坐标"""
    return {'square': (abs(square_x), abs(square_y)), 'tmnls_crd': ((x1_0, y1_0), (x2_0, y2_0))}


def draw_source_ac(id='Uac?',
                   cnt_crd=None,
                   angle=0,
                   canvas=None,
                   slct=False,
                   tmnls_vol=None,
                   max_vol=None):
    """
    func: 绘制交流电源
    :param id:
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param tmnls_vol:
    :param max_vol:
    :return:
    """
    """输入变量"""
    if tmnls_vol is None:
        tmnls_vol = ('0V', '0V')
    if max_vol is None:
        max_vol = '100V'
    if cnt_crd is None:
        cnt_crd = (400, 400)

    """绘制参数定义"""
    # 圆形半径
    radius = 20
    # 引脚长度
    pin_length = 20
    # 线条和颜色
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        circle_color = 'blue'
    else:
        lwidth = 1.5
        if float(tmnls_vol[0].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if float(tmnls_vol[1].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            circle_color = 'red'
        else:
            circle_color = 'black'
    # 图形外方框
    square_x = radius * 2
    square_y = radius * 2

    """绘制过程"""
    # 绘制中间的圆形
    x0 = cnt_crd[0] - radius
    y0 = cnt_crd[1] - radius
    x1 = cnt_crd[0] + radius
    y1 = cnt_crd[1] + radius
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_oval(x0, y0, x1, y1, outline=circle_color, width=lwidth, tags=id)

    # 绘制正弦号
    x0 = cnt_crd[0] - radius / 2
    y0 = radius / 4 * sin((x0 - cnt_crd[0] - radius/2) * 2 * pi / radius) + cnt_crd[1]
    x1 = x0 + radius / 4
    y1 = radius / 4 * sin((x1 - cnt_crd[0] - radius/2) * 2 * pi / radius) + cnt_crd[1]
    x2 = x1 + radius / 4
    y2 = radius / 4 * sin((x2 - cnt_crd[0] - radius/2) * 2 * pi / radius) + cnt_crd[1]
    x3 = x2 + radius / 4
    y3 = radius / 4 * sin((x3 - cnt_crd[0] - radius/2) * 2 * pi / radius) + cnt_crd[1]
    x4 = x3 + radius / 4
    y4 = radius / 4 * sin((x4 - cnt_crd[0] - radius/2) * 2 * pi / radius) + cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle+90)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle+90)
    x2, y2 = coord_mirr_rota(orig_crd=(x2, y2), cnt_crd=cnt_crd, angle=angle+90)
    x3, y3 = coord_mirr_rota(orig_crd=(x3, y3), cnt_crd=cnt_crd, angle=angle+90)
    x4, y4 = coord_mirr_rota(orig_crd=(x4, y4), cnt_crd=cnt_crd, angle=angle+90)
    canvas.create_line(x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, fill=circle_color, width=lwidth, smooth=True, tags=id)

    # 绘制引脚1
    x1_0 = cnt_crd[0] - (radius + pin_length)
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0] - radius
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin1_color, width=lwidth, tags=id)

    # 绘制引脚2
    x2_0 = cnt_crd[0] + (radius + pin_length)
    y2_0 = cnt_crd[1]
    x2_1 = cnt_crd[0] + radius
    y2_1 = cnt_crd[1]
    x2_0, y2_0 = coord_mirr_rota(orig_crd=(x2_0, y2_0), cnt_crd=cnt_crd, angle=angle)
    x2_1, y2_1 = coord_mirr_rota(orig_crd=(x2_1, y2_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x2_0, y2_0, x2_1, y2_1, fill=pin2_color, width=lwidth, tags=id)

    """返回开关两端子的坐标"""
    return {'square': (abs(square_x), abs(square_y)), 'tmnls_crd': ((x1_0, y1_0), (x2_0, y2_0))}


def draw_switch(id='S?',
                cnt_crd=None,
                angle=0,
                canvas=None,
                swst='open',
                slct=False,
                tmnls_vol=None,
                max_vol=None):
    """
    func: 绘制开关
    :param id: 开关id
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param swst: 开关状态, 'open', 'close'
    :param slct:
    :param tmnls_vol:
    :param max_vol:
    :return:
    """
    """输入变量"""
    if tmnls_vol is None:
        tmnls_vol = ('0V', '0V')
    if max_vol is None:
        max_vol = '100V'
    if cnt_crd is None:
        cnt_crd = (400, 400)

    """内部变量"""
    length = 30
    width = 16
    # 开关的臂长
    arm_len = length * 1.1
    # 引脚长度
    pin_len = 15
    if float(tmnls_vol[0].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
        pin1_color = 'red'
    else:
        pin1_color = 'black'
    if float(tmnls_vol[1].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
        pin2_color = 'red'
    else:
        pin2_color = 'black'
    if pin1_color != pin2_color and swst == 'close':
        raise TypeError('状态错误：开关合位，两端电位不同！！')
    if swst == 'open':
        ang = 25
    else:
        ang = 10
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
    else:
        lwidth = 2

    """绘制"""
    # 绘制中间的刀闸样式
    x0 = cnt_crd[0] - length / 2
    y0 = cnt_crd[1] - width / 2
    x1 = cnt_crd[0] - length / 2
    y1 = cnt_crd[1] + width / 2
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin1_color, width=lwidth, tags=id)

    x0 = cnt_crd[0] + length / 2
    y0 = cnt_crd[1]
    x1 = x0 - length * cos_deg(ang)
    y1 = y0 - length * sin_deg(ang)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin2_color, width=lwidth, tags=id)

    # 绘制引脚1
    pin_len = 25
    x1_0 = cnt_crd[0] - (length / 2 + pin_len)
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0] - (length / 2)
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin1_color, width=lwidth, tags=id)

    # 绘制引脚2
    x2_0 = cnt_crd[0] + (length / 2 + pin_len)
    y2_0 = cnt_crd[1]
    x2_1 = cnt_crd[0] + (length / 2)
    y2_1 = cnt_crd[1]
    x2_0, y2_0 = coord_mirr_rota(orig_crd=(x2_0, y2_0), cnt_crd=cnt_crd, angle=angle)
    x2_1, y2_1 = coord_mirr_rota(orig_crd=(x2_1, y2_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x2_0, y2_0, x2_1, y2_1, fill=pin2_color, width=lwidth, tags=id)

    # square数据，用来确定选中设备的区域
    square_x = length/2
    square_y = width/2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    """返回开关两端子的坐标"""
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': ((x1_0, y1_0), (x2_0, y2_0))}


def draw_ground(id='G?',
                cnt_crd=None,
                angle=0,
                canvas=None,
                slct=False):
    """
    func: 绘制接地
    :param id:
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :return:
    """
    """输入变量"""
    if cnt_crd is None:
        cnt_crd = (400, 400)

    """绘图参数"""
    # 最长一条横的长度
    length = 30
    # 三条横线间的距离
    intvl = 8
    if slct:
        lwidth = 4
        pin_color = 'blue'
    else:
        lwidth = 2
        pin_color = 'black'

    """绘制"""
    # 绘制三横
    x0 = cnt_crd[0]
    y0 = cnt_crd[1] - length / 2
    x1 = cnt_crd[0]
    y1 = cnt_crd[1] + length / 2
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin_color, width=lwidth, tags=id)

    x0 = cnt_crd[0] + intvl
    y0 = cnt_crd[1] - length / 4
    x1 = cnt_crd[0] + intvl
    y1 = cnt_crd[1] + length / 4
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin_color, width=lwidth, tags=id)

    x0 = cnt_crd[0] + intvl * 2
    y0 = cnt_crd[1] - length / 8
    x1 = cnt_crd[0] + intvl * 2
    y1 = cnt_crd[1] + length / 8
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=pin_color, width=lwidth, tags=id)

    # 绘制引脚
    pin_len = 20
    x1_0 = cnt_crd[0] - pin_len
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0]
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin_color, width=lwidth, tags=id)

    # square数据，用来确定选中设备的区域
    square_x = length
    square_y = intvl * 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    """返回端子的坐标"""
    return {'square': (abs(square_x), abs(square_y)), 'tmnls_crd': ((x1_0, y1_0),)}


def draw_diode(id='Us?',
               cnt_crd=None,
               angle=0,
               canvas=None,
               slct=False,
               tmnls_vol=None,
               max_vol=None,
               fill=False):
    """
    func: 绘制二极管
    :param id:
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param tmnls_vol:
    :param max_vol:
    :param fill: 三角形内部是否填充，默认不填充
    :return:
    """
    """输入变量"""
    if tmnls_vol is None:
        tmnls_vol = ('0V', '0V')
    if max_vol is None:
        max_vol = '100V'
    if cnt_crd is None:
        cnt_crd = (400, 400)

    """绘制参数定义"""
    # 二极管中间部分的长度和宽度
    length = 20
    width = 20
    # 引脚长度
    pin_length = 30
    # 线条和颜色
    if slct:
        lwidth = 4
        pin1_color = 'blue'
        pin2_color = 'blue'
        tri_line_color = 'blue'
        if fill:
            tri_fill_color = 'blue'
        else:
            tri_fill_color = 'white'
    else:
        lwidth = 2
        if float(tmnls_vol[0].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin1_color = 'red'
        else:
            pin1_color = 'black'
        if float(tmnls_vol[1].replace('V', '')) / float(max_vol.replace('V', '')) > 0.5:
            pin2_color = 'red'
        else:
            pin2_color = 'black'
        if pin1_color == 'red' or pin2_color == 'red':
            tri_line_color = 'red'
            if fill:
                tri_fill_color = 'red'
            else:
                tri_fill_color = 'white'
        else:
            tri_line_color = 'black'
            if fill:
                tri_fill_color = 'black'
            else:
                tri_fill_color = 'white'
    # 图形外方框
    square_x = length / 2
    square_y = width / 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    """绘制过程"""
    # 绘制中间的三角形
    x0 = cnt_crd[0] + (length / 2)
    y0 = cnt_crd[1]
    x1 = cnt_crd[0] - (length / 2)
    y1 = cnt_crd[1] - (width / 2)
    x2 = cnt_crd[0] - (length / 2)
    y2 = cnt_crd[1] + (width / 2)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    x2, y2 = coord_mirr_rota(orig_crd=(x2, y2), cnt_crd=cnt_crd, angle=angle)
    canvas.create_polygon(x0, y0, x1, y1, x2, y2, fill=tri_fill_color, outline=tri_line_color, tags=id, width=lwidth)

    # 绘制三角旁的一竖
    x0 = cnt_crd[0] + (length / 2)
    y0 = cnt_crd[1] - (width / 2)
    x1 = cnt_crd[0] + (length / 2)
    y1 = cnt_crd[1] + (width / 2)
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=tri_line_color, tags=id, width=lwidth)

    # 绘制引脚1
    x1_0 = cnt_crd[0] - (length / 2 + pin_length)
    y1_0 = cnt_crd[1]
    x1_1 = cnt_crd[0] - (length / 2)
    y1_1 = cnt_crd[1]
    x1_0, y1_0 = coord_mirr_rota(orig_crd=(x1_0, y1_0), cnt_crd=cnt_crd, angle=angle)
    x1_1, y1_1 = coord_mirr_rota(orig_crd=(x1_1, y1_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x1_0, y1_0, x1_1, y1_1, fill=pin1_color, width=lwidth, tags=id)

    # 绘制引脚2
    x2_0 = cnt_crd[0] + (length / 2 + pin_length)
    y2_0 = cnt_crd[1]
    x2_1 = cnt_crd[0] + (length / 2)
    y2_1 = cnt_crd[1]
    x2_0, y2_0 = coord_mirr_rota(orig_crd=(x2_0, y2_0), cnt_crd=cnt_crd, angle=angle)
    x2_1, y2_1 = coord_mirr_rota(orig_crd=(x2_1, y2_1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x2_0, y2_0, x2_1, y2_1, fill=pin2_color, width=lwidth, tags=id)

    """返回开关两端子的坐标"""
    return {'square': (abs(square_x * 2), abs(square_y * 2)), 'tmnls_crd': ((x1_0, y1_0), (x2_0, y2_0))}


def draw_arrow(id='a?',
               cnt_crd=None,
               angle=0,
               canvas=None,
               slct=False,
               color='black',
               tail_len=10,
               arrw_len=20,
               arrw_wid=5):
    """
    func: 绘制一个箭头
    :param id:
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param color:
    :param tail_len: 尾巴长度
    :param arrw_len: 箭头长度
    :param arrw_wid: 箭头宽度
    :return:
    """
    if cnt_crd is None:
        cnt_crd = (400, 400)

    """绘图参数"""
    if slct:
        lwidth = 4
        color = 'blue'
    else:
        lwidth = 2
        color = color

    """绘制"""
    # 绘制横
    x0 = cnt_crd[0] - tail_len
    y0 = cnt_crd[1]
    x1 = cnt_crd[0] + arrw_len
    y1 = cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    canvas.create_line(x0, y0, x1, y1, fill=color, width=lwidth, tags=id,
                       arrow=tk.LAST, arrowshape=(arrw_len, sqrt(arrw_wid**2+arrw_len**2), arrw_wid))

    # 图形外方框
    square_x = (tail_len + arrw_len) / 2
    square_y = arrw_wid
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    """返回包围图形的外框尺寸: (x, y)"""
    return {'square': (abs(square_x * 2), abs(square_y * 2))}


def draw_pn(id='Gph-?',
            cnt_crd=None,
            angle=0,
            canvas=None,
            slct=False,
            distance=10,
            size=8,
            color='black'):
    """
    func: 绘制一个正负号
    :param id:
    :param cnt_crd:
    :param angle:
    :param canvas:
    :param slct:
    :param distance: 正负号的距离
    :param size: 正负号的尺寸
    :return:
    """
    if cnt_crd is None:
        cnt_crd = (400, 400)

    """绘图参数"""
    # 箭头长度和宽度
    if slct:
        size = 10
        color = 'blue'
    else:
        size = size
        color = color

    """绘制"""
    x0 = cnt_crd[0] - distance / 2
    y0 = cnt_crd[1]
    x1 = cnt_crd[0] + distance / 2
    y1 = cnt_crd[1]
    x0, y0 = coord_mirr_rota(orig_crd=(x0, y0), cnt_crd=cnt_crd, angle=angle)
    x1, y1 = coord_mirr_rota(orig_crd=(x1, y1), cnt_crd=cnt_crd, angle=angle)
    font = tkFont.Font(size=size,
                       weight='bold')
    canvas.create_text(x0,
                       y0,
                       text='+',
                       font=font,
                       tag=id,
                       fill=color,
                       activefill='blue')
    canvas.create_text(x1,
                       y1,
                       text='-',
                       font=font,
                       tag=id,
                       fill=color,
                       activefill='blue')

    # 图形外方框
    square_x = distance / 2
    square_y = (size + 6) / 2
    square_x, square_y = coord_mirr_rota(orig_crd=(square_x, square_y), cnt_crd=(0, 0), angle=angle)

    """返回包围图形的外框尺寸: (x, y)"""
    return {'square': (abs(square_x * 2), abs(square_y * 2))}


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1000x800')
    frm = tk.Frame(root, width=1400, height=800)
    frm.grid(row=0, column=0)

    bcanv = tk.Canvas(frm, width=1000, height=800)
    bcanv.grid(row=0, column=0)
    draw_pn(id='D-1',
            cnt_crd=None,
            angle=0,
            distance=20,
            canvas=bcanv,
            slct=False)

    root.mainloop()
