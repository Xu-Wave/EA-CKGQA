import time
from bert_base.client import BertClient


def ner_on_work(str_input):
    with BertClient(show_server_config=False, check_version=False, check_length=False, mode='NER') as bc:
        start_t = time.perf_counter()
        str_input_list = list(str_input)
        rst = bc.encode([str_input])
        result = list(rst[0])
        print('rst:', result)
        print(time.perf_counter() - start_t)

        entity_list = []
        entity_list_number = 0
        if (result.count('B-LOC') == 1 and result.count('B-ORG') == 0 and result.count('B-PER') == 0) \
                or (result.count('B-LOC') == 0 and result.count('B-ORG') == 1 and result.count('B-PER') == 0) \
                or (result.count('B-LOC') == 0 and result.count('B-ORG') == 0 and result.count('B-PER') == 1):
            for every in result:
                if every != 'O':
                    entity_list.append(str_input_list[entity_list_number])
                entity_list_number += 1
            entity_str = "".join(entity_list)
            return entity_str
        else:
            print('属于多实体问题，需要单独进行处理')
            return None
