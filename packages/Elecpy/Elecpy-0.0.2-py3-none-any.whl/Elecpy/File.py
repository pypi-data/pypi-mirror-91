"""
该模块用来操作文件，文件使用txt创建，保存名称为.cir
"""
import os
from Backup import *


def jdg_cir_file_sta(fline):
    """
    func: 判断cir文件开始
    :param fline: 文件中的一行内容
    :return:
    """
    if '<<cir_file>>' in fline:
        return True
    else:
        return False


def jdg_cmp_file_sta(fline):
    """
    func: 判断cmp文件开始
    :param fline: 文件中的一行内容
    :return:
    """
    if '<<cmp_file>>' in fline:
        return True
    else:
        return False


def jdg_file_end(fline):
    """
    func: 判断cir文件结束
    :param fline:
    :return:
    """
    if '<<end>>' in fline:
        return True
    else:
        return False


def wr_cir_file_sta(file):
    """
    func: 写cir文件开始
    :return:
    """
    file.write('<<cir_file>>\n\n\n')


def wr_cmp_file_sta(file):
    """
    func: 写cmp文件开始
    :param file:
    :return:
    """
    file.write('<<cmp_file>>\n\n\n')


def wr_file_end(file):
    """
    func: 写cir文件结束
    :param file:
    :return:
    """
    file.write('\n\n\n<<end>>')


class File:
    """
    class: 文件
    """
    def __init__(self):
        """
        method: 创建一个文件
        """
        # .cir源文件（即已打开的.cir文件）的路径
        self.source_cirfilepath = None
        # .cmp源文件（即已打开的.cmp文件）的路径
        self.source_cmpfilepath = None

    def open_cirfile(self,
                     path=None,
                     file=None):
        """
        method: 打开一个.cir文件，返回数据cir_data={'comps_data': [], 'wires_data': [], 'texts_data': []}
        该方法可判别文件是否是cir文件，如果不是cir文件，则报错
        :param path: 文件路径
        :param file: 文件名称，包含后缀名.cir
        :return:
        """
        if file.split('.')[1] != 'cir':
            raise TypeError('The file must be .cir!')
        filepath = os.path.join(path, file)
        if not os.path.isfile(filepath):
            raise TypeError('The file is not exist!!')

        self.source_cirfilepath = filepath

        # 数据段区间标志位
        cir_rd_section = False
        # 数据容器
        cir_data = None

        with open(filepath, 'r') as file:
            lines = file.readlines()
            for i, el in enumerate(lines):
                # 判断cir文件开始
                if jdg_cir_file_sta(el):
                    cir_rd_section = True

                # 判断元件数据段开始
                elif cir_rd_section and el != '\n' and el != '<<end>>':
                    cir_data = eval(el)

                # cir文件结束
                elif jdg_file_end(el):
                    break
        # 记录文件源
        self.source_cmpfilepath = filepath
        return cir_data

    def save_cirfile(self,
                     cir_data,
                     filepath=None):
        """
        func: 保存文件，如果filepath给定，则将cir_data保存入filepath中，如果filepath未给定，则将cir_data存入
        self.source_cirfilepath中，如果filepath和self.source_cirfilepath均为None，则报错
        :param cir_data: 电路数据
        :param filepath: 目标文件路径
        :return:
        """
        # 如果filepath存在，则将cir_data保存至指定的路径中，且该文件必须为新建，类似于save as
        if filepath:
            cirfilepath = filepath
        # 如果path不存在而self.source_cirfilepath存在，则将cir_data存入该文件中，该文件可新建也可已存在，类似于save
        elif self.source_cirfilepath:
            cirfilepath = self.source_cirfilepath
        else:
            raise TypeError('The directory to save the file is needed!!')

        # 以写的方式打开cirfilepath文件路径
        with open(cirfilepath, 'w') as file:
            # 写cir文件开始
            wr_cir_file_sta(file)
            file.write(str(cir_data))
            # 写cir文件结束
            wr_file_end(file)

        # 记录文件源
        self.source_cmpfilepath = filepath

    def open_cmpfile(self,
                     path=None,
                     file=None):
        """
        method: 打开一个.cmp文件, 返回数据comp_data={'comp_id': 'crd_x': 'crd_y': , ...}
        该方法可判别文件是否是cmp文件，如果不是cmp文件，则报错
        :param path: 文件路径
        :param file: 文件名称，包含后缀名.cmp
        :return:
        """
        if file.split('.')[1] != 'cmp':
            raise TypeError('The file must be .cmp!')
        filepath = os.path.join(path, file)
        if not os.path.isfile(filepath):
            raise TypeError('The file is not exist!!')

        # 数据组区间
        comp_rd_section = False
        # 数据容器
        comp_data = {}

        with open(filepath, 'r') as file:
            lines = file.readlines()
            for i, el in enumerate(lines):
                if jdg_cmp_file_sta(el):
                    comp_rd_section = True
                elif comp_rd_section and el != '\n' and el != '<<end>>':
                    comp_data = eval(el)
                elif jdg_file_end(el):
                    break

        # 记录文件源
        self.source_cmpfilepath = filepath

        return comp_data

    def save_cmpfile(self,
                     comp_data=None,
                     filepath=None):
        """
        func: 保存文件，如果filepath给定，则将comp_data保存入filepath中，如果filepath未给定，则将comp_data存入
        self.source_cmpfilepath中，如果filepath和self.source_cmpfilepath均为None，则报错
        :param comp_data: 电路数据
        :param filepath: 目标文件路径
        :return:
        """
        if os.path.basename(filepath).split('.')[1] != 'cmp':
            raise TypeError('The file must be .cmp!')
        # 判断comp_data是否为空
        if comp_data is None:
            raise TypeError('The cir_data can not be None!!')

        # 如果filepath存在，则将cir_data保存至指定的路径中，且该文件必须为新建，类似于save as
        if filepath:
            if os.path.isfile(filepath):
                raise TypeError('This file is already exist!!')
            cmpfilepath = filepath
        # 如果path不存在而self.source_cirfilepath存在，则将cir_data存入该文件中，该文件可新建也可已存在，类似于save
        elif self.source_cmpfilepath:
            cmpfilepath = self.source_cirfilepath
        else:
            raise TypeError('The directory to save the file is needed!!')

        # 以写的方式打开cmpfilepath文件路径
        with open(cmpfilepath, 'w') as file:
            wr_cmp_file_sta(file)
            file.write(str(comp_data))
            wr_file_end(file)

        # 记录文件源
        self.source_cmpfilepath = filepath


if __name__ == '__main__':
    cirfile = File()
