# coding=utf-8
"""
该模块是用于计算电路，包括根据已知的电路网络表求出各节点电压和各支路的电流等
"""
import numpy as np
import pandas as pd
import os
import DatabaseManager as dm
from math import *
import cmath
import matplotlib.pyplot as plt
from File import *
from GUIElements import *

"""常量定义"""
diode_close_R = 0.001
diode_open_R = 1000000.0


def get_num_nodes(comps_data=None):
    """
    func: 求comps_data中的非参考节点数
    :param comps_data: 元件数据
    :return: 非参考节点数
    """
    # 求comps_data中的最大节点值max_node
    num_node = 0
    for data in comps_data:
        if data['node1'] > num_node:
            num_node = data['node1']
        if data['node2'] > num_node:
            num_node = data['node2']
    return num_node


def oper_data_init(comps_data=None):
    """
    func: 电路运行数据的初始化，(节点电压, 元件电压, 元件电流)
    :param comps_data: 元件数据
    :return:
    """
    # 节点电压
    u_nodes = {}
    # 元件电压
    u_comps = {}
    # 元件电流
    i_comps = {}
    num_nodes = get_num_nodes(comps_data)
    num_comps = len(comps_data)
    for i in range(num_nodes):
        u_nodes['u_node' + str(i + 1)] = [0]
    for i in range(num_comps):
        if comps_data[i]['designator'].split('-')[0] == 'C':
            u_comps[comps_data[i]['designator']] = [comps_data[i]['Uc']]
            i_comps[comps_data[i]['designator']] = [0]
        elif comps_data[i]['designator'].split('-')[0] == 'L':
            u_comps[comps_data[i]['designator']] = [0]
            i_comps[comps_data[i]['designator']] = [comps_data[i]['Il']]
        else:
            u_comps[comps_data[i]['designator']] = [0]
            i_comps[comps_data[i]['designator']] = [0]
    return u_nodes, u_comps, i_comps


def get_matrix_a(netlist=None):
    """
    func: 求解关联矩阵
    :param netlist: 网络表
    :return: 关联矩阵
    """
    num_nodes = max(max(netlist['node1']), max(netlist['node2']))
    num_comps = netlist.shape[0]
    # 创建num_node行、num_comp列的全零矩阵A
    a = np.zeros([num_nodes, num_comps])
    # 根据网络表，填充关联矩阵A
    for k in range(num_comps):
        j = netlist.loc[k, 'node1']
        if j > 0:
            a[j - 1, k] = 1
        j = netlist.loc[k, 'node2']
        if j > 0:
            a[j - 1, k] = -1
    return a


def get_matrix_fh(netlist=None,
                  dt=0.01):
    """
    func: 求解矩阵f和h
    :param netlist: 网络表
    :param dt: 时间间隔
    :return:
    """
    num_comps = netlist.shape[0]
    """求解矩阵F和H"""
    # 创建num_comp阶的全零矩阵F和H
    f = np.zeros([num_comps, num_comps], float)
    h = np.zeros([num_comps, num_comps], float)
    # 对于每个支路，按不同情况确定F和H的元素值
    for k in range(num_comps):
        if netlist.loc[k, 'name'][0] == 'G':
            f[k, k] = netlist.loc[k, 'value']
            h[k, k] = -1
        elif netlist.loc[k, 'name'][0] == 'C':
            f[k, k] = float(netlist.loc[k, 'value']) / dt
            h[k, k] = -1
        elif netlist.loc[k, 'name'][0] == 'R':
            f[k, k] = -1
            h[k, k] = netlist.loc[k, 'value']
        elif netlist.loc[k, 'name'][0] == 'L':
            f[k, k] = -1
            h[k, k] = float(netlist.loc[k, 'value']) / dt
        elif netlist.loc[k, 'name'][0] == 'U':
            f[k, k] = 1
            h[k, k] = 0
        elif netlist.loc[k, 'name'][0] == 'I':
            f[k, k] = 0
            h[k, k] = 1
        elif netlist.loc[k, 'name'] == 'VCVS':
            j = netlist.loc[k, 'value'].split('*')[1]
            ukj = netlist.loc[k, 'value'].split('*')[0]
            f[k, k] = 1
            f[k, j] = -ukj
            h[k, k] = 0
        elif netlist.loc[k, 'name'] == 'VCCS':
            j = netlist.loc[k, 'value'].split('*')[1]
            gkj = netlist.loc[k, 'value'].split('*')[0]
            f[k, k] = 0
            f[k, j] = -gkj
            h[k, k] = 1
        elif netlist.loc[k, 'name'] == 'CCVS':
            j = netlist.loc[k, 'value'].split('*')[1]
            rkj = netlist.loc[k, 'value'].split('*')[0]
            f[k, k] = 1
            f[k, j] = -rkj
            h[k, k] = 0
        elif netlist.loc[k, 'name'] == 'CCCS':
            j = netlist.loc[k, 'value'].split('*')[1]
            bkj = netlist.loc[k, 'value'].split('*')[0]
            f[k, k] = 0
            f[k, j] = -bkj
            h[k, k] = 1
    return f, h


def get_vector_us(netlist=None):
    """
    func: 求解电压源相量
    :param netlist:
    :return:
    """
    num_comps = netlist.shape[0]
    # 创建列向量Us
    u_s = np.zeros([num_comps, 1], float)
    # 对于每个支路，确定Us和Is的元素值
    for k in netlist.index:
        if 'U' in netlist.loc[k, 'name']:
            u_s[k] = netlist.loc[k, 'value']
    return u_s


