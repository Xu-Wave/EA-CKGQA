# coding = UTF-8
__Date__ = '2019/7/19'
__Author__ = 'Xu Tao'

import os
import signal
import subprocess
import time
import TT_Mission_gStore
import cixing_LTP词性标注  # 词性标注目录信息
from pyltp import Postagger  # 词性标注
import cos_sim_and_delete_get_type  # 余弦值计算以及清除get_type的信息
import entity_keywords_chou  # 抽取关键词列表
import jieba
import process_every_逐个扫描函数  # 需要单独处理复杂问题时才使用
# 以下为队友写的代码
import z_NLP
import z_NLP_result
import z_inget
# 以上为队友写的代码
from bert_serving.client import BertClient
import NER_test  # 自动NER
import mention2ent_file_test  # 自动消歧
import sys

sys.path.append('./ltp_function')
sys.path.append('./auto_NER')
sys.path.append('./实体消歧')

jieba.load_userdict('dict1.txt')  # 第一步加载字典

question_file_number = 0  # question文件默认行数，等会遍历执行的时候直接加到1，这样执行也可以

question_file = open('question_done.txt', encoding='utf-8-sig')
answer_file = open('finally_result.txt', 'a+')

alone_to_do_question_number = []  

content = question_file.read().splitlines()

for each_question in content:
    question_file_number += 1
    print('此问题序号 = ', question_file_number, each_question)
    answer_file.flush()
    
    if alone_to_do_question_number.count(question_file_number) == 0:
        start_ner_mission = subprocess.Popen('. /home/xt/PycharmProjects/CCKS_END/auto_NER/start_ner', shell=True,
                                             close_fds=True, preexec_fn=os.setsid)
        print('ner服务开启成功，pid为：', start_ner_mission.pid)
        time.sleep(3)  # 等待ner服务完全开启

        wei_true_index = -1  # 记录实体的当前索引，词性标注会跳过此索引

        ready_entity = NER_test.ner_on_work(each_question)
        print('待消歧实体为：', ready_entity)
        if ready_entity is None:
            answer_file.write('\n')
            os.killpg(start_ner_mission.pid, signal.SIGUSR1)
            cos_sim_and_delete_get_type.delete_get_type()
            time.sleep(1)  # 等待ner服务完全关闭
            continue
        true_entity = mention2ent_file_test.mention2ent_on_work(ready_entity)
        if true_entity is None:
            answer_file.write('\n')
            os.killpg(start_ner_mission.pid, signal.SIGUSR1)
            cos_sim_and_delete_get_type.delete_get_type()
            time.sleep(1)  # 等待ner服务完全关闭
            continue
        print('消歧后的真实体为：', true_entity)
        gStore_List = [true_entity]
        print('消歧后马上的gStore列表为：', gStore_List)
        os.killpg(start_ner_mission.pid, signal.SIGUSR1)
        time.sleep(1)  # 等待ner服务完全关闭
        # 接下来进行常规操作
        start_bert_mission = subprocess.Popen('. /home/xt/PycharmProjects/CCKS_END/start_bert_vector', shell=True,
                                              close_fds=True, preexec_fn=os.setsid)
        print('bert服务开启成功，pid为：', start_bert_mission.pid)

        seg_list = list(jieba.cut(each_question))  # 分词处理，并且转化为列表形式

        wei_true_index = seg_list.count(ready_entity)
        if wei_true_index == 0:
            wei_true_index = -1
        else:
            wei_true_index = seg_list.index(ready_entity)

        print('seg_list为：', seg_list)  # 分词后的列表
        print('现在的gStore_List为：', gStore_List)  # 确定好的三元组
        postagger = Postagger()  # 初始化实例
        postagger.load(cixing_LTP词性标注.pos_model_path)  # 加载模型
        postags_str = postagger.postag(seg_list)  # 对列表进行词性标注,并输出为str
        postags = list(postags_str)  # 转化为列表
        print(postags)  # 打印列表
        postagger.release()  # 释放模型

        Keywords_List = entity_keywords_chou.keyword_chou(postags, 1, wei_true_index, seg_list)
        print('Keywords_List为：', Keywords_List)
        ls = []
        dict1 = {}
        if len(gStore_List) == 0:  # 如果得出的三元组为空，则自动跳过
            answer_file.write('\n')
            os.killpg(start_bert_mission.pid, signal.SIGUSR1)
            cos_sim_and_delete_get_type.delete_get_type()
            time.sleep(1)  # 给bert关闭时间作缓冲
            continue
        if len(gStore_List) == 2:  # 如果得出的三元组已经有了实体和属性，则直接进行查询
            triple_flag = 1  # 若三元组已经为1，则不向量化等后续操作，后续的操作函数无效
            TT_Mission_gStore.net(z_NLP_result.nlp(gStore_List))
            tiaoguo = z_NLP_result.inget()  # inget函数中存在最终检索不到结果的情况，此标志位用于跳过此情况，减少bug
            if tiaoguo == 1:
                tiaoguo = 0
                answer_file.write('\n')
                os.killpg(start_bert_mission.pid, signal.SIGUSR1)
                cos_sim_and_delete_get_type.delete_get_type()
                time.sleep(1)  # 给bert关闭时间作缓冲
                continue
        else:
            G = gStore_List
            TT_Mission_gStore.net(z_NLP.nlp(G))
            z_inget.getlist()  # 提取属性
            time.sleep(6)  # 给bert开启时间作缓冲
            bc = BertClient()
            f = open('get_type.txt', 'r')
            content = f.read().splitlines()
            c = 0
            if len(content) == 0:
                answer_file.write('\n')
                os.killpg(start_bert_mission.pid, signal.SIGUSR1)
                cos_sim_and_delete_get_type.delete_get_type()
                time.sleep(1)  # 给bert关闭时间作缓冲
                continue
            if len(Keywords_List) == 0:
                answer_file.write('\n')
                os.killpg(start_bert_mission.pid, signal.SIGUSR1)
                cos_sim_and_delete_get_type.delete_get_type()
                time.sleep(1)  # 给bert关闭时间作缓冲
                continue
            for a in Keywords_List:
                if c - 0.99 >= 0:
                    break
                for b in content:
                    vector_a = bc.encode([a])
                    vector_b = bc.encode([b])
                    c = cos_sim_and_delete_get_type.cos_sim(vector_a, vector_b)
                    print(c, a, b)
                    dict1[c] = b
            keys = list(dict1.keys())
            keys.sort(reverse=True)
            print(keys)
            print(dict1)
            ls.append(dict1[keys[0]])

            if len(ls) == 0:
                answer_file.write('\n')
                os.killpg(start_bert_mission.pid, signal.SIGUSR1)
                cos_sim_and_delete_get_type.delete_get_type()
                time.sleep(1)  # 给bert关闭时间作缓冲
                continue

            print('抽取得到的属性是：', dict1[keys[0]])
            s = set(ls)
            l = list(s)
            gStore_List.extend(l)
            print(gStore_List)
            # aaa(gStore_List)
            TT_Mission_gStore.net(z_NLP_result.nlp(gStore_List))
            z_NLP_result.inget()
            cos_sim_and_delete_get_type.delete_get_type()
        print('此问题序号 = ', question_file_number, each_question)
        os.killpg(start_bert_mission.pid, signal.SIGUSR1)
        time.sleep(1)  # 给bert关闭时间作缓冲

    else:
        start_bert_mission = subprocess.Popen('. /home/xt/PycharmProjects/CCKS_END/start_bert_vector', shell=True,
                                              close_fds=True, preexec_fn=os.setsid)
        print('bert服务开启成功，pid为：', start_bert_mission.pid)

        wei_index = -1  # 记录手工规则得到的真实体的当前索引，词性标注会跳过此索引
        entity_flag = 0  # 若实体已经经过分词扫描被确定了，则 entity_flag = 1，否则为0
        triple_flag = 0  # later

        seg_list = list(jieba.cut(each_question))  # 分词处理，并且转化为列表形式
        seg_list, gStore_List, entity_flag, wei_index = process_every_逐个扫描函数.process_every(seg_list, entity_flag,
                                                                                           wei_index)
        # 分词的时候便将第一个实体确定下来，保存在gStore_List中
        print('seg_list为：', seg_list)  # 分词后的列表
        print('gStore_List为：', gStore_List)  # 确定好的三元组
        print('entity_flag为：', entity_flag)  # 实体是否被确定的标志位，执行到此，此位必定为1

        postagger = Postagger()  # 初始化实例
        postagger.load(cixing_LTP词性标注.pos_model_path)  # 加载模型
        postags_str = postagger.postag(seg_list)  # 对列表进行词性标注,并输出为str
        postags = list(postags_str)  # 转化为列表
        print(postags)  # 打印列表
        postagger.release()  # 释放模型

        Keywords_List = entity_keywords_chou.keyword_chou(postags, entity_flag, wei_index, seg_list)
        print('Keywords_List为：', Keywords_List)

        ls = []
        dict1 = {}
        if len(gStore_List) == 0:  # 如果得出的三元组为空，则自动跳过
            answer_file.write('\n')
            os.killpg(start_bert_mission.pid, signal.SIGUSR1)
            cos_sim_and_delete_get_type.delete_get_type()
            time.sleep(1)  # 给bert关闭时间作缓冲
            continue

        if len(gStore_List) == 2:  # 如果得出的三元组已经有了实体和属性，则直接进行查询
            triple_flag = 1  # 若三元组已经为1，则不向量化等后续操作，后续的操作函数无效
            TT_Mission_gStore.net(z_NLP_result.nlp(gStore_List))
            tiaoguo = z_NLP_result.inget()  # inget函数中存在最终检索不到结果的情况，此标志位用于跳过此情况，减少bug
            if tiaoguo == 1:
                tiaoguo = 0
                answer_file.write('\n')
                os.killpg(start_bert_mission.pid, signal.SIGUSR1)
                cos_sim_and_delete_get_type.delete_get_type()
                time.sleep(1)  # 给bert关闭时间作缓冲
                continue
        else:
            G = gStore_List
            TT_Mission_gStore.net(z_NLP.nlp(G))
            z_inget.getlist()  # 提取属性
            time.sleep(6)  # 给bert开启时间作缓冲
            bc = BertClient()
            f = open('get_type.txt', 'r')
            content = f.read().splitlines()
            c = 0
            if len(content) == 0:
                answer_file.write('\n')
                os.killpg(start_bert_mission.pid, signal.SIGUSR1)
                cos_sim_and_delete_get_type.delete_get_type()
                time.sleep(1)  # 给bert关闭时间作缓冲
                continue
            if len(Keywords_List) == 0:
                answer_file.write('\n')
                os.killpg(start_bert_mission.pid, signal.SIGUSR1)
                cos_sim_and_delete_get_type.delete_get_type()
                time.sleep(1)  # 给bert关闭时间作缓冲
                continue

            for a in Keywords_List:
                if c - 0.99 >= 0:
                    break
                for b in content:
                    vector_a = bc.encode([a])
                    vector_b = bc.encode([b])
                    c = cos_sim_and_delete_get_type.cos_sim(vector_a, vector_b)
                    print(c, a, b)
                    dict1[c] = b
            keys = list(dict1.keys())
            keys.sort(reverse=True)
            print(keys)
            print(dict1)
            ls.append(dict1[keys[0]])

            if len(ls) == 0:
                answer_file.write('\n')
                os.killpg(start_bert_mission.pid, signal.SIGUSR1)
                cos_sim_and_delete_get_type.delete_get_type()
                time.sleep(1)  # 给bert关闭时间作缓冲
                continue

            print('抽取得到的属性是：', dict1[keys[0]])
            s = set(ls)
            l = list(s)
            gStore_List.extend(l)
            print(gStore_List)
            TT_Mission_gStore.net(z_NLP_result.nlp(gStore_List))
            z_NLP_result.inget()
            cos_sim_and_delete_get_type.delete_get_type()
        print('此问题序号 = ', question_file_number, each_question)
        os.killpg(start_bert_mission.pid, signal.SIGUSR1)
        time.sleep(1)  # 给bert关闭时间作缓冲
