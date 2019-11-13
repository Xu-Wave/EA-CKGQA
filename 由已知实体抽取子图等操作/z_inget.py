import json


# 此程序用于提取实体所对应的全部属性并存放到get_type.txt中
def getlist():
    path = r"./res.txt"  # json文件所在路径

    with open(path, "rb") as f:
        all_part = json.load(f)  # 读取所有文件内容
        results = all_part['results']  # 获取results标签下的内容
        results_bindings = results['bindings']  # 获取results标签下的bingdings内容
    # 定义一个list，将数据全部放到list中
    ls = []
    for res in results_bindings:
        res1 = res['x']
        res1 = res1['value']
        get_type = open("get_type.txt", "a+")
        get_type.write(res1)
        get_type.write('\n')
        if res1 not in ls:
            ls.append(res1)
    return ls