def get_vector_is(netlist=None):
    """
    func: 求解电压源相量
    :param netlist:
    :return:
    """
    num_comps = netlist.shape[0]
    # 创建列向量Is
    i_s = np.zeros([num_comps, 1], float)
    # 对于每个支路，确定Us和Is的元素值
    for k in netlist.index:
        if 'I' in netlist.loc[k, 'name']:
            i_s[k] = netlist.loc[k, 'value']
    return i_s


def get_matrix_afh(a=None,
                   f=None,
                   h=None):
    """
    func: 合并矩阵A F H
    :param a: 关联矩阵a
    :param f: 矩阵F
    :param h: 矩阵H
    :return:
    """
    num_nodes = a.shape[0]
    num_comps = a.shape[1]
    """创建零矩阵"""
    zero_1 = np.zeros([num_nodes, num_nodes])
    zero_2 = np.zeros([num_nodes, num_comps])
    zero_3 = np.zeros([num_comps, num_comps])
    zero_4 = np.zeros([num_comps, num_nodes])
    """创建单位矩阵1num_comp"""
    one = np.identity(num_comps)
    # 合并矩阵A、F、H
    mat_1 = np.concatenate([zero_1, zero_2, a], axis=1)
    mat_2 = np.concatenate([-a.T, one, zero_3], axis=1)
    mat_3 = np.concatenate([zero_4, f, h], axis=1)
    mat_a = np.concatenate([mat_1, mat_2, mat_3], axis=0)

    return mat_a


def get_vector_usis(a=None,
                    u_s=None,
                    i_s=None):
    """
    func: 获取相量us和is的合并
    :param a: 关联矩阵A
    :param u_s:
    :param i_s:
    :return:
    """
    num_nodes = a.shape[0]
    num_comps = a.shape[1]
    # 创建零向量
    zero_5 = np.zeros([num_nodes, 1])
    zero_6 = np.zeros([num_comps, 1])
    # 合并矩阵b
    mat_b = np.concatenate([zero_5, zero_6, u_s + i_s], axis=0)

    return mat_b


def get_universal_netlist(comps_data=None,
                          u_comps=None,
                          i_comps=None,
                          dt=0.01):
    """
    func: 将netlist表转换为universal_netlist表(简称ul_netlist)，ul_netlist与netlist的不同是，netlist中包含的是实际中的
    电路模型，如二极管、三极管等，而ul_netlist中的电路模型是netlist中的电路模型的进一步等效，如二极管按状态不同可等效为负电压源
    ，负电流源或低阻抗电阻等
    :param comps_data: 元件数据，list[dict, dict,...]
    :param u_comps: 元件电压，dict{'designator': [], 'designator': [], ...}
    :param i_comps: 元件电流, dict{'designator': [], 'designator': [], ...}
    :param dt: 时间间隔
    :return:
    """
    # 求comps_data中的非参考节点数num_nodes
    num_nodes = get_num_nodes(comps_data)

    ul_netlist = pd.DataFrame({'name': [],
                               'sn': [],
                               'value': [],
                               'node1': [],
                               'node2': []})
    ul_netlist = ul_netlist.astype({'sn': 'int32', 'node1': 'int32', 'node2': 'int32'})

    # 求
    net_data = {}
    for idx, data in enumerate(comps_data):
        net_data['name'] = data['designator'].split('-')[0]
        if net_data['name'] == 'C':
            # 电容值
            net_data['name'] = 'C'
            net_data['sn'] = data['designator'].split('-')[1]
            net_data['value'] = data['value']
            num_nodes += 1
            net_data['node1'] = data['node1']
            net_data['node2'] = num_nodes
            ul_netlist = ul_netlist.append(net_data, ignore_index=True)
            # 电容初始电压当做串联一个电压源
            net_data['name'] = 'Uc'
            net_data['value'] = u_comps[data['designator']][-1]
            net_data['node1'] = num_nodes
            net_data['node2'] = data['node2']
            ul_netlist = ul_netlist.append(net_data, ignore_index=True)
        elif net_data['name'] == 'L':
            # 电感值
            net_data['name'] = 'L'
            net_data['sn'] = data['designator'].split('-')[1]
            net_data['value'] = data['value']
            net_data['node1'] = data['node1']
            net_data['node2'] = data['node2']
            ul_netlist = ul_netlist.append(net_data, ignore_index=True)
            # 电感初始电流当做并联一个电流源
            net_data['name'] = 'Il'
            net_data['value'] = i_comps[data['designator']][-1]
            net_data['node1'] = data['node1']
            net_data['node2'] = data['node2']
            ul_netlist = ul_netlist.append(net_data, ignore_index=True)
        elif net_data['name'] == 'D':
            # 正向截止，当作大电阻
            if 0 <= u_comps[data['designator']][-1] < data['Vf']:
                net_data['name'] = 'Rd'
                net_data['sn'] = data['designator'].split('-')[1]
                net_data['value'] = diode_open_R
                net_data['node1'] = data['node1']
                net_data['node2'] = data['node2']
                ul_netlist = ul_netlist.append(net_data, ignore_index=True)
            # 正向导通时，当作负电压源
            elif u_comps[data['designator']][-1] >= data['Vf']:
                net_data['name'] = 'Rd'
                net_data['sn'] = data['designator'].split('-')[1]
                net_data['value'] = diode_close_R
                net_data['node1'] = data['node1']
                num_nodes += 1
                net_data['node2'] = num_nodes
                ul_netlist = ul_netlist.append(net_data, ignore_index=True)

                net_data['name'] = 'Ud'
                net_data['sn'] = data['designator'].split('-')[1]
                net_data['value'] = data['Vf']
                net_data['node1'] = num_nodes
                net_data['node2'] = data['node2']
                ul_netlist = ul_netlist.append(net_data, ignore_index=True)
            # 反向截止时，当作负电流源
            elif u_comps[data['designator']][-1] < 0:
                net_data['name'] = 'Rd'
                net_data['sn'] = data['designator'].split('-')[1]
                net_data['value'] = diode_open_R
                net_data['node1'] = data['node1']
                net_data['node2'] = data['node2']
                ul_netlist = ul_netlist.append(net_data, ignore_index=True)

                net_data['name'] = 'Id'
                net_data['sn'] = data['designator'].split('-')[1]
                net_data['value'] = -data['Ir']
                net_data['node1'] = data['node1']
                net_data['node2'] = data['node2']
                ul_netlist = ul_netlist.append(net_data, ignore_index=True)
        elif net_data['name'] == 'Uac' or net_data['name'] == 'Iac':
            net_data['name'] = data['designator'].split('-')[0]
            net_data['sn'] = data['designator'].split('-')[1]
            # 时间索引
            t_idx = len(u_comps[data['designator']])
            net_data['value'] = data['amp'] * sin(2 * pi * data['freq'] * t_idx * dt + pi / 180 * data['phase'])
            net_data['node1'] = data['node1']
            net_data['node2'] = data['node2']
            ul_netlist = ul_netlist.append(net_data, ignore_index=True)
        elif net_data['name'] == 'Udc' or net_data['name'] == 'Idc':
            net_data['name'] = data['designator'].split('-')[0]
            net_data['sn'] = data['designator'].split('-')[1]
            net_data['value'] = data['amp']
            net_data['node1'] = data['node1']
            net_data['node2'] = data['node2']
            ul_netlist = ul_netlist.append(net_data, ignore_index=True)
        else:
            net_data['name'] = data['designator'].split('-')[0]
            net_data['sn'] = data['designator'].split('-')[1]
            net_data['value'] = data['value']
            net_data['node1'] = data['node1']
            net_data['node2'] = data['node2']
            ul_netlist = ul_netlist.append(net_data, ignore_index=True)

    return ul_netlist


