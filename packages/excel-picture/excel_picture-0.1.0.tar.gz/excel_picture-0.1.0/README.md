# excel_picture
一个可以快速批量获取文件中的图片信息
基于python的实现的批量获取文件中的图片信息，并已json 形式展示，安装简单，可安装于python2或python3 环境中，用于web业务，博客，各种脚本中，等批量填充网站图片


## 1.如何安装


#### 使用pip 安装
```commandline
pip install  excel_picture
```


### 2.及使用示例 支持xlsx xls 等文件格式


```commandline
from excel_picture import main
res = main(file_path='test.xlsx')
print(res)
```


### 3.运行结果示例


```commandline
{'com': '/image2.png, /image33.png',
'com2':'/image1.png, /image3.png'}
```
### 4.结果讲解


key 对应的 文件的图片备注信息，支持中英文，尽量使用英文
value 为图片路径


### 5.联系我们


 <13073771301@163.com>