# coding = UTF-8
__Date__ = '2019/7/4'
__Author__ = 'Xu Tao'

import re
import linecache

# process_in_data()函数所需参数
All_One_lie = []
All_Two_lie = []

# 在AllTwolie文本中进行全名称匹配，此文本中均为真实体，所以每个实体都是唯一的
line_number_All_Two_lie = 1  # 在AllTwolie文本中匹配到真实体时的行数

# 若查询不到真实体，此标志位会进行置位，接下来则会在伪实体中进行匹配
Two_to_One_flag = 0

# 若伪实体中查询到，则此标志位会进行置0，否则接下来我们构建手工规则，对此类现象单独进行处理
Man_doing_flag = 1

# 在AllOnelie文本中进行全名称匹配，此文本中均为伪实体，所以同一个content可能对应多个伪实体
line_number_All_One_lie = 1  # 在AllOnelie文本中匹配到伪实体时的行数，一般有多行

# 当找到多个伪实体时，我们将其伪实体的对应行数进行存储，以便后续消歧使用
ready_to_receive_numbers = []

# 将候选实体存放于列表中
ready_true_entities_flag = 0
ready_to_entities = []


# 情景是：
# 目前已经得到了一个具体的“实体”
# 这个实体可能是真实体，也可能是假实体
# 所以首先在txt中的第二列中去进行全名称匹配，如果匹配到，则直接归为真实体
# 如果未匹配到，则在第一列中进行匹配，如果匹配到，则取对应排名第一的真实体
# 否则则输出需要手工规则，等待我们去配置手工规则


def wash_in_data():  # 清洗数据
    All_line_number_in_wash = 1
    with open("pkubase-mention2ent.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        # print(lines)
    with open("清洗后的数据.txt", "w", encoding="utf-8") as f_w:
        for line in lines:
            Every_line = line.split()
            if len(Every_line) != 3:
                print(All_line_number_in_wash)
                continue
            f_w.write(line)
            All_line_number_in_wash += 1


def process_in_data():
    with open('清洗后的数据.txt', 'r', encoding="utf-8") as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
            Every_line = lines.split()  # 以空格来隔开每行的内容，并进行存储于列表中
            All_One_lie.append(Every_line[0])
            All_Two_lie.append(Every_line[1])

    with open('AllOnelie.txt', 'w+', encoding="utf-8") as write_to_All_One_lie:
        for One in All_One_lie:
            write_to_All_One_lie.write(One)
            write_to_All_One_lie.write('\n')

    with open('AllTwolie.txt', 'w+', encoding="utf-8") as write_to_All_Two_lie:
        for Two in All_Two_lie:
            write_to_All_Two_lie.write(Two)
            write_to_All_Two_lie.write('\n')


def mention2ent_on_work(ready_entity):
    del ready_to_entities[:]
    global line_number_All_Two_lie, Two_to_One_flag, line_number_All_One_lie, Man_doing_flag, ready_true_entities_flag
    # ready_entity = input('请输入待消歧实体：')
    content = r'^%s$' % ready_entity  # 全名称匹配的内容
    with open('AllTwolie.txt', 'r', encoding="utf-8") as in_All_Two_lie_get_entity:
        while True:
            lines = in_All_Two_lie_get_entity.readline()  # 整行读取数据
            if not lines:
                line_number_All_Two_lie = 1  # 恢复计数器
                Two_to_One_flag = 1
                print('Two_to_One_flag = 1, 该实体非真实体, 则在伪实体中查询其存在')
                break
            com_content = re.compile(content)  # 正则表达式的使用
            is_content = re.match(com_content, lines)
            if is_content:
                print(line_number_All_Two_lie)
                print('该实体为真实体, 可直接放入三元组第一位中')
                line_number_All_Two_lie = 1  # 恢复计数器
                return ready_entity
            line_number_All_Two_lie += 1

    if Two_to_One_flag == 1:  # 该实体为非真实体，所以现在在伪实体库中进行查询其存在
        Two_to_One_flag = 0  # 标志位恢复
        with open('AllOnelie.txt', 'r', encoding="utf-8") as in_All_One_lie_get_entity:
            while True:
                lines = in_All_One_lie_get_entity.readline()  # 整行读取数据
                if not lines:
                    if Man_doing_flag == 1:
                        print('Man_doing_flag = 1, 非伪实体, 则需要手工规则进行构建')
                        return None
                    break
                com_another_content = re.compile(content)
                is_another_content = re.findall(com_another_content, lines)
                if is_another_content:
                    Man_doing_flag = 0  # 如果找到，则标志位置0，表明用户不需要单独为此建立手工规则
                    # 如果找到，说明存在伪实体，即伪实体有潜力成为真实体，此时标志位置位，打开后续处理伪实体程序的开关
                    ready_true_entities_flag = 1
                    ready_to_receive_numbers.append(line_number_All_One_lie)  # 存储行数
                    print(line_number_All_One_lie)
                line_number_All_One_lie += 1
            Man_doing_flag = 1  # 标志位恢复
            line_number_All_One_lie = 1  # 行数计数恢复

            if ready_true_entities_flag == 1:
                for true_entity in ready_to_receive_numbers:
                    ready_to_entities.append(linecache.getline(r'AllTwolie.txt', true_entity))
            del ready_to_receive_numbers[:]
            ready_true_entities_flag = 0  # 标志位恢复
            print('消歧为：', ready_to_entities[0])
            return ready_to_entities[0]