def u_nodes_append(u_nodes=None,
                   un_t=None):
    """
    func: 节点电压u_nodes的元素添加
    :param u_nodes: 节点电压历史列表{'node1':[], 'node2':[], ...}
    :param un_t: 当前计算出的节点电压['node1vol', 'node2vol', ...]
    :return:
    """
    for i, u_node in enumerate(u_nodes):
        u_nodes[u_node].append(un_t[i])


def u_comps_append(netlist=None,
                   u_comps=None,
                   u_t=None):
    """
    func: 元件电压u_comps的元素添加
    :param netlist: 网络表
    :param u_comps: 节点电压历史列表{'comp1':[], 'comp2':[], ...}
    :param u_t: 当前计算出的元件电压['comp1vol', 'comp2vol', ...]
    :return:
    """
    u_t_dict = {}
    for idx in netlist.index:
        u_t_dict[netlist.loc[idx, 'name'] + '-' + netlist.loc[idx, 'sn']] = u_t[idx]

    for i, u_comp in enumerate(u_comps):
        name = u_comp.split('-')[0]
        sn = u_comp.split('-')[1]
        if name == 'C':
            u_new = u_t_dict[u_comp] + u_t_dict['Uc-' + str(sn)]
        elif name == 'D':
            if 'Ud-' + str(sn) in u_t_dict.keys():
                u_new = u_t_dict['Ud-' + str(sn)] + u_t_dict['Rd-' + str(sn)]
            elif 'Id-' + str(sn) in u_t_dict.keys():
                u_new = u_t_dict['Id-' + str(sn)] + u_t_dict['Rd-' + str(sn)]
            else:
                u_new = u_t_dict['Rd-' + str(sn)]
        else:
            u_new = u_t_dict[u_comp]
        u_comps[u_comp].append(u_new)


def i_comps_append(netlist=None,
                   i_comps=None,
                   i_t=None):
    """
    func: 元件电流i_comps的元素添加
    :param netlist: 网络表
    :param i_comps: 节点电压历史列表{'comp1':[], 'comp2':[], ...}
    :param i_t: 当前计算出的元件电压['comp1vol', 'comp2vol', ...]
    :return:
    """
    i_t_dict = {}
    for idx in netlist.index:
        i_t_dict[netlist.loc[idx, 'name'] + '-' + netlist.loc[idx, 'sn']] = i_t[idx]

    for i, i_comp in enumerate(i_comps):
        name = i_comp.split('-')[0]
        sn = i_comp.split('-')[1]
        if name == 'L':
            i_new = i_t_dict[i_comp] + i_t_dict['Il-' + str(sn)]
        elif name == 'D':
            if 'Ud' + str(sn) in i_t_dict.keys():
                i_new = i_t_dict['Ud-' + str(sn)]
            elif 'Rd' + str(sn) in i_t_dict.keys():
                i_new = i_t_dict['Rd-' + str(sn)]
            elif 'Id' + str(sn) in i_t_dict.keys():
                i_new = i_t_dict['Id-' + str(sn)]
        else:
            i_new = i_t_dict[i_comp]
        i_comps[i_comp].append(i_new)


