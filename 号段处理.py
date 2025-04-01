#!/usr/bin/env python
# coding: utf-8
########################################
## 号段处理工具
########################################
import glob
import os
import re
import sys
lib_dir = os.path.join(os.getcwd(), 'pylib')
sys.path.append(lib_dir)
import xlrd

smc_num_file = 'files/SMC_Num.txt'
SF_file = 'files/SF.txt'
QH_file = 'files/QH.txt'
ID_file = 'files/彩铃省份ID.txt'
folder_path = '新增号段'

# 定义省份名称与短信中心地址对应关系
def SMC_Num_Init():
    # 定义省份列表
    province_name = []
    # 定义短信中心地址列表
    smc_addr = []
    with open(smc_num_file, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.split('=')
            # 省份添加至列表中,去除省份前后空格
            province_name.append(line[0].strip())
            # 短信中心地址添加至列表中，去除短信中心前后空格
            smc_addr.append(line[1].strip())
    # 返回省份名称列表、短信中心地址列表
    return province_name, smc_addr

# 定义省份名称与省份缩写对应关系
def SF_Num_Init():
    # 定义省份列表
    SF_name01 = []
    # 定义缩写列表
    SX_addr = []
    with open(SF_file, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.split('=')
            # 缩写添加至列表中,去除省份前后空格
            SX_addr.append(line[0].strip())
            # 省份添加至列表中，去除前后空格
            SF_name01.append(line[1].strip())
    # 返回省份名称列表、短信中心地址缩写列表
    return SF_name01, SX_addr

# 定义省份名称与区号对应关系
def QH_Num_Init():
    # 定义省份列表
    SF_name02 = []
    # 定义区号列表
    QH_addr = []
    with open(QH_file, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.split('=')
            # 区号添加至列表中,去除省份前后空格
            QH_addr.append(line[1].strip())
            # 省份添加至列表中，去除前后空格
            SF_name02.append(line[0].strip())
    # 返回省份名称列表、区号列表
    return SF_name02, QH_addr

def ID_Num_Init():
    # 定义省份列表
    SF_name03 = []
    # 定义区号列表
    ID_addr = []
    with open(ID_file, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.split('=')
            # ID添加至列表中,去除省份前后空格
            ID_addr.append(line[1].strip())
            # 省份添加至列表中，去除前后空格
            SF_name03.append(line[0].strip())
    # 返回省份名称列表、区号列表
    return SF_name03, ID_addr

def Init_Config(province_name, smc_addr, SF_name01, SX_addr, SF_name02, QH_addr, SF_name03, ID_addr):
    try:
        file_list = os.listdir('新增号段')
        start_col = 3
        #print(file_list)
        out_filename = '号段处理' + '.txt'
        with open(out_filename, 'r+') as f:
            f.truncate(0)
        #号首所在的行列
        for excel_file in file_list:
            if '中国广电' in excel_file:
                start_row = 2
                spare = 1
                suffix = ''
                carrier = '广电'
            elif '中国电信' in excel_file:
                start_row = 3
                spare = 0
                carrier = '电信'
                suffix = '_DX'
            elif '中国联通' in excel_file:
                start_row = 1
                spare = 0
                carrier = '联通'
                suffix = '_LT'
            elif '中国移动' in excel_file:
                start_row = 2
                spare = 0
                carrier = '移动'
                suffix = '_YD'
            # print(excel_file)
            #print(start_row)
            # 判断xlsx文件在当前目录中
            file_list = os.path.join(folder_path, excel_file)
            rd = xlrd.open_workbook(file_list)
            # 获取sheet列表，sheet名称为号段首部
            # print('ALL sheets: %s' % rd.sheet_names())
            sheet1 = rd.sheets()[0]
            sheet1_name = sheet1.name
            sheet1_cols = sheet1.ncols
            sheet1_nrows = sheet1.nrows
            # 输出sheet名称，总列数，总行数
            #print('Sheet1 Name: %s\nSheet1 cols: %s\nSheet1 rows: %s' % (sheet1_name, sheet1_cols, sheet1_nrows))
            if rd.sheet_loaded(sheet1_name):
                # 通过页签名来获取页签中的对象
                p = rd.sheet_by_name(sheet1_name)
                # 获取表格第一行名称
                # print(p.row_values(rowx=0))
                # 通过页签对象获取页签中的有效行数
                rows = p.nrows
                # 读取列数据
                for i in range(start_col, sheet1_cols-spare):
                    cell1 = sheet1.row(start_row-1)[i].value
                    if type(cell1) is float:
                        cell1 = str(int(cell1))
                    else:
                        cell1 = str(cell1)
                    cell1 = cell1[:4]
                    #print('%s' % (cell1))
                    # 读取每行的数据，返回数据为列表,从第三行读取，跳过第一二行，第一二行为列的定义
                    for line in range(start_row, rows):
                        # 判断行数据不为空
                        if len(p.row_values(rowx=line)[0]) > 0:
                            # 获取号段所属省份
                            phone_num_province = p.row_values(rowx=line)[0]
                            # 获取号段
                            phone_num_detail = p.row_values(rowx=line)[i]
                            if type(phone_num_detail) is float:
                                phone_num_detail = str(int(phone_num_detail))
                            # 判断号段不为空
                            if len(phone_num_detail) > 0:
                                # print(phone_num_head,phone_num_province,phone_num_suffix)
                                phone_num_suffix_list = Suffix_Init(phone_num_detail)
                                # 打印号段后缀
                                # print(phone_num_suffix_list)
                                # # 打印号段号头部
                                # print(phone_num_head)
                                #
                                # # 打印省份
                                # print(phone_num_province)
                                # 根据省份获取短信中心号码
                                smc_addr_info = smc_addr[province_name.index(phone_num_province)]

                                # 根据省份获取短信中心缩写
                                SX_addr_info = SX_addr[SF_name01.index(phone_num_province)]
                                sx_addr_info = SX_addr_info.lower()
                                # 根据省份获取区号
                                QH_addr_info = QH_addr[SF_name02.index(phone_num_province)]
                                #根据省份获取彩铃省份ID
                                ID_addr_info = ID_addr[SF_name03.index(phone_num_province)]

                                for n in phone_num_suffix_list:
                                    split_phone_num = "%s%s|%s|%s|%s|%s|%s|%s|%s" % (
                                        cell1, n, smc_addr_info, phone_num_province, carrier, SX_addr_info, sx_addr_info, QH_addr_info, ID_addr_info)
                                    with open(out_filename, 'a') as f:
                                        print(split_phone_num, file=f)

        print('号段处理成功！')

    except Exception as e:
        print(e)



# 号段后缀处理
def Suffix_Init(phone_num_suffix):
    # 处理号段中连续号段，即号段中000-029 连续号段
    phone_num_suffix_list = re.split('[,、]', phone_num_suffix)
    # 定义新号段列表
    phone_num_suffix_list_new = []

    for line_info in phone_num_suffix_list:
        if '-' in line_info:
            line_info_list = line_info.split('-')
            # 根据连续号段进行拆分
            for line_info_detail in range(int(line_info_list[0]), int(line_info_list[1]) + 1):
                m = "%03d" % line_info_detail
                # 将差分后的记录写入列表中
                phone_num_suffix_list_new.append(m)
        else:
            phone_num_suffix_list_new.append(line_info)

    return phone_num_suffix_list_new




if __name__ == '__main__':
    # 格式化省份短信中心信息
    province_name, smc_addr = SMC_Num_Init()
    SF_name01, SX_addr = SF_Num_Init()
    SF_name02, QH_addr = QH_Num_Init()
    SF_name03, ID_addr = ID_Num_Init()
    # 格式化好短信息生成号段添加内容
    Init_Config(province_name, smc_addr, SF_name01, SX_addr, SF_name02, QH_addr, SF_name03, ID_addr)
