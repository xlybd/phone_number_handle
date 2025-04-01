#!/usr/bin/env python
# coding: utf-8
########################################
## 网关本地MT文件生成
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
    # 定义省份列表
    province_name = []
    # 定义运营商列表
    carrier_name = []
    # 定义省份缩写列表
    SX_addr = []
    for line in open(process_file):
        line = line.strip()
        line = line.split('|')
        split_num.append(line[0].strip())
        province_name.append(line[2].strip())
        carrier_name.append(line[3].strip())
        SX_addr.append(line[4].strip())
    # 返回列表
    return split_num, province_name, carrier_name, SX_addr


def Init_Config(split_num, province_name, carrier_name, SX_addr):
    try:
        out_filename = '本地MT.txt'
        with open(out_filename, 'w') as f:
            f.write('Version:1.1\nencrypt:1\nFileInfo:LocalMTRoute\n')
        for num in split_num:
            phone_num_province = province_name[split_num.index(num)]
            carrier = carrier_name[split_num.index(num)]
            SX_addr_info = SX_addr[split_num.index(num)]


            split_phone_num = "SMC_%s_S,%s,      ,%s%s,        ,0" % (
                SX_addr_info, num, phone_num_province, carrier)
            with open(out_filename, 'a') as f:
                print(split_phone_num, file=f)
        print('本地MT.txt文件生成成功！')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 格式化号段处理信息
    split_num, province_name, carrier_name, SX_addr = Num_Process()
    Init_Config(split_num, province_name, carrier_name, SX_addr)