def cal_universal_cir(comps_data=None,
                      t=1.0,
                      dt=0.01,
                      prgsbar=None):
    """
    func: 离散微分法电路计算
    :param comps_data: 网络表
    :param t: 时间长度, s
    :param dt: 单位时间, s
    :return:
    """
    """参数判别"""
    if comps_data is None:
        raise TypeError('请输入网络表')

    """电路运行数据变量定义及初始化"""
    u_nodes, u_comps, i_comps = oper_data_init(comps_data)

    """时间序列"""
    t_list = np.arange(0, t, dt)

    """progressbar"""
    if prgsbar:
        prgsbar['maximum'] = int(t / dt)

    """迭代求解"""
    for index, ti in enumerate(t_list[1:]):
        if prgsbar:
            prgsbar['value'] = index
            prgsbar.update()
        """网络表转换"""
        ul_netlist = get_universal_netlist(comps_data,
                                           u_comps,
                                           i_comps,
                                           dt)
        # print(ul_netlist)

        """得到电路中所有节点（不包括参考节点）的数量"""
        ul_num_node = max(max(ul_netlist['node1']), max(ul_netlist['node2']))
        # 得到电路中所有支路（包括电源支路）的数量（即所有元器件的数量，也即netlist的行数）
        ul_num_comp = ul_netlist.shape[0]

        """求解关联矩阵A"""
        a = get_matrix_a(ul_netlist)

        """求解矩阵f和h"""
        f, h = get_matrix_fh(ul_netlist, dt=dt)

        """求解电压源向量us和电流源向量is"""
        u_s = get_vector_us(ul_netlist)
        i_s = get_vector_is(ul_netlist)

        """计算方程组"""
        mat_a = get_matrix_afh(a, f, h)
        mat_b = get_vector_usis(a, u_s, i_s)
        # 计算x，x为numpy.ndarray数据，且为2维数组
        x = np.linalg.solve(mat_a, mat_b)

        """x转换为pandas.Series数据，方便输出"""
        # 将x由二维数组转换为一维数组（要将numpy.ndarray转换为pandas.Series，此步必须）
        x = x.reshape(x.size, )
        # 将x切片，得到节点电压un_t，支路电压u_t，支路电流i_t
        un_t = x[:ul_num_node]
        u_t = x[ul_num_node: ul_num_node + ul_num_comp]
        i_t = x[ul_num_node + ul_num_comp:]

        """将值赋给u_nodes、u_comps、i_comps"""
        u_nodes_append(u_nodes, un_t)
        u_comps_append(ul_netlist, u_comps, u_t)
        i_comps_append(ul_netlist, i_comps, i_t)

    """参考方向"""
    for key in u_comps:
        for comp_data in comps_data:
            if comp_data['designator'] == key:
                for idx, *_ in enumerate(u_comps[key]):
                    if not comp_data['vol_dir']:
                        u_comps[key][idx] *= -1
    for key in i_comps:
        for comp_data in comps_data:
            if comp_data['designator'] == key:
                for idx, *_ in enumerate(u_comps[key]):
                    if key.split('-')[0] == 'Uac' or key.split('-')[0] == 'Udc' or \
                            key.split('-')[0] == 'Idc' or key.split('-')[0] == 'Iac':
                        if comp_data['cur_dir']:
                            i_comps[key][idx] *= -1
                    else:
                        if not comp_data['cur_dir']:
                            i_comps[key][idx] *= -1

    return {'time': t_list, 'voltage_node': u_nodes, 'voltage_component': u_comps, 'current_component': i_comps}


