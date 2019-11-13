# coding=utf-8
# Version:python3.6.0
# Tools:Pycharm 2019
__date__ = '2019/5/24 下午10:33'
__author__ = 'TT'


def keyword_chou(form_pos_list, form_entity_flag, form_wei_index, form_seg_list):
    """
    实体确认过后，再执行此函数才有效；
    执行效果为 把实体index除去，其余关键词均放入列表中，并进行return输出，供向量化替换使用
    :param form_seg_list:分词列表
    :param form_pos_list:词性列表
    :param form_entity_flag:实体是否锁定的标志位
    :param form_wei_index:上面函数return出来的临时保存索引号，此函数中对此索引号自动过滤掉
    :return:返回所有除去实体以外的关键词
    """
    pos_list_count = 0  # 下方遍历计数使用
    Keywords_List = []  # 创建关键词列表
    for if_named in form_pos_list:
        if form_entity_flag == 1:  # 锁定标志位必须被锁定，即 = 1，此函数才有效
            if pos_list_count != form_wei_index:  # 过滤
                if if_named == 'n' or if_named == 'nh' or if_named == 'ni' or if_named == 'nl' \
                        or if_named == 'ns' or if_named == 'nt' or if_named == 'nz' or if_named == 'ws' or if_named == 'v':
                    Keywords_List.append(form_seg_list[pos_list_count])

        pos_list_count += 1
    return Keywords_List
