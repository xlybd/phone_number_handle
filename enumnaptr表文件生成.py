#!/usr/bin/env python
# coding: utf-8
########################################
## enumnaptr表文件生成
########################################
import glob
import os
import sys
import datetime
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
        pattern = 'ENUMNAPTR*.txt'
        files = glob.glob(pattern)
        for file in files:
            os.remove(file)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
        out_filename = 'ENUMNAPTRQL' + timestamp + '.txt'
        rollbak_filename = 'ENUMNAPTRQL' + timestamp + '_rollbak.txt'

        with open(out_filename, 'w') as f:
            print('', file=f)
        with open(rollbak_filename, 'w') as f:
            print('', file=f)
        with open(out_filename, 'r+') as f:
            f.truncate(0)
        with open(rollbak_filename, 'r+') as f:
            f.truncate(0)
        for num in split_num:
            smc_addr_info = smc_addr[split_num.index(num)]
            phone_num_province = province_name[split_num.index(num)]
            carrier = carrier_name[split_num.index(num)]
            SX_addr_info = SX_addr[split_num.index(num)]
            sx_addr_info = sx_addr[split_num.index(num)]
            QH_addr_info = QH_addr[split_num.index(num)]
            ID_addr_info = ID_addr[split_num.index(num)]

            enumnaptr = "86%s|!^.*$!sip:info@%s.ims.mnc015.mcc460.3gppnetwork.org!|0|%s%s" % (
            num, sx_addr_info, phone_num_province, carrier)
            enumnaptr_rollbak = "86%s|!^.*$!sip:info@%s.ims.mnc015.mcc460.3gppnetwork.org!|1|%s%s" % (
                num, sx_addr_info, phone_num_province, carrier)
            with open(out_filename, 'a') as f:
                print(enumnaptr, file=f)
            with open(rollbak_filename, 'a') as f:
                print(enumnaptr_rollbak, file=f)

        print('enumnaptr表文件生成成功！')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 格式化号段处理信息
    split_num, smc_addr, province_name, carrier_name, SX_addr, sx_addr, QH_addr, ID_addr = Num_Process()
    Init_Config(split_num, smc_addr, province_name, carrier_name, SX_addr, sx_addr, QH_addr, ID_addr)
