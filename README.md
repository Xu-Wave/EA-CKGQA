# EA-CKGQA

基于知识图谱的中文问答系统（EA-CKGQA）

CCKS2019 评测任务六

## Start.py是程序入口

由于是多人合作书写的代码，且比赛时间紧凑，

代码可读性不是很强，所以特意将整体思路分割成各个部分，

并对各个部分进行了详细的阐述，提供了复现所需要的所有文件。

## 项目介绍

此程序是CCKS2019评测任务六——基于知识图谱的中文问答系统而做的。

总排名第九名，排除百度、平安、华为、网易等企业分数，高校排名为第四名。

## 代码详解

### 对中文问题进行数据清洗（见目录）

由于官方给的问题集包含有很多冗余信息，所以我们对这些信息进行数据清洗，

具体清洗所用的停用词为stop_words.txt，

我们对stop_words.txt中的内容进行了删改，从而更适合我们的QA场景。

### 对中文问题进行命名实体识别（见目录）

此文件夹内为全部进行NER实现所需要的文件，

部分文件由于大小问题没有放在这里，但均给予了下载链接，

同时提供了我们方法的训练集、运行脚本等。

NER方法来自：
https://github.com/macanv/BERT-BiLSTM-CRF-NER

训练集和训练后的模型均已提供，

放入必要的依赖后，配置一下start_ner脚本内的模型路径，

使用NER_test中的ner_on_work函数，

即可在代码中使用。

### 对识别后的实体进行实体消歧（见目录）

pkubase-mention2ent.txt 文件下载地址
链接:https://pan.baidu.com/s/1MaZGxDg9KQrpZWE9bSAi0Q  密码:1cok

实体消歧所需要的文件下载地址
链接:https://pan.baidu.com/s/1Oa10t3t73zO13ydv1KcBFg  密码:sssa

### 使用gStore工具（见目录）

### 对实体进行召回所有子图等操作获得准确属性（见目录）

通过NER和实体消歧获得的准确实体，

抽取该实体下的所有子图，

并从子图中抽取所有待选属性，

并比较待选属性列表与关键词列表的余弦相似度，

从而从待选属性中找到最终的准确属性。


z_inget.py用于提取实体所对应的全部属性并存放到get_type.txt中；

entity_keywords_chou.py用于根据词性筛选出关键词列表；

start_bert_vector脚本用于开启Bert服务对候选属性列表和关键词列表向量化；

cos_sim_and_delete_get_type.py用于计算余弦相似度以及清空get_type.txt文件。

### Start.py中组建实体、属性查询语句，获得中文问题的最终答案。

## 额外的资源下载

Jieba分词使用的字典是我们通过mention2entity文件进行反向构建的

字典dict1.txt下载地址为：
链接:https://pan.baidu.com/s/1EOi-y7-dbNzKJEAjosQ3FA  密码:uhet


作者邮箱：xutaowk0@163.com
