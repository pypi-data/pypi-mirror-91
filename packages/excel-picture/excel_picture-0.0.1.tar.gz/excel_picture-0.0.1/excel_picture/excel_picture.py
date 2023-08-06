# -*- coding: utf-8 -*-
import base64
import re
import xml.dom.minidom as xmldom
import os
import zipfile
import shutil
import xlrd




def isfile_exist(file_path):
    if not os.path.isfile(file_path):
        print("It's not a file or no such file exist ! %s" % file_path)
        return False
    else:
        return True


# 复制并修改指定目录下的文件类型名，将excel后缀名修改为.zip
def copy_change_file_name(file_path, new_type='.zip'):
    if not isfile_exist(file_path):
        return ''

    extend = os.path.splitext(file_path)[1]  # 获取文件拓展名
    if extend != '.xlsx' and extend != '.xls':
        print("It's not a excel file! %s" % file_path)
        return False

    file_name = os.path.basename(file_path)  # 获取文件名
    new_name = str(file_name.split('.')[0]) + new_type  # 新的文件名，命名为：xxx.zip

    dir_path = os.path.dirname(file_path)  # 获取文件所在目录
    new_path = os.path.join(dir_path, new_name)  # 新的文件路径
    if os.path.exists(new_path):
        os.remove(new_path)
    shutil.copyfile(file_path, new_path)
    return new_path  # 返回新的文件路径，压缩包


# 解压文件
def unzip_file(zipfile_path):
    if not isfile_exist(zipfile_path):
        return False

    if os.path.splitext(zipfile_path)[1] != '.zip':
        print("It's not a zip file! %s" % zipfile_path)
        return False

    file_zip = zipfile.ZipFile(zipfile_path, 'r')
    file_name = os.path.basename(zipfile_path)  # 获取文件名
    zipdir = os.path.join(os.path.dirname(zipfile_path), str(file_name.split('.')[0]))  # 获取文件所在目录
    for files in file_zip.namelist():
        # print([os.path.join(zipfile_path, zipdir)])
        file_zip.extract(files, zipdir)  # 解压到指定文件目录
        # file_zip.extract(files)  # 解压到指定文件目录

    file_zip.close()
    return True


# 读取解压后的文件夹，打印图片路径
def read_img(excel_file_path):
    zipfile_path = str(os.path.splitext(excel_file_path)[0])
    img_dict = dict()
    dir_path = os.path.dirname(zipfile_path)  # 获取文件所在目录
    file_name = os.path.basename(zipfile_path)  # 获取文件名
    pic_dir = 'xl' + os.sep + 'media'  # excel变成压缩包后，再解压，图片在media目录
    pic_path = os.path.join(dir_path, str(file_name.split('.')[0]), pic_dir)
    file_list = os.listdir(pic_path)
    file_list.sort(key=lambda x: int(str(x).replace('image','').split('.')[0]))
    for file in file_list:
        filepath = os.path.join(pic_path, file)
        # print(filepath)
        img_index = int(re.findall(r'image(\d+)\.', filepath)[0])
        img_base64 = get_img_base64(img_path=filepath)
        img_dict[str(img_index)] = dict(img_index=img_index, img_path=filepath, img_base64=img_base64)

    return img_dict


# 获取img_base64
def get_img_base64(img_path):
    if not isfile_exist(img_path):
        return ""
    with open(img_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return 'data:image/jpeg;base64,%s' % s


def get_img_pos_info(excel_file_path,img_dict, img_feature):
    """解析xml 文件，获取图片在excel表格中的索引位置信息"""

    zip_file_path = str(os.path.splitext(excel_file_path)[0])
    os.path.dirname(zip_file_path)
    dir_path = os.path.dirname(zip_file_path)  # 获取文件所在目录
    file_name = os.path.basename(zip_file_path)  # 获取文件名
    xml_dir = 'xl' + os.sep + 'drawings' + os.sep + 'drawing1.xml'
    xml_path = os.path.join(dir_path, str(file_name.split('.')[0]), xml_dir)
    image_info_dict = parse_xml(xml_path, img_dict, img_feature=img_feature)  # 解析xml 文件， 返回图片索引位置信息
    return image_info_dict


# 重命名解压获取图片位置，及图片表格索引信息
def get_img_info(excel_file_path, img_feature):
    if img_feature not in ["img_index", "img_path", "img_base64"]:
        raise Exception('图片返回参数错误， ["img_index", "img_path", "img_base64"]')
    zip_file_path = copy_change_file_name(excel_file_path)
    if zip_file_path != '':
        if unzip_file(zip_file_path):
            img_dict = read_img(excel_file_path)  # 获取图片，返回字典，图片 img_index， img_index， img_path， img_base6
            image_info_dict = get_img_pos_info(zip_file_path, img_dict, img_feature)
            return image_info_dict
    return dict()


# 解析xml文件并获取对应图片位置
def parse_xml(file_name, img_dict, img_feature='img_path'):
    # 得到文档对象
    image_info = dict()
    dom_obj = xmldom.parse(file_name)
    # 得到元素对象
    element = dom_obj.documentElement
    def _f(subElementObj):
        # image_info = {}
        for anchor in subElementObj:
            xdr_from = anchor.getElementsByTagName('xdr:from')[0]
            col = xdr_from.childNodes[0].firstChild.data  # 获取标签间的数据
            row = xdr_from.childNodes[2].firstChild.data
            # print(anchor.getElementsByTagName('xdr:pic'))
            # print(anchor.getElementsByTagName('xdr:pic')[0])
            try:

                embed =anchor.getElementsByTagName('xdr:pic')[0].getElementsByTagName('xdr:blipFill')[0].getElementsByTagName(
                    'a:blip')[0].getAttribute('r:embed')  # 获取属性
            except Exception as e:
                print(e)
            # print(embed)
            image_info[(int(row), int(col))] = img_dict.get(str(embed.replace('rId', '')), {}).get(img_feature)
    sub_twoCellAnchor = element.getElementsByTagName("xdr:twoCellAnchor")
    # sub_oneCellAnchor = element.getElementsByTagName("xdr:oneCellAnchor")

    _f(sub_twoCellAnchor)
    # _f(sub_oneCellAnchor)
    return image_info



def main(file_path,img_feature='img_path'):
    img_col_index = [5, 6]
    book = xlrd.open_workbook(file_path)
    sheet = book.sheet_by_index(0)
    ncols = sheet.ncols
    c = []
    d = {}
    rows = []
    for q in range(0, ncols):
        rows.append(q)
    img_info_dict = get_img_info(file_path, img_feature)
    for i in img_info_dict.items():
        if int(i[0][1]) == rows[i[0][1]]:
            c.append({str(sheet.cell(0, int(i[0][1])).value): i[1]})
    for i in c:
        for key in i:
            if key not in d:
                d[key] = i[key]
            else:
                d[key] = ", ".join([d[key], i[key]])

    return d




if __name__ == '__main__':
    res = main(file_path='/Users/zhao/githubs/excel_picture/xianghe_moban.xlsx')
    print(res)