def cal_sinsteady_cir(netlist=None):
    """
    函数：正弦稳态电路计算
    :param netlist: 网络表
    :return:Un节点电压、U支路电压、I支路电流
    """
    """参数判别"""
    if netlist is None:
        raise TypeError('请输入网络表')
    if type(netlist) is not pd.DataFrame:
        raise TypeError('请输入正确的pandas.DataFrame数据')

    """读取netlist中的关键信息"""
    # 得到电路中所有节点（不包括参考节点）的数量
    num_node = max(max(netlist['node1']), max(netlist['node2']))

    # 得到电路中所有支路（包括电源支路）的数量（即所有元器件的数量，也即netlist的行数）
    num_comp = netlist.shape[0]

    # 得到所有节点（不包括参考节点）的名称列表（[node0, node1, ...]）
    list_node = list(range(0, num_node))
    for i in range(num_node):
        list_node[i] = 'U_node' + str(list_node[i] + 1)

    # 得到所有支路的电压和电流名称列表（[U1, R1, ...])
    list_branch_u = list(range(0, num_comp))
    list_branch_i = list(range(0, num_comp))
    for i in range(num_comp):
        list_branch_u[i] = 'U_' + str(netlist.loc[i, 'name']) + '-' + str(netlist.loc[i, 'sn'])
        list_branch_i[i] = 'I_' + str(netlist.loc[i, 'name']) + '-' + str(netlist.loc[i, 'sn'])

    """求解Us、Is"""
    # 创建全零列向量Us、Is
    u_s = np.zeros([num_comp, 1], complex)
    i_s = np.zeros([num_comp, 1], complex)
    # 对于每个支路，确定Us和Is的元素值
    freq = None
    for k in range(num_comp):
        value = netlist.loc[k, 'value']
        if netlist.loc[k, 'name'] == 'Us' or netlist.loc[k, 'name'] == 'Is':
            value_list = value.split(',')
            # 如果电源是正弦
            if value_list[0] == 'sin':
                if freq is not None and float(value_list[2]) != freq:
                    raise TypeError('电源频率不一致')
                freq = float(value_list[2])
                m = float(value_list[1])
                phi = float(value_list[3])
                if netlist.loc[k, 'name'] == 'Us':
                    u_s[k] = m * cmath.exp(1j * phi)
                elif netlist.loc[k, 'name'] == 'Is':
                    i_s[k] = m * cmath.exp(1j * phi)
            # 如果电源是常数
            elif value_list[0] == 'const':
                if 'C' in list(netlist['name']) or 'L' in list(netlist['name']):
                    raise TypeError('电路中含有储能元件，电源不能是直流')
                if netlist.loc[k, 'name'] == 'Us':
                    u_s[k] = float(value_list[1])
                elif netlist.loc[k, 'name'] == 'Is':
                    i_s[k] = float(value_list[1])

    """求解关联矩阵A"""
    # 创建num_node行、num_comp列的全零矩阵A
    a = np.zeros([num_node, num_comp])
    # 根据网络表，填充关联矩阵A
    for k in range(num_comp):
        j = netlist.loc[k, 'node1']
        if j > 0:
            a[j - 1, k] = 1
        j = netlist.loc[k, 'node2']
        if j > 0:
            a[j - 1, k] = -1

    """求解矩阵F和H"""
    # 创建num_comp阶的全零矩阵F和H
    f = np.zeros([num_comp, num_comp], complex)
    h = np.zeros([num_comp, num_comp], complex)
    # 对于每个支路，按不同情况确定F和H的元素值
    for k in range(num_comp):
        if netlist.loc[k, 'name'] == 'G':
            f[k, k] = float(netlist.loc[k, 'value'])
            h[k, k] = -1
        if netlist.loc[k, 'name'] == 'C':
            f[k, k] = float(netlist.loc[k, 'value'].split(',')[0]) * 1j * 2 * np.pi * freq
            h[k, k] = -1
        if netlist.loc[k, 'name'] == 'R':
            f[k, k] = -1
            h[k, k] = float(netlist.loc[k, 'value'])
        if netlist.loc[k, 'name'] == 'L':
            f[k, k] = -1
            h[k, k] = float(netlist.loc[k, 'value'].split(',')[0]) * 1j * 2 * np.pi * freq
        if netlist.loc[k, 'name'] == 'Us':
            f[k, k] = 1
            h[k, k] = 0
        if netlist.loc[k, 'name'] == 'Is':
            f[k, k] = 0
            h[k, k] = 1
        if netlist.loc[k, 'name'] == 'VCVS':
            j = float(netlist.loc[k, 'value'].split('*')[1])
            ukj = float(netlist.loc[k, 'value'].split('*')[0])
            f[k, k] = 1
            f[k, j] = -ukj
            h[k, k] = 0
        if netlist.loc[k, 'name'] == 'VCCS':
            j = float(netlist.loc[k, 'value'].split('*')[1])
            gkj = float(netlist.loc[k, 'value'].split('*')[0])
            f[k, k] = 0
            f[k, j] = -gkj
            h[k, k] = 1
        if netlist.loc[k, 'name'] == 'CCVS':
            j = float(netlist.loc[k, 'value'].split('*')[1])
            rkj = float(netlist.loc[k, 'value'].split('*')[0])
            f[k, k] = 1
            f[k, j] = -rkj
            h[k, k] = 0
        if netlist.loc[k, 'name'] == 'CCCS':
            j = float(netlist.loc[k, 'value'].split('*')[1])
            bkj = float(netlist.loc[k, 'value'].split('*')[0])
            f[k, k] = 0
            f[k, j] = -bkj
            h[k, k] = 1

    """创建单位矩阵1num_comp"""
    one = np.identity(num_comp)

    """合并矩阵"""
    # 合并矩阵A、F、H
    zero_1 = np.zeros([num_node, num_node])
    zero_2 = np.zeros([num_node, num_comp])
    zero_3 = np.zeros([num_comp, num_comp])
    zero_4 = np.zeros([num_comp, num_node])
    mat_1 = np.concatenate([zero_1, zero_2, a], axis=1)
    mat_2 = np.concatenate([-a.T, one, zero_3], axis=1)
    mat_3 = np.concatenate([zero_4, f, h], axis=1)
    mat_a = np.concatenate([mat_1, mat_2, mat_3], axis=0)
    # 合并矩阵b
    zero_5 = np.zeros([num_node, 1])
    zero_6 = np.zeros([num_comp, 1])
    mat_b = np.concatenate([zero_5, zero_6, u_s + i_s], axis=0)

    """计算方程组"""
    # 计算x，x为numpy.ndarray数据，且为2维数组
    x = np.linalg.solve(mat_a, mat_b)

    """x转换为pandas.Series数据，方便输出"""
    # 将x由二维数组转换为一维数组（要将numpy.ndarray转换为pandas.Series，此步必须）
    x = x.reshape(x.size, )
    # 将x切片，得到节点电压un，支路电压u，支路电流i
    un = x[:num_node]
    u = x[num_node: num_node + num_comp]
    i = x[num_node + num_comp:]
    # 将un、u、i转换为pandas.Series数据
    un_series = pd.Series(un, index=list_node)
    u_series = pd.Series(u, index=list_branch_u)
    i_series = pd.Series(i, index=list_branch_i)
    # 返回
    return un_series, u_series, i_series


