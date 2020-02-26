import re
from core.application.helper import extract_name


def extract_card(lines):
    cards = []
    # boxs_valid = []
    card_pattern1 = re.compile('[0-9]{18}')
    card_pattern2 = re.compile('[0-9]{15}')
    card_pattern3 = re.compile('[0-9]{10}')

    for i in range(len(lines)):
        line = ''.join(lines[i])
        if ''.join(card_pattern1.findall(line)):
            cards += card_pattern1.findall(line)
        if ''.join(card_pattern2.findall(line)):
            cards += card_pattern2.findall(line)
        if ''.join(card_pattern3.findall(line)):
            cards += card_pattern3.findall(line)
    return cards


class Apply:
    """
    申请表识别
    """

    def __init__(self, result):
        self.result = result
        self.N = len(self.result)
        self.res = {"applyTitle": "信用卡申请表", "name": "男", "No": "", "period": "", "sex": ""}
        try:
            self.full_name()
            self.idNO()
            self.sex()
        except Exception as e:
            print(e)

    def full_name(self):
        """
        身份证姓名
        """
        name = {}
        name_index = -1
        all_txt = "".join(self.result)
        if len(extract_name(all_txt)) > 0:
            name['name'] = extract_name(all_txt)[0]
            self.res.update(name)


    def sex(self):
        """
        性别女民族汉
        """

        sex = {}
        for i in range(self.N):
            txt = self.result[i]
            if '男' in txt:
                sex["sex"] = '男'
                self.res.update(sex)
                break
            elif '女' in txt:
                sex["sex"] = '女'
                self.res.update(sex)
                break

    def idNO(self):
        """
        身份证号码
        """
        No = {}
        all_txt = ""
        for i in range(len(self.result)):
            txt = self.result[i].replace(' ', '')
            txt = txt.replace('.', '').replace(':', '')
            txt = txt.replace('B', '8')
            all_txt+=txt
            # 身份证号码
            res = extract_card(all_txt)
            if len(res) > 10:
                No['No'] = res[0]
                self.res.update(No)


    def time(self):
        """
        有效期限
        """
        time = {}
        index = -1
        time_pattern = re.compile('[-.0-9长期]{2,}')

        for i in range(self.N):
            txt = self.result[i].replace('.', '').replace(
                ':', '').replace('B', '8').replace(';', '')

            for j, num in enumerate(txt):
                if num.isdigit() or '长期' in num:
                    index = j
                    break
            time["period"] = ''.join(time_pattern.findall(txt[index:]))
            if len(time["period"]) > 0:
                self.res.update(time)
                break


