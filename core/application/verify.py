import re
import numpy as np
from core.application.helper import get_conf
from core.image import union_rbox

key_words = ["证明", "告知", "牡丹", "透支", "受理", '侦查',
             "侦察", "回执", "报案", "报案", "案件", '回告',
             "情况说明", "立案", "情况的说明"]
head_words = ["证明", "告知", "牡丹", "透支", "受理",
              "侦察", "回执", "报案", "案件", '回告', '侦查',
              "情况说明", "关于", "立案", "市", "公安"]
end_words = ['证明', '回执', '回复', '说明', '通知书', '回执单', '催告函'
                                                   '告知书', '报案函', '决定书', '报案书', '情况', '的函']

standard_heads = ['回告证明', '接受案件回执单', '案件侦查情况说明', '案件侦察情况说明', '牡丹卡恶意透支案件进展情况说明',
                  '牡丹卡恶意透支案件进展情况', '立案告知书', '侦查进展情况告知书', '案件侦察进展情况说明',
                  '案件侦查进展情况说明', '牡丹个人卡透支逾期还款催告函', '牡丹信用卡透支催收通知书',
                  '报警回执', '案件线索及材料收受回复', '受案回执', '原始追索记录', '尽职追索证明',
                  '受理回执', '报案函', '报案书', '立案决定书', '侦察证明', '证明']


def judge_have_word(word_list, sentence):
    for word in word_list:
        if word in sentence:
            return True
    return False


def is_head(record, height_ave):
    sen_temp = re.sub("[^\u4e00-\u9fa5]", "", record['words'])
    # print(record['words'])
    # print(record["position"]["height"]-height_ave)
    # return record["position"]["height"]-height_ave > 0 and\
    #     judge_have_word(head_words, sen_temp)
    return judge_have_word(head_words, sen_temp)


def filter(title_temp):
    for head in standard_heads:
        if head in title_temp:
            return head
    return ''


class Verify:
    """
    公安核查
    """

    def __init__(self, result):
        self.result = union_rbox(result, 3.5)
        self.res = {"verifyTitle": "", "verifyName": ""}
        try:
            self.title()
        except Exception as e:
            print(e)

        if self.res["verifyTitle"] == "":
            self.res["verifyName"] = ""

    def title(self):
        title = {}

        index = 0
        title_temp = ''
        height_ave = np.median([record['position']['height']
                                for record in self.result])
        for i in range(len(self.result)):
            if i > 2:
                break
            text = re.sub("[^\u4e00-\u9fa5]", "", self.result[i]['words'])
            if judge_have_word(key_words, text):
                index = i
                break
        if len(self.result[index]['words']) in range(2, 5) \
                or self.result[index]['words'][-2:] in end_words \
                or self.result[index]['words'][-3:] in end_words:
            title_temp = self.result[index]['words']

        if title_temp == '':
            title_temp_ = [self.result[i]["words"]
                           for i in range(min(len(self.result), 3))
                           if is_head(self.result[i], height_ave)]
            title_temp = "".join(title_temp_)

        title_temp = re.sub("[^\u4e00-\u9fa5]", "", title_temp)

        if '关于' in title_temp and '说明' in title_temp:
            if title_temp.index('关于') < title_temp.index('说明'):
                title_temp = title_temp[title_temp.index(
                    '关于'):title_temp.index('说明') + 2]
        elif '关于' in title_temp and '的函' in title_temp:
            if title_temp.index('关于') < title_temp.index('的函'):
                title_temp = title_temp[title_temp.index(
                    '关于'):title_temp.index('的函') + 2]
        else:
            title_temp = filter(title_temp)

        title['verifyTitle'] = title_temp

        self.res.update(title)

    def date(self):
        date = {}
        for i in range(len(self.result)):
            txt = self.result[i]['words']
            txt = txt.replace(' ', '')
            # 出生年月

            res = re.findall('\d*年\d*月\d*日', txt)
            if len(res) == 0:
                res = re.findall('\d*年\d*月', txt)

            if len(res) > 0:
                res_temp = res[0]
                date['time'] = res_temp
                self.res.update(date)
                break


# if __name__ == "__main__":
#     result = getocr('140.jpg', 0)
#     loss_temp = Verify(result, '')
#     # result_new = union_rbox(result,0)
#     for key in loss_temp.res.keys():
#         print('{}: {}'.format(key, loss_temp.res[key]))