class Calculation:
    """
    class: 计算类
    """
    def __init__(self,
                 netlist=None,
                 dt=None,
                 t=None):
        """
        method:
        :param netlist: 电路的netlist
        :param dt:
        :param t:
        """
        # 网络表
        self.netlist = netlist
        # 生成的输出数据：运行数据
        self.out_data = None
        # 计算方法
        self.method = ['discrete_differential', 'sinusoidal_steady_state']
        # 电路配置数据
        self.cir_config = None
        # data
        self.dis_diff = {'dt': dt, 'time': t}
        self.sin_stdy = {'xx': 00}
        # 根窗口
        self.root = None
        # 窗口宽、高
        self.width = None
        self.height = None
        # 方法选择框架
        self.method_choice_frame = None
        # 内容选择框架
        self.content_set_frame = None
        # 方法变量
        self.method_var = None
        self.set_disdiff_frame = None
        self.set_sinstdy_frame = None
        # 表格
        self.table_nm = {}
        self.table_vl = {}
        self.entry_var = {}

    def add_netlist(self,
                    netlist,
                    cir_config=None):
        """
        method: 添加netlist
        :param netlist: 网络表
        :param cir_config:
        :return:
        """
        self.netlist = netlist
        self.cir_config = cir_config

    def main_window(self):
        """
        method: 主窗口
        :return:
        """
        self.__window_shell()
        self.method_choice_page()
        self.button_area()

    def plot_config_window(self):
        """
        method: 配置plot窗口
        :return:
        """
        self.__window_shell()
        self.plot_config_area()

    def __window_shell(self,
                       width=500,
                       height=500):
        """
        :param 窗口框架
        :param width
        :parma height
        :return:
        """
        self.width = width
        self.height = height
        """创建窗口"""
        self.root = tk.Toplevel()
        self.root.title('Analysis Config')
        if self.width and self.height:
            geometry = str(self.width) + 'x' + str(self.height)
        else:
            self.root.state('zoomed')
            self.root.update()
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
            geometry = str(self.width) + 'x' + str(self.height)
        self.root.geometry(geometry)
        # 计算方法选择frame
        self.method_choice_frame = tk.Frame(self.root, bg='#F0F0F0', height=50, width=self.width, relief=tk.RIDGE)
        self.method_choice_frame.grid(row=0, column=0)
        self.method_choice_frame.grid_propagate(0)

        # 内容设置frame
        self.content_set_frame = tk.Frame(self.root, bg='#F0F0F0', height=self.height - 80, width=self.width)
        self.content_set_frame.grid(row=1, column=0)
        self.content_set_frame.grid_propagate(0)

        # 按键frame
        self.button_frame = tk.Frame(self.root, bg='#F0F0F0', height=30, width=width)
        self.button_frame.grid(row=2, column=0)
        self.button_frame.grid_propagate(0)

    def method_choice_page(self):
        """
        method:
        :return:
        """
        method_choice_label = tk.Label(self.method_choice_frame, text='Chose the method:', width=25)
        method_choice_label.grid(row=0, column=0)
        optionlist = ('', 'discrete_differential', 'sinusoidal_steady_state')
        self.method_var = tk.StringVar(value=optionlist[1])
        method_list = ttk.OptionMenu(self.method_choice_frame, self.method_var, *optionlist)
        method_list.grid(row=0, column=1)
        butt_confrm = ttk.Button(self.method_choice_frame, width=20, text='Confirm', command=self.param_set_page)
        butt_confrm.grid(row=0, column=2)

    def param_set_page(self):
        """
        method:
        :return:
        """
        if self.method_var.get() == 'discrete_differential':
            self.set_disdiff_params()
        elif self.method_var.get() == 'sinusoidal_steady_state':
            self.set_sinstdy_params()

    def set_disdiff_params(self):
        """
        method: 设置离散微分法的参数
        :return:
        """
        self.dis_diff['dt'] = self.cir_config['dt']
        self.dis_diff['time'] = self.cir_config['t']
        if self.set_sinstdy_frame:
            self.set_sinstdy_frame.destroy()
        self.set_disdiff_frame = tk.Frame(self.content_set_frame, bg='#F0F0F0', height=self.height - 60,
                                          width=self.width)
        self.set_disdiff_frame.grid(row=0, column=0)
        self.set_disdiff_frame.grid_propagate(0)
        for idx, key in enumerate(self.dis_diff):
            if key == 'id' or key == 'crd_x' or key == 'crd_y' or key == 'angle' or key == 'node1' or key == \
                    'node2' or key == 'vol_dir' or key == 'cur_dir':
                continue
            self.table_nm[key] = tk.Label(self.set_disdiff_frame, text=key, width=int(self.width / 16),
                                          relief=tk.RIDGE, bd=1)
            if self.dis_diff[key] is True:
                self.entry_var[key] = tk.StringVar(value='True')
            elif self.dis_diff[key] is False:
                self.entry_var[key] = tk.StringVar(value='False')
            elif type(self.dis_diff[key]) == float:
                self.entry_var[key] = tk.DoubleVar(value=self.dis_diff[key])
            elif type(self.dis_diff[key]) == int:
                self.entry_var[key] = tk.IntVar(value=self.dis_diff[key])
            else:
                self.entry_var[key] = tk.StringVar(value=self.dis_diff[key])

            self.table_vl[key] = tk.Entry(self.set_disdiff_frame,
                                          width=int(self.width / 16),
                                          textvariable=self.entry_var[key])

            self.table_nm[key].grid(row=idx, column=0)
            self.table_nm[key].grid_propagate(0)
            self.table_vl[key].grid(row=idx, column=1)
            self.table_vl[key].grid_propagate(0)

    def set_sinstdy_params(self):
        """
        method: 设置正弦稳态法的参数
        :return: 
        """
        if self.set_disdiff_frame:
            self.set_disdiff_frame.destroy()
        self.set_sinstdy_frame = tk.Frame(self.content_set_frame, bg='#F0F0F0', height=self.height - 60,
                                          width=self.width)
        self.set_sinstdy_frame.grid(row=0, column=0)
        self.set_sinstdy_frame.grid_propagate(0)

    def button_area(self):
        """
        method:
        :return:
        """
        def save_param():
            if self.method_var.get() == 'discrete_differential':
                for key in self.entry_var:
                    self.dis_diff[key] = self.entry_var[key].get()
                    if key == 'dt':
                        self.cir_config['dt'] = self.dis_diff[key]
                    elif key == 'time':
                        self.cir_config['t'] = self.dis_diff[key]
            elif self.method_var.get() == 'sinusoidal_steady_state':
                for key in self.entry_var:
                    self.sin_stdy[key] = self.entry_var[key].get()

        def run():
            save_param()
            """progress bar"""
            prg = ttk.Progressbar(self.root, mode='determinate', length=150)
            prg.grid(row=0, column=0)
            prg.start()
            self.out_data = cal_universal_cir(comps_data=self.netlist, t=self.dis_diff['time'], dt=self.dis_diff['dt'],
                                              prgsbar=prg)
            prg.stop()
            prg.destroy()
            plot_win = Plot(self.out_data)
            plot_win.main_window()

        butt_save = ttk.Button(self.button_frame, width=20, text='Save', command=save_param)
        butt_save.grid(row=0, column=0)
        butt_run = ttk.Button(self.button_frame, width=20, text='Run', command=run)
        butt_run.grid(row=0, column=1)

    def get_vol_node(self,
                     node=None):
        """
        method: 显示节点电压
        :return:
        """
        # 如果没有给定node，则返回所有节点的电压值
        if node is None:
            return self.out_data['vol_node']
        # 如果给定某个node的名称，则返回该节点的电压值
        elif type(node) == str:
            return self.out_data['vol_node'][node]
        # 如果给定某几个node的名称组成的列表，则返回该几个节点的电压值
        elif type(node) == list:
            for i in node:
                return self.out_data['vol_node'][node[i]]

    def plot_config_area(self):
        """
        method: 图形配置
        :return:
        """
        self.plot_config_frame = tk.Frame(self.content_set_frame, bg='#F0F0F0', height=self.height - 60,
                                          width=self.width)
        self.plot_config_frame.grid(row=0, column=0)
        self.plot_config_frame.grid_propagate(0)

        row_num = 0
        for key in self.out_data:
            lbl = ttk.Label(self.plot_config_frame, text=key)
            lbl.grid(row=row_num, column=0)
            row_num += 1
            if key == 'time':
                continue
            for subkey in self.out_data[key]:
                print(subkey)
                self.cir_param_var[subkey] = tk.StringVar(value=subkey)
                self.cir_param_sl[subkey] = ttk.Checkbutton(self.plot_config_frame, variable=self.cir_param_var,
                                                            text=subkey,
                                                            width=int(self.width / 16))

                self.cir_param_sl[subkey].grid(row=row_num, column=1)
                self.cir_param_sl[subkey].grid_propagate(0)
                row_num += 1

    def get_vol_comp(self,
                     designator=None):
        """
        method: 显示元件电压
        :param designator:
        :return:
        """
        pass

    def get_cur_comp(self,
                     designator=None):
        """
        method: 显示元件电流
        :param designator:
        :return:
        """
        pass

    def fig_plot(self, param):
        """
        method: 显示某个参数param的时变曲线
        :param param:
        :return:
        """
        pass

    def fig_phasor(self, param):
        """
        method: 显示某个或某几个参数param的相量图
        :param param:
        :return:
        """
        pass

    def export_out(self,
                   path=None,
                   file=None):
        """
        method: 导出电路计算数据至.out文件
        :param path: 路径
        :param file: 文件名称，包含.out后缀名
        :return:
        """
        pass

    def cal_transient(self,
                      t=1,
                      dt=0.01):
        """
        method: 暂态计算
        :param t: 时长
        :param dt: 时间步长
        :return: t_list, u_nodes, u_comps, i_comps
        """
        return cal_universal_cir(self.comps_data, t, dt)

    def cal_sinsteady(self):
        """
        method: 正弦稳态计算
        :return:
        """
        return cal_sinsteady_cir(self.comps_data)


