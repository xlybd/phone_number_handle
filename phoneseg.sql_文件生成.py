#!/usr/bin/env python
# coding: utf-8
########################################
## 彩铃phoneseg.sql文件生成
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
    # 定义彩铃身份ID
    ID_addr = []
    for line in open(process_file):
        line = line.strip()
        line = line.split('|')
        split_num.append(line[0].strip())
        ID_addr.append(line[7].strip())
    # 返回列表
    return split_num, ID_addr


def Init_Config(split_num, ID_addr):
    try:
        out_filename = 'phoneseg.sql'
        with open(out_filename, 'w') as f:
            f.write('INSERT INTO TV_PHONESEG (STARTCODE,ENDCODE,PROVINCEID,HCODE) VALUES\n')
        for num in split_num:
            ID_addr_info = ID_addr[split_num.index(num)]

            split_phone_num = "('%s0000','%s9999','%s','000')," % (num, num, ID_addr_info)
            with open(out_filename, 'a') as f:
                print(split_phone_num, file=f)
        print('phoneseg.sql文件生成成功！')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 格式化号段处理信息
    split_num, ID_addr = Num_Process()
    Init_Config(split_num, ID_addr)
