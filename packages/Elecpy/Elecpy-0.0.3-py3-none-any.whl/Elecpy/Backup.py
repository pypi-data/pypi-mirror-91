"""
该模块放置一些备份的程序段
"""
from Elecpy.Circuit import *
from Elecpy.Default import *
import copy
from Elecpy.File import *


class Project:
    """
    class: 项目，管理若干电路
    """
    def __init__(self,
                 root_path=None):
        """
        method: 创建一个项目
        :param root_path: 项目根目录
        """
        if root_path is None:
            raise TypeError('请输入根目录root_path')
        self.root_path = root_path

        """内部变量"""
        # 电路数据
        self.cirs_data = {}
        # 电路集合
        self.cir_obj = None
        self.content = None

        """读取所有电路的数据"""
        self.load_cirs_data()

    def cir_content(self,
                    pframe=None):
        """
        method: 电路文件的目录
        :param pframe: 父frame
        :return: None
        """
        cont_data = pd.DataFrame({'directory': [],
                                 'file': []})
        for i, directory in enumerate(os.listdir(self.root_path)):
            dir_path = os.path.join(self.root_path, directory)
            for j, file in enumerate(os.listdir(dir_path)):
                file = file.replace('.xlsx', '')
                data = pd.DataFrame({'directory': [directory],
                                     'file': [file]})
                cont_data = cont_data.append(data,
                                             ignore_index=True)
        self.content = Contents(pframe=pframe,
                                wdg_height=250,
                                cont_data=cont_data,
                                open_flag=(True, False))

    def load_cirs_data(self):
        """
        method: 加载所有电路的数据
        :return:
        """
        for i, directory in enumerate(os.listdir(self.root_path)):
            dir_path = os.path.join(self.root_path, directory)
            for j, file in enumerate(os.listdir(dir_path)):
                cir_id = file.replace('.xlsx', '')
                cir_data_path = os.path.join(self.root_path, directory, file).replace('\\', '/')
                comps_data = pd.read_excel(io=cir_data_path,
                                           sheet_name='comps_data')
                wires_data = pd.read_excel(io=cir_data_path,
                                           sheet_name='wires_data')
                cirdata = {'comps_data': comps_data, 'wires_data': wires_data}

                self.cirs_data[cir_id] = cirdata

    def create_circuit(self,
                       cir_id=None,
                       pframe=None,
                       cav_width=None,
                       cav_height=None):
        """
        method: 创建电路
        :param cir_id: 电路id
        :param pframe: 父frame
        :param cav_width: 画布宽度
        :param cav_height: 画布高度
        :return:
        """
        if cir_id in self.cirs_data.keys():
            cirdata = self.cirs_data[cir_id]
            self.cir_obj = CirDiagram(cir_id=cir_id,
                                   pframe=pframe,
                                   cav_width=cav_width,
                                   cav_height=cav_height,
                                   **cirdata)
            self.cir_obj.mode_normal()
            # self.cir_obj.calc_sin_steady_cir()

    def new_circuit(self,
                    cir_id=None,
                    pframe=None,
                    cav_width=None,
                    cav_height=None):
        """
        method: 创建新的电路
        :param cir_id:
        :param pframe: 父frame
        :param cav_width: 画布宽
        :param cav_height: 画布高
        :return:
        """
        self.cir_objs = CirDiagram(cir_id=cir_id,
                                pframe=pframe,
                                cav_width=cav_width,
                                cav_height=cav_height)


if __name__ == '__main__':
    cir = Circuit(cir_name='test')
    cir.add_res(designator='R-3')
    crd = (60, 60)
    cir.select(crd)

    # cir.add_component(comp_nm='resistor')
    print(cir.source_data)
