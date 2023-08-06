# coding=utf-8
"""
该模块是用于绘制相量图、电气图等
"""
import turtle
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd


def draw_phasors(tt=None,
                 ph_var=None,
                 origin=None,
                 name='默认相量',
                 zoom=1,
                 txt_displace=None,
                 arrow_len_ratio=1,
                 arrow_ang=20):
    """
    函数：绘制相量图
    :param ph_var:相量变量[Re+Im*j]
    :param origin:相量原点，[x, y]
    :param name:相量名称
    :param zoom:放大缩小系数
    :param txt_displace:文字位置位移，[dx,dy]（相量名称默认显示在相量尾端，可标注移动方向）
    :param arrow_len_ratio:箭头长度比例
    :param arrow_ang:箭头夹角
    :return:
    """
    """判断参数"""
    if ph_var is None:
        ph_var = 1 + 1j
    if origin is None:
        origin = [0, 0]
    if txt_displace is None:
        txt_displace = [0, 0]

    """配置turtle"""
    # 隐藏turtle图标（箭头）
    tt.hideturtle()
    # 定义turtle绘制速度
    tt.speed(speed=0)

    """绘制相量"""
    # 画笔复位
    tt.penup()
    tt.goto(0, 0)
    tt.pendown()
    # 绘制相量
    angle = 180 / math.pi * np.angle(ph_var)
    x = ph_var.real * zoom
    y = ph_var.imag * zoom
    tt.setheading(to_angle=angle)
    tt.goto(x, y)
    # 绘制箭头
    tt.begin_fill()
    tt.setheading(to_angle=angle + 180 - arrow_ang/2)
    tt.forward(10*arrow_len_ratio)
    tt.setheading(to_angle=angle + 270)
    tt.forward(10*arrow_len_ratio*math.sin(arrow_ang/2*np.pi/180)*2)
    tt.goto(x, y)
    tt.fillcolor('black')
    tt.end_fill()
    # 绘制文字
    tt.penup()
    tt.goto(x + txt_displace[0], y + txt_displace[1])
    tt.pendown()
    tt.write(name, align='left')
    # 画完收笔
    tt.penup()


if __name__ == '__main__':
    tt1 = turtle.Turtle()
    ph1 = 30 + 0j
    ph2 = 10 - 50j
    ph3 = -100 + 20j
    ph4 = -100 - 2j
    draw_phasors(tt=tt1,
                 ph_var=ph1,
                 zoom=2)
    draw_phasors(tt=tt1,
                 ph_var=ph2,
                 zoom=2,
                 txt_displace=[5, 0])
    draw_phasors(tt=tt1,
                 ph_var=ph3,
                 zoom=2)
    draw_phasors(tt=tt1,
                 ph_var=ph4,
                 zoom=2)
    tt1.screen.mainloop()