class Plot:
    """
    class: Plot类
    """

    def __init__(self,
                 outdata=None):
        """
        method:
        :param outdata: 电路计算后的运行数据
        """
        # 网络表
        self.outdata = outdata
        # 显示的变量
        self.plot_var = {}
        # 根窗口
        self.root = None
        # 窗口宽、高
        self.width = None
        self.height = None
        # 配置图形显示框架
        self.plot_config_frame = None
        # 图形配置
        self.label = {}
        self.cir_param_nm = {}
        self.cir_param_sl = {}
        self.cir_param_var = {}

    def add_outdata(self,
                    outdata):
        """
        method: 添加outdata
        :param outdata: 数据
        :return:
        """
        self.outdata = outdata

    def main_window(self):
        """
        method: 配置plot窗口
        :return:
        """
        self.__window_shell()
        self.plot_config_page()
        self.button_area()

    def button_area(self):
        """
        method:
        :return:
        """
        def run():
            self.plot_var = {}
            label_vol = False
            label_cur = False
            for key in self.cir_param_var:
                if self.cir_param_var[key].get():
                    if key.split(':')[0] == 'voltage_component':
                        label_vol = True
                    if key.split(':')[0] == 'current_component':
                        label_cur = True
                    self.plot_var[key] = self.outdata[key.split(':')[0]][key.split(':')[1]]

            if label_vol and label_cur:
                fig, (ax1, ax2) = plt.subplots(2, 1)
                fig.suptitle('Voltage and Current')
                for var in self.plot_var:
                    if var.split(':')[0] == 'voltage_component':
                        ax1.plot(self.outdata['time'][1:], self.plot_var[var][1:], label='voltage:' + var.split(':')[1])
                    elif var.split(':')[0] == 'current_component':
                        ax2.plot(self.outdata['time'][1:], self.plot_var[var][1:], label='current:' + var.split(':')[1])
                ax1.set_xlabel('t/s')
                ax2.set_xlabel('t/s')
                ax1.set_ylabel('U/V')
                ax2.set_ylabel('I/A')
                ax1.legend(loc='upper right')
                ax2.legend(loc='upper right')
                ax1.grid()
                ax2.grid()
            else:
                for var in self.plot_var:
                    plt.plot(self.outdata['time'][1:], self.plot_var[var][1:],
                             label=var.split(':')[0].replace('_component', ':') + var.split(':')[1])
                plt.legend(loc='upper right')
                plt.xlabel(xlabel='t/s')
                if label_vol:
                    plt.ylabel(ylabel='U/V')
                if label_cur:
                    plt.ylabel(ylabel='I/A')
                plt.grid()
            plt.show()

        butt_run = ttk.Button(self.button_frame, width=20, text='Plot', command=run)
        butt_run.grid(row=0, column=1)

    def __window_shell(self,
                       width=500,
                       height=500):
        """
        :param 窗口框架
        :param width
        :parma height
        :return:
        """
        self.width = width
        self.height = height
        """创建窗口"""
        self.root = tk.Toplevel()
        self.root.title('Plot Config')
        if self.width and self.height:
            geometry = str(self.width) + 'x' + str(self.height)
        else:
            self.root.state('zoomed')
            self.root.update()
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
            geometry = str(self.width) + 'x' + str(self.height)
        self.root.geometry(geometry)
        # 计算方法选择frame
        self.method_choice_frame = tk.Frame(self.root, bg='#F0F0F0', height=50, width=self.width, relief=tk.RIDGE)
        self.method_choice_frame.grid(row=0, column=0)
        self.method_choice_frame.grid_propagate(0)

        # 内容设置frame
        self.content_set_frame = tk.Frame(self.root, bg='#F0F0F0', height=self.height - 80, width=self.width)
        self.content_set_frame.grid(row=1, column=0)
        self.content_set_frame.grid_propagate(0)

        # 按键frame
        self.button_frame = tk.Frame(self.root, bg='#F0F0F0', height=30, width=width)
        self.button_frame.grid(row=2, column=0)
        self.button_frame.grid_propagate(0)

    def plot_config_page(self):
        """
        method: 图形配置
        :return:
        """
        self.plot_config_frame = tk.Frame(self.content_set_frame, bg='#F0F0F0', height=self.height - 60,
                                          width=self.width)
        self.plot_config_frame.grid(row=0, column=0)
        self.plot_config_frame.grid_propagate(0)

        row_num = 0
        for key in self.outdata:
            if key == 'time':
                continue
            self.label[key] = ttk.Label(self.plot_config_frame, text=key, font='25')
            self.label[key].grid(row=row_num, column=0)
            row_num += 1
            for subkey in self.outdata[key]:
                self.cir_param_var[key + ':' + subkey] = tk.IntVar(value=0)
                self.cir_param_sl[key + ':' + subkey] = ttk.Checkbutton(self.plot_config_frame,
                                                                        variable=self.cir_param_var[key + ':' + subkey],
                                                                        text=subkey,
                                                                        width=int(self.width / 16))

                self.cir_param_sl[key + ':' + subkey].grid(row=row_num, column=0)
                self.cir_param_sl[key + ':' + subkey].grid_propagate(0)
                row_num += 1


if __name__ == '__main__':
    cir_data = [{'designator': 'Uac-1', 'amp': 10, 'freq': 50, 'phase': 0, 'node1': 1, 'node2': 0, 'vol_dir': True,
                 'cur_dir': True},
                {'designator': 'R-1', 'value': 3185.0, 'node1': 1, 'node2': 2, 'vol_dir': True, 'cur_dir': True},
                {'designator': 'C-1', 'value': 1e-06, 'Uc': 0, 'node1': 2, 'node2': 0, 'vol_dir': True,
                 'cur_dir': True}]
    ans = Calculation(cir_data)
    ans.main_window()
