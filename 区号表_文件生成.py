#!/usr/bin/env python
# coding: utf-8
########################################
## 网关区号表文件生成
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
    # 定义区号列表
    QH_addr = []
    for line in open(process_file):
        line = line.strip()
        line = line.split('|')
        split_num.append(line[0].strip())
        province_name.append(line[2].strip())
        QH_addr.append(line[6].strip())
    # 返回列表
    return split_num, province_name, QH_addr


def Init_Config(split_num, province_name, QH_addr):
    try:
        out_filename = '区号表.txt'
        with open(out_filename, 'w') as f:
            f.write('Version:1.1\nencrypt:1\nFileInfo:AreaCode\n号码前缀,区号,计费用户号码归属省\n')
        for num in split_num:
            phone_num_province = province_name[split_num.index(num)]
            QH_addr_info = QH_addr[split_num.index(num)]

            split_phone_num = "%s  ,%s,%s" % (
                num, QH_addr_info, phone_num_province)
            with open(out_filename, 'a') as f:
                print(split_phone_num, file=f)
        print('区号表.txt文件生成成功！')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 格式化号段处理信息
    split_num, province_name, QH_addr = Num_Process()
    Init_Config(split_num, province_name, QH_addr, )
