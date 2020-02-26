"""
本金查询
"""
import re
from core.application.helper import get_conf
from core.image import union_rbox, union_rbox2
from core.application.helper import check_bankcard


def startswith(str_, list_):
    for _ in list_:
        if str_.startswith(_):
            return True
    return False


def extract_card(lines):
    cards = []
    # boxs_valid = []
    card_pattern1 = re.compile('[0-9]{19}')
    card_pattern2 = re.compile('[0-9]{18}')
    card_pattern3 = re.compile('[0-9]{16}')
    card_pattern4 = re.compile('[0-9]{15}')
    for i in range(len(lines)):
        line = ''.join(lines[i])
        if ''.join(card_pattern1.findall(line)):
            cards += card_pattern1.findall(line)
        if ''.join(card_pattern2.findall(line)):
            cards += card_pattern2.findall(line)
        if ''.join(card_pattern3.findall(line)):
            cards += card_pattern3.findall(line)
        if ''.join(card_pattern4.findall(line)):
            cards += card_pattern4.findall(line)
    return cards


def get_dic(point1, point2):
    if point1['left'] - point2['left'] < 500:
        return 25*pow(point1['top'] + point1['height']/2
                      - point2['top']-point2['height']/2, 2) +\
            pow(point1['left'] + point1['width'] - point2['left'], 2)
    return 100000000000000


def extract_rmb(line):
    rmb_pattern = re.compile('([-0-9]{1,})([-0-9,.]{2,})')
    if rmb_pattern.findall(line):
        return ''.join(rmb_pattern.findall(line)[0])


def unify_rec(line):
    line = line.replace(" ", "")
    line = line.replace("/", "")
    line = line.replace('%', '')
    line = line.replace('全', '金')
    line = line.replace('生', '金')
    line = line.replace('会', '金')
    line = line.replace('木', '本')
    line = line.replace('B', '8')
    line = line.replace('S', '8')
    return line


def unify_rec1(line):
    line = line.replace(' 0.00 ', '')
    line = line.replace(' 0.0 ', '')
    line = line.replace(' .00 ', '')
    line = line.replace(' 0.000 ', '')
    line = line.replace(" ", "")
    line = line.replace("/", "")
    line = line.replace('%', '')
    line = line.replace('全', '金')
    line = line.replace('生', '金')
    line = line.replace('会', '金')
    line = line.replace('木', '本')
    line = line.replace('B', '8')
    line = line.replace('S', '8')
    return line


class Captial:
    """
    本金查询
    """

    def __init__(self, result):

        self.result_ori = result
        self.result = union_rbox(result, 0.5)
        self.res = {}

        self.res["card"] = ""
        self.res["rmb"] = ""
        self.res["principal"] = ""
        try:
            self.card()
        except Exception as e:
            print(e)
        try:
            self.principal()
        except Exception as e:
            print(e)
        try:
            self.rmb()
        except Exception as e:
            print(e)


#        self.res["confidence"] = ""
#        self.confidence()

    def predeal(self, result):
        new = []
        for res in result:
            res['box'] = (res['cx'], res['cy'], res['w'] +
                          res['cx'], res['cy']+res['h'])
            new.append(res)
        return new

    def rmb(self):
        # title = {}
        # index = 0
        # for i in range(len(self.result)):
        #     pass
        # title["title"] = self.result[index]["words"]
        # self.res.update(title)
        self.result = union_rbox(self.result_ori, 1)
        lines = [unify_rec1(self.result[i]["words"])
                 for i in range(len(self.result))]

        rmb = {}
        rmb_temp = ""
        for i in range(len(lines)):
            line = lines[i]
#            print(line)
            if '本金' in line and extract_rmb(line[line.index('本金'):]):
                rmb_temp = extract_rmb(line[line.index('本金'):])
                if startswith(rmb_temp, ['0', '.', ',']):
                    rmb_temp = ''
                if len(rmb_temp) > 0 and str(rmb_temp[0]).isdigit():
                    rmb_temp = '-{}'.format(rmb_temp)
            if rmb_temp != "" and not startswith(rmb_temp, ['0', '.', ',']):
                # confidence_ = str(get_confidence(self.path, box))
                rmb_temp = rmb_temp
                break
