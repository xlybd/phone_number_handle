#!/usr/bin/env python
# coding: utf-8
########################################
## 短信中心号段处理工具
########################################
import glob
import os
import re
import sys
import xlrd

smc_num_file = 'files/SMC_Num.txt'
SF_file = 'files/SF.txt'
QH_file = 'files/QH.txt'
province_name_BQ = ['安徽', '北京', '甘肃', '河北', '黑龙江', '吉林', '江苏', '辽宁', '内蒙古', '宁夏', '青海', '山东',
                    '陕西', '山西', '天津', '新疆']
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

def Init_Config(province_name, smc_addr, SF_name01, SX_addr, SF_name02, QH_addr):
    try:
        file_list = os.listdir('新增号段')
        start_col = 3
        #print(file_list)
        #号首所在的行列
        for excel_file in file_list:
            if '中国广电' in excel_file:
                start_row = 2
                suffix = ''
                carrier = '广电'
                year = input("输入广电号段年份例如：2024\n")
                batch = input("输入广电号段批次（大写）例如：一\n")
            elif '中国电信' in excel_file:
                start_row = 3
                carrier = '电信'
                suffix = '_DX'
                year = input("输入电信号段年份例如：2024\n")
                batch = input("输入电信号段批次（大写）例如：一\n")
            elif '中国联通' in excel_file:
                start_row = 1
                carrier = '联通'
                suffix = '_LT'
                year = input("输入联通号段年份例如：2024\n")
                batch = input("输入联通号段批次（大写）例如：一\n")
            elif '中国移动' in excel_file:
                start_row = 2
                carrier = '移动'
                suffix = '_YD'
                year = input("输入移动号段年份例如：2024\n")
                batch = input("输入移动号段批次（大写）例如：一\n")
            out_filename = 'SMSC_群组表_' + carrier + '.txt'
            with open(out_filename, 'w') as f:
                print('groupname:名称,Remark:备注,addr:号首,matchlen:匹配长度,Remark:备注',
                      file=f)
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
                for i in range(start_col, sheet1_cols-1):
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
                            if phone_num_province in province_name_BQ:

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
                                    # 遍历后缀列表，生成短信中心SMC鉴权表新增配置
                                    QH_addr_info = QH_addr[SF_name02.index(phone_num_province)]

                                    for n in phone_num_suffix_list:
                                        split_phone_num = "BQ%s%s(group),,86%s%s,13,%s%s%s年第%s批号段" % (
                                        SX_addr_info, suffix, cell1, n, phone_num_province, carrier, year, batch)
                                        with open(out_filename, 'a') as f:
                                            print(split_phone_num, file=f)

        print('SMSC_群组表文件生成成功！')

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
    # 格式化好短信息生成号段添加内容
    Init_Config(province_name, smc_addr, SF_name01, SX_addr, SF_name02, QH_addr)
