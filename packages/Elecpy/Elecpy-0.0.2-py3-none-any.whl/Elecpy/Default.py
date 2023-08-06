"""
该模块用于放置缺省值，或叫默认值
"""
import pandas as pd


# 电路设置数据
dft_cir_config = {'ref_vol_visible': None,
                  'ref_cur_visible': None,
                  'dt': 0.001,
                  't': 0.1}


# 默认的电路数据
dft_cir_data = {'cir_config': dft_cir_config,
                'comps_data': {},
                'conns_data': {},
                'texts_data': {},
                'grphs_data': {}}

# 默认的电阻数据
dft_res_data = {'id': 'resistor-?',
                'designator': 'R-?',
                'value': 10,
                'node1': None,
                'node2': None,
                'vol_dir': True,
                'cur_dir': True,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# 默认的电容数据
dft_cap_data = {'id': 'capacitor-?',
                'designator': 'C-?',
                'value': 1E-6,
                'Uc': 0,
                'node1': None,
                'node2': None,
                'vol_dir': True,
                'cur_dir': True,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# 默认的电感数据
dft_ind_data = {'id': 'inductor-?',
                'designator': 'L-?',
                'value': 1E-6,
                'Il': 0,
                'node1': None,
                'node2': None,
                'vol_dir': True,
                'cur_dir': True,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# 默认的二极管数据
dft_dio_data = {'id': 'diode-?',
                'designator': 'D-?',
                'Ir': 55E-6,
                'Vf': 0.5,
                'node1': None,
                'node2': None,
                'vol_dir': True,
                'cur_dir': True,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# 默认的放电间隙
dft_gap_data = {'id': 'gap-?',
                'designator': 'Gap-?',
                'Roff': 1E9,
                'Ron': 1,
                'node1': None,
                'node2': None,
                'vol_dir': True,
                'cur_dir': True,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# 默认的DC电压源数据
dft_vdc_data = {'id': 'voltage_dc-?',
                'designator': 'Udc-?',
                'amp': 10,
                'node1': None,
                'node2': None,
                'vol_dir': True,
                'cur_dir': True,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# 默认的AC电压源数据
dft_vac_data = {'id': 'voltage_ac-?',
                'designator': 'Uac-?',
                'amp': 10,
                'freq': 50,
                'phase': 0,
                'node1': None,
                'node2': None,
                'vol_dir': True,
                'cur_dir': True,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# 默认的DC电流源数据
dft_idc_data = {'id': 'current_dc-?',
                'designator': 'Idc-?',
                'amp': 0,
                'node1': None,
                'node2': None,
                'vol_dir': True,
                'cur_dir': True,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# 默认的AC电流源数据
dft_iac_data = {'id': 'current_ac-?',
                'designator': 'Iac-?',
                'amp': 10,
                'freq': 50,
                'phase': 0,
                'node1': None,
                'node2': None,
                'vol_dir': True,
                'cur_dir': True,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# 默认接地点的数据
dft_gnd_data = {'id': 'ground-?',
                'designator': 'GND-?',
                'node1': 0,
                'node2': 0,
                'vol_dir': True,
                'cur_dir': True,
                'crd_x': 60,
                'crd_y': 60,
                'angle': 0}

# 默认元件数据
dft_comps_data = {'resistor': dft_res_data,
                  'capacitor': dft_cap_data,
                  'inductor': dft_ind_data,
                  'diode': dft_dio_data,
                  'voltage_ac': dft_vac_data,
                  'voltage_dc': dft_vdc_data,
                  'current_ac': dft_iac_data,
                  'current_dc': dft_idc_data,
                  'ground': dft_gnd_data,
                  'gap': dft_gap_data}

# 默认导线数据
dft_wire_data = {'id': 'wire-1',
                 'designator': 'w-?',
                 'net_id': '1',
                 'sta_comp': None,
                 'sta_tmnl': None,
                 'end_comp': None,
                 'end_tmnl': None}

# 默认文本数据
dft_text_data = {'id': 'text-1',
                 'crd_x': 0,
                 'crd_y': 20,
                 'angle': 0,
                 'visible': True,
                 'content': 'text',
                 'font_family': 'Times',
                 'font_size': '8',
                 'font_weight': 'bold',
                 'font_slant': 'roman',
                 'font_underline': 0,
                 'font_overstrike': 0}

# 默认箭头数据
dft_arrow_data = {'id': 'arrow-1',
                  'crd_x': 0,
                  'crd_y': 20,
                  'angle': 0,
                  'visible': True,
                  'tail_len': 20,
                  'arrw_len': 20,
                  'arrw_wid': 5,
                  'color': 'black'}

# 默认正负号数据
dft_posneg_data = {'id': 'pn-1',
                   'crd_x': 0,
                   'crd_y': 20,
                   'angle': 0,
                   'visible': True,
                   'size': 8,
                   'distance': 60,
                   'color': 'black'}

# 元件自带图形默认数据
dft_graph_data = {'arrow': dft_arrow_data,
                  'pn': dft_posneg_data}


if __name__ == '__main__':
    print(dft_comps_data['R'])
