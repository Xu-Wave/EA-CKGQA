# coding = UTF-8
__Date__ = '2019/7/19'
__Author__ = 'Xu Tao'

import numpy as np


def cos_sim(vector_a, vector_b):
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim


def delete_get_type():
    f = open('get_type.txt', "a+")
    f.seek(0)
    f.truncate()  # 清空文件