#        print(rmb_temp)

        lines = [unify_rec(self.result_ori[i]["words"])
                 for i in range(len(self.result_ori))]
#        print('-----------------------------------')
        for i in range(len(lines)):
            line = lines[i]
            if '本金' in line:
                if rmb_temp == '' and i+4 < len(lines):
                    texts = [text.replace('，', ',')
                             for text in lines[i:i+5]
                             if not startswith(text, ['0', '.', ','])]
                    for text in texts:
                        if set(text) <= set('1234567890,-.'):
                            rmb_temp = text
                            break
            if rmb_temp != "" and not rmb_temp.startswith('0'):
                if not rmb_temp.startswith('-'):
                    rmb_temp = '-{}'.format(rmb_temp)
                rmb_temp = rmb_temp
                break

        for i in range(len(lines)):
            line = lines[i]
            if '本金' in line:
                #                print('*********************************')
                if rmb_temp == '' and i-2 >= 0:
                    texts = [text.replace('，', ',')
                             for text in lines[i-2:i] if not text.startswith('0')]
#                    print(texts)
                    for text in texts:
                        if set(text) <= set('1234567890,-.'):
                            rmb_temp = text
                            break
            if rmb_temp != "" and not rmb_temp.startswith('0'):
                # confidence_ = str(get_confidence(self.path, box))
                if not rmb_temp.startswith('-'):
                    rmb_temp = '-{}'.format(rmb_temp)
                rmb_temp = rmb_temp
                break

        if ' ' in rmb_temp or rmb_temp.startswith(','):
            if len(rmb_temp[:rmb_temp.index(" ")]) == 1 or rmb_temp.startswith(','):
                rmb_temp = ""

        if rmb_temp.count('.') >= 2 and ',' not in rmb_temp:
            rmb_temp = ','.join(
                [rmb_temp[:rmb_temp.index('.')], rmb_temp[rmb_temp.index('.')+1:]])
        rmb["rmb"] = rmb_temp
        self.res.update(rmb)

    def card(self):
        card = {}
        lines = [unify_rec(self.result[i]["words"]) for i in range(len(self.result))]

        # boxs = [self.result[i]["position"] for i in range(len(self.result))]
        cards = extract_card(lines)
        for i in range(len(cards)):
            car = cards[i]

            # box = boxs_valid[i]
            #del check_bankcard
            # if check_bankcard(car) and str(car) != '':
            if str(car) != '':
                # confidence_ = str(get_confidence(self.path, box))
                card["card"] = car
                self.res.update(card)
                break

    def principal(self):
        lines = [self.result[i]["words"] for i in range(len(self.result))]

        principal = {}
        for i in range(len(lines)):
            # box = boxs[i]
            line = lines[i]
            line = line.replace('%', '')
            line = line.replace('布', '币')
            line = line.replace('市', '币')
            line = line.replace('而', '币')
            line = line.replace('大', '人')
            if '币种' in line:
                if '民币' in line[line.index('币种'):] or '001' in line[line.index('币种'):]:
                    principal["principal"] = "人民币"
                    self.res.update(principal)
                    break
                if '美元' in line[line.index('币种'):] or '014' in line[line.index('币种'):]:
                    principal["principal"] = "美元"
                    self.res.update(principal)
                    break
                if '欧元' in line[line.index('币种'):]:
                    principal["principal"] = "欧元"
                    self.res.update(principal)
                    break
                if '日元' in line[line.index('币种'):]:
                    principal["principal"] = "日元"
                    self.res.update(principal)
                    break
            if ('人民币' in line.replace(" ", "")) or ('001' in line.replace(" ", "")):
                principal["principal"] = "人民币"
                self.res.update(principal)
                break


# if __name__ == "__main__":
#     import os
#     from apphelper.post import getocr
#     result = getocr('captial-20-229_rotated.jpg', 0)
#     loss_temp = Captial(result)
#     for key in loss_temp.res.keys():
#         print('{}: {}'.format(key, loss_temp.res[key]))
