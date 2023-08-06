# coding=utf-8
"""
该模块定义了一些工具函数，如基于角度的三角函数，坐标变换，主变绕组联结组别识别等
"""
from math import *
import os
import pandas as pd


def cos_deg(angle=None):
    """
    func：计算某个以度表示的角度值的余弦值
    :param angle:以度表示的角度值
    :return:余弦值
    """
    if angle is not None:
        return cos(radians(angle))


def sin_deg(angle=None):
    """
    func：计算某个以度表示的角度值的正弦值
    :param angle:以度表示的角度值
    :return:正弦值
    """
    if angle is not None:
        return sin(radians(angle))


def tan_deg(angle=None):
    """
    func：计算某个以度表示的角度值的正切值
    :param angle:以度表示的角度值
    :return:正切值
    """
    if angle is not None:
        return tan(radians(angle))


def coord_mirr_rota(orig_crd=None,
                    cnt_crd=None,
                    mirr=None,
                    angle=0):
    """
    func: 在直角坐标系（左上顶点为O点，向右x+方向，向下为y+方向）内，某点围绕中心点先镜像后顺时针旋转时，其坐标的变换。
    假设一个点的初始坐标为orig_crd，将其围绕中心点(坐标为cnt_crd)先镜像后顺时针旋转angle度，计算该点的新坐标
    :param orig_crd: 被旋转点原坐标
    :param cnt_crd: 中心点坐标
    :param mirr: 镜像, None: 不镜像, 'x': x轴镜像, 'y': y轴镜像, 'xy': x轴和y轴同时镜像
    :param angle: 顺时针旋转角度, 0°, 90°, 180°, 270°
    :return: 旋转后的新坐标, (x, y)
    """
    # 如果点与中心点重合
    if orig_crd[0] == cnt_crd[0] and orig_crd[1] == cnt_crd[1]:
        new_coord = orig_crd
    # 如果点与中心点不重合
    else:
        # 获取距离
        x_dstn = orig_crd[0] - cnt_crd[0]
        y_dstn = orig_crd[1] - cnt_crd[1]
        # 镜像坐标变换
        if mirr == 'x':
            y_dstn = -y_dstn
        elif mirr == 'y':
            x_dstn = -x_dstn
        elif mirr == 'xy' or mirr == 'yx':
            y_dstn = -y_dstn
            x_dstn = -x_dstn
        # 顺时针旋转坐标变换
        new_coord = (cnt_crd[0] + round(x_dstn * cos_deg(angle) - y_dstn * sin_deg(angle)),
                     cnt_crd[1] + round(y_dstn * cos_deg(angle) + x_dstn * sin_deg(angle)))

    return new_coord


