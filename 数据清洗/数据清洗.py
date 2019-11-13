# coding = UTF-8
__Date__ = '2019/6/30'
__Author__ = 'Xu Tao'
# TODO 注意对空格的清洗！！！
import jieba
import re  # 使用正则表达式

filename = "./questions1.txt"
stopwords_file = "./stop_words.txt"
pattern = r"^q[1-766]:$"

stop_f = open(stopwords_file,"r",encoding='utf-8')
stop_words = list()
for line in stop_f.readlines():
    line = line.strip()
    if not len(line):
        continue
    stop_words.append(line)
stop_f.close

print(len(stop_words))

# f = open(filename,"r",encoding='utf-8')
f = open('question1.txt',"r",encoding='utf-8')

result = list()
for line in f.readlines():
    line = line.strip()
    if not len(line):
        continue
    outstr = ''
    seg_list = jieba.cut(line,cut_all=False)
    for word in seg_list:
        if word not in stop_words:
            if word != '\t':
                if re.match(pattern, word) is None:
                    outstr += word
                    outstr += ""
    result.append(outstr.strip())
f.close

with open("./question2.txt","w",encoding='utf-8') as fw:
    for sentence in result:
        sentence.encode('utf-8')
        data=sentence.strip()
        if len(data)!=0:
            fw.write(data)
            fw.write("\n")
print("end")
