#!/usr/bin/env python
# coding: utf-8
########################################
## 短信中心号段处理工具
########################################
import os
import sys
lib_dir = os.path.join(os.getcwd(), 'pylib')
sys.path.append(lib_dir)

process_file = '号段处理.txt'
# 获取号段处理信息
def Num_Process():
    # 定义号段列表
    split_num = []
    # 定义短信中心地址列表
    smc_addr = []
    # 定义省份列表
    province_name = []
    # 定义运营商列表
    carrier_name = []
    # 定义省份缩写列表
    SX_addr = []
    # 定义省份缩写小写列表
    sx_addr = []
    # 定义区号列表
    QH_addr = []
    # 定义彩铃身份ID
    ID_addr = []
    for line in open(process_file):
        line = line.strip()
        line = line.split('|')
        split_num.append(line[0].strip())
        smc_addr.append(line[1].strip())
        province_name.append(line[2].strip())
        carrier_name.append(line[3].strip())
        SX_addr.append(line[4].strip())
        sx_addr.append(line[5].strip())
        QH_addr.append(line[6].strip())
        ID_addr.append(line[7].strip())
    # 返回列表
    return split_num, smc_addr, province_name, carrier_name, SX_addr, sx_addr, QH_addr, ID_addr


def Init_Config(split_num, smc_addr, province_name, carrier_name, SX_addr, sx_addr, QH_addr, ID_addr):
    try:
        for num in split_num:
            smc_addr_info = smc_addr[split_num.index(num)]
            phone_num_province = province_name[split_num.index(num)]
            carrier = carrier_name[split_num.index(num)]
            SX_addr_info = SX_addr[split_num.index(num)]
            sx_addr_info = sx_addr[split_num.index(num)]
            QH_addr_info = QH_addr[split_num.index(num)]
            ID_addr_info = ID_addr[split_num.index(num)]

            split_phone_num = (num, smc_addr_info, phone_num_province, carrier, SX_addr_info, sx_addr_info, QH_addr_info, ID_addr_info)

            print(split_phone_num)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 格式化号段处理信息
    split_num, smc_addr, province_name, carrier_name, SX_addr, sx_addr, QH_addr, ID_addr = Num_Process()
    Init_Config(split_num, smc_addr, province_name, carrier_name, SX_addr, sx_addr, QH_addr, ID_addr)