def winding_info(conn_set='YNyn0d11'):
    """
    method: 将联结组别字符串转换为字典信息保存
    :param conn_set: 联结组别(connection set)
    :return: dict({'绕组数': 3, '绕组1': 'y', '绕组1中性点': True, '绕组2': 'y', '绕组2中性点': True, '绕组3': 'd',
    '绕组1方向': 0, '绕组2方向': 0, '绕组3方向': 11 })
    """
    wind_info = {}
    # 绕组数
    num = conn_set.count('Y') + conn_set.count('y') + conn_set.count('d')
    wind_info['绕组数'] = num

    # 联结组别字符串按绕组分成几个部分，生成list(['YN00', 'yn00', 'd11'])
    conn_set_lst = []
    wind_i = 0
    if conn_set[0] == 'Y' or conn_set[0] == 'y' or conn_set[0] == 'd' or conn_set[0] == 'D':
        conn_set_lst.append(conn_set[0])
    for i in range(1, len(conn_set)):
        if conn_set[i] == 'Y' or conn_set[i] == 'y' or conn_set[i] == 'd' or conn_set[i] == 'D':
            wind_i += 1
            conn_set_lst.append(conn_set[i])
        else:
            conn_set_lst[wind_i] += conn_set[i]

    # 对每个绕组分别处理
    for i in range(num):
        if 'Y' in conn_set_lst[i] or 'y' in conn_set_lst[i]:
            wind_info['绕组' + str(i+1)] = 'y'
            if 'N' in conn_set_lst[i] or 'n' in conn_set_lst[i]:
                wind_info['绕组' + str(i + 1) + '中性点'] = True
                if len(conn_set_lst[i]) == 2:
                    wind_info['绕组' + str(i + 1) + '方向'] = 0
                elif len(conn_set_lst[i]) == 3:
                    wind_info['绕组' + str(i + 1) + '方向'] = int(conn_set_lst[i][2])
                elif len(conn_set_lst[i]) == 4:
                    wind_info['绕组' + str(i + 1) + '方向'] = int(conn_set_lst[i][2:4])
            else:
                wind_info['绕组' + str(i + 1) + '中性点'] = False
                if len(conn_set_lst[i]) == 1:
                    wind_info['绕组' + str(i + 1) + '方向'] = 0
                elif len(conn_set_lst[i]) == 2:
                    wind_info['绕组' + str(i + 1) + '方向'] = int(conn_set_lst[i][1])
                elif len(conn_set_lst[i]) == 3:
                    wind_info['绕组' + str(i + 1) + '方向'] = int(conn_set_lst[i][1:3])
        elif 'D' in conn_set_lst[i] or 'd' in conn_set_lst[i]:
            wind_info['绕组' + str(i + 1)] = 'd'
            wind_info['绕组' + str(i + 1) + '中性点'] = False
            if len(conn_set_lst[i]) == 1:
                wind_info['绕组' + str(i + 1) + '方向'] = 0
            elif len(conn_set_lst[i]) == 2:
                wind_info['绕组' + str(i + 1) + '方向'] = int(conn_set_lst[i][1])
            elif len(conn_set_lst[i]) == 3:
                wind_info['绕组' + str(i + 1) + '方向'] = int(conn_set_lst[i][1:3])

    return wind_info


def point_capture(crd=None, x_intvl=20, y_intvl=20):
    """
    func: 点捕获
    :param crd: 实际点坐标
    :param x_intvl: x捕获间距
    :param y_intvl: y捕获间距
    :return: 捕获：修正后的点坐标，未捕获：False
    """
    if crd is not None:
        x = crd[0]
        y = crd[1]
        if abs(x - x_intvl * round(float(x) / x_intvl)) < 10 and abs(y - y_intvl * round(float(y) / y_intvl)) < 10:
            x = round(float(x) / x_intvl) * x_intvl
            y = round(float(y) / y_intvl) * y_intvl
            return x, y
        else:
            return False
    else:
        return False


def get_multi_value(value=None):
    """
    func: 获取倍数因子和值，如输入1000，得到'k', 1
    :return: 倍数因子和值
    """
    if value is None:
        value = ''
        multi = ''
    else:
        if value >= 1E12:
            value /= 1E12
            multi = 'T'
        elif value >= 1E9:
            value /= 1E9
            multi = 'G'
        elif value >= 1E6:
            value /= 1E6
            multi = 'M'
        elif value >= 1E3:
            value /= 1E3
            multi = 'k'
        elif value <= 1E-12:
            value /= 1E-12
            multi = 'p'
        elif value <= 1E-9:
            value /= 1E-9
            multi = 'n'
        elif value <= 1E-6:
            value /= 1E-6
            multi = 'u'
        elif value <= 1E-3:
            value /= 1E-3
            multi = 'm'
        else:
            multi = ''
    return multi, value


def get_unit(comp_nm):
    """
    func: 根据输入的元件名称，返回单位，如输入'R'，返回'Ω'
    :return:
    """
    unit = ''
    if comp_nm == 'R':
        unit = 'Ω'
    elif comp_nm == 'C':
        unit = 'F'
    elif comp_nm == 'L':
        unit = 'H'
    elif comp_nm == 'Uac' or comp_nm == 'Udc':
        unit = 'V'
    elif comp_nm == 'Iac' or comp_nm == 'Idc':
        unit = 'A'
    return unit


if __name__ == "__main__":
    print(get_multi_value(1580))
