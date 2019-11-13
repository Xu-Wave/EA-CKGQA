# coding=utf-8
# Version:python3.6.0
# Tools:Pycharm 2019
__date__ = '2019/4/24 下午12:34'
__author__ = 'TT'

import GstoreConnector

# before you run this example, make sure that you have started up ghttp service (using bin/ghttp db_name port)
username = "endpoint"
password = "123"
filename = "res.txt"


def net(sparql1):
    """
    实现gStore的API连接，以及进行查询，后续会根据问题的类型进行相应的一些选项修改
    :param sparql1: 查询语句1，以后可能会有查询语句2、3、4...
    """
    gc = GstoreConnector.GstoreConnector("pkubase.gstore-pku.com", 80)
    gc.fquery(username, password, "pkubase", sparql1, filename)
    print(gc.query(username, password, "pkubase", sparql1))

# unload the database
# ret = gc.unload("test", username, password)

# load the database 
# ret = gc.load("lubm", username, password)

# query
# print(gc.query(username, password, "pkubase", sparql))

# query and save the result in a file
# gc.fquery(username, password, "pkubase", sparql, filename)
