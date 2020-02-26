"""
身份证
"""
import re
from core.image import union_rbox
from core.application.helper import check_bankcard, check_idcard
from core.application.helper import str_count, get_conf
from core.application.helper import extract_name
from core.application.helper import idcard2sex

provinces = ['河北', '山西', '内蒙', '黑龙', '吉林', '辽宁', '陕西',
             '青海', '新疆', '宁夏', '山东', '河南', '江苏', '甘肃',
             '浙江', '安徽', '江西', '福建', '台湾', '湖北', '西藏',
             '湖南', '广东', '广西', '海南', '四川', '云南', '贵州',
             '香港', '澳门']
nations = ["汉族", "满族", "蒙古族", "回族", "藏族", "维吾尔族", "苗族", "彝族",
           "壮族", "布依族", "侗族", "瑶族", "白族", "土家族", "哈尼族",
           "哈萨克族", "傣族", "黎族", "傈僳族", "佤族", "畲族", "高山族", "拉祜族",
           "水族", "东乡族", "纳西族", "景颇族", "柯尔克孜族", "土族", "达斡尔族",
           "仫佬族", "羌族", "布朗族", "撒拉族", "毛南族", "仡佬族", "锡伯族",
           "普米族", "朝鲜族", "塔吉克族", "怒族", "乌孜别克族", "俄罗斯族",
           "鄂温克族", "德昂族", "保安族", "裕固族", "京族", "塔塔尔族",
           "独龙族", "鄂伦春族", "赫哲族", "门巴族", "珞巴族", "基诺族", "阿昌族"]


def is_provinces(str_):
    for province in provinces:
        if province in str_:
            return True
    return False


def is_nation(str_):
    for nation in nations:
        if nation in str_:
            return True
    return False


def extract_provinces(str_):
    for province in provinces:
        if province in str_:
            return province
    return False


class Idcard():
    """
    身份证结构化识别正面
    """

    def __init__(self, result):
        self.init_result = result
        result = union_rbox(result, 1)

        self.resulting = result

        self.result = union_rbox(result, 2)
        self.check_status = 0
        self.N = len(self.result)
        self.res = {"name": "", "sex": "", "No": ""}
        try:
            self.full_name()
        except Exception as e:
            print(e)
        try:
            self.idNO()
        except Exception as e:
            print(e)
        try:
            self.sex()
        except Exception as e:
            print(e)

    def full_name(self):
        """
        身份证姓名
        """
        name = {}
        name_index = -1

        for i in range(self.N):
            txt = self.result[i]["words"].replace(' ', '')
            txt = txt.replace("住名", "姓名")
            if (txt.find("姓") == 0) and ("名" not in txt):
                txt.replace("姓", "姓名")
            if txt.find("名") == 0:
                txt.replace("名", "姓名")
            if "姓名" in txt:
                name_index = i

        if name_index != -1:
            txt = self.result[name_index]["words"].replace(' ', '')
            res = re.findall("姓名[\u4e00-\u9fa5]{1,4}", txt)

            if len(res) > 0:
                if len(res) == 6:  # 这个有时候是四个字的名字，我就加了一个判断
                    name['name'] = res[0].replace('姓名', '')[-4:]
                else:
                    name['name'] = res[0].replace('姓名', '')[-3:]

            elif len(txt) == 5:
                name['name'] = txt[-3:]

            elif txt.find("名") and txt.find("名") < 2:
                name['name'] = txt[txt.find("名") + 1:][-3:]

            else:
                name['name'] = txt[-3:]

            # 3
            if name['name'] != "":
                name['name'] = name['name']
                self.res.update(name)

        elif self.N == 6 and len(name) == 0 and (len(self.result[0]["words"].replace(' ', '')) == 2):
            txt = self.result[0]["words"].replace(' ', '')
            name['name'] = txt[-4:]
            name['name'] = name['name']
            self.res.update(name)

        else:
            total = ""
            for i in range(self.N):
                txt = self.resulting[i]["words"].replace(' ', ',')
                if (("男" in txt) or ("女" in txt) or ("性别" in txt)) and (("族" in txt) or is_nation(txt)):
                    break

                if is_provinces(txt):
                    break

                total += txt + ","
            print(total)
            name_list = extract_name(total)

            if len(name_list) > 0:
                name["name"] = name_list[0]
                self.res.update(name)

    def sex(self):
        """
        性别女民族汉
        """

        sex = {}
        for i in range(self.N):
            txt = self.result[i]["words"].replace(' ', '')
            txt = txt.replace('.', '').replace(':', '')
            if (("男" in txt) or ("女" in txt)) and (("族" in txt) or is_nation(txt)):
                if '男' in txt:
                    sex["sex"] = '男'
                    self.res.update(sex)
                    break
                elif '女' in txt:
                    sex["sex"] = '女'
                    self.res.update(sex)
                    break
        middle = sex.get('sex')
        if sex.get('sex') == None:
            all_text = ''.join([self.result[i]["words"] for i in range(len(self.result))])
            if self.res["No"] != '':
                if '男' in all_text and idcard2sex(self.res["No"]) == '男':
                    sex['sex'] = '男'
                if '女' in all_text and idcard2sex(self.res["No"]) == '女':
                    sex['sex'] = '女'
                self.res.update(sex)

    def nation(self):
        """
        性别女民族汉
        """
        nation = {}

        for i in range(self.N):
            txt = self.result[i]["words"].replace(' ', '')
            txt = txt.replace('.', '').replace(':', '')
            if (("男" in txt) or ("女" in txt) or ("性别" in txt) or ("族" in txt)) and is_nation(txt):
                for zu in nations:
                    if zu in txt:
                        nation["nation"] = zu
                        self.res.update(nation)
                        break
            elif is_nation(txt) and len(txt) == 1:
                for zu in nations:
                    if zu in txt:
                        nation["nation"] = zu
                        self.res.update(nation)
                        break

    def idNO(self):
        """
        身份证号码
        """
        No = {}
        for i in range(len(self.init_result)):
            txt = self.init_result[i]["words"].replace(' ', '')
            txt = txt.replace('.', '').replace(':', '')
            txt = txt.replace('B', '8')
            # 身份证号码
            res = re.findall('\d*[X|x]', txt)
            res += re.findall('\d{15,18}', txt)
            if len(res) > 0 and check_idcard(res[0]):
                No['No'] = res[0]
                self.check_status = 1
                self.res.update(No)
                break
            if len(res) > 0 and (not check_idcard(res[0])):
                No['No'] = res[0]

                self.res.update(No)
                break

    def address(self):
        """
        身份证地址
        """
        adds = {}
        add = ""
        start_index = -1
        end_index = -1

        for i in range(self.N):
            txt = self.result[i]["words"].replace(' ', '')
            if "省" in txt or "市" in txt or is_provinces(txt):
                start_index = i
                break

        for i in range(self.N):
            txt = self.result[i]["words"].replace(' ', '')
            if str_count(txt)["DG"] > 6 and i >= start_index:
                end_index = max(start_index, i)
                break
        # end_index 可能解析不到
        if end_index == -1:
            end_index = self.N

        print(start_index, end_index)
        if start_index != -1:
            for index in range(start_index, min(end_index, self.N)):
                add += self.result[index]["words"].replace(
                    ' ', '').replace('.', '').replace(':', '')

            if "住址" in add:
                add = add.replace("住址", "")
            else:
                if add.find("省") < 5 and add.find("省"):
                    index0 = add.find("省")
                    if "龙" in add[:index0]:
                        add = add[max(0, index0 - 3):]
                    else:
                        add = add[max(0, index0 - 2):]
                elif add.find("市") < 5 and add.find("市"):
                    index1 = add.find("市")
                    add = add[max(0, index1 - 2):]

                elif extract_provinces(add):
                    add = add[add.index(extract_provinces(add)):]
                else:
                    add = add

            if add != '':
                adds["adds"] = add
            self.res.update(adds)


class Idback:
    """
    身份证反面
    """

    def __init__(self, result):
        self.result = union_rbox(result, 2)
        #        self.result = self.predeal(self.result)
        self.N = len(self.result)
        self.res = {"sign": "", "time": ""}
        self.time_app = ""
        try:
            self.sign()
        except Exception as e:
            print(e)
        try:
            self.time()
        except Exception as e:
            print(e)

    #        self.res["confidence"] = ""
    #        self.confidence()

    def predeal(self, result):
        new = []
        for res in result:
            res["position"] = (res['cx'], res['cy'],
                               res['w'] + res['cx'], res['cy'] + res['h'])
            new.append(res)
        return new

    def sign(self):
        """
        机关
        """
        sign = {}
        #        if self.N in range(4,7):
        for i in range(self.N):
            txt = self.result[i]["words"]
            txt = re.sub("[^\u4e00-\u9fa5]", '', txt)
            txt = txt.replace("执关", "机关")
            txt = txt.replace("类关", "机关")
            txt = txt.replace('分司', "分局")
            txt = txt.replace('余局', "分局")
            txt = txt.replace("巩关", "机关")
            if "机关" in txt or "分局" in txt or "公安局" in txt:
                txt = txt.replace('.', '').replace(':', '')
                #                box =  self.result[i]["position"]
                index = txt.find("机关")
                sign_temp = txt[index + 2:]
                sign["sign"] = sign_temp
                self.res.update(sign)
                break
            if "发机" in txt or "分局" in txt or "公安局" in txt:
                txt = txt.replace('.', '').replace(':', '')
                #                box =  self.result[i]["position"]
                index = txt.find("发机")
                sign_temp = txt[index + 2:]
                sign["sign"] = sign_temp
                self.res.update(sign)
                break

    def time(self):
        """
        有效期限
        """
        time = {}
        index = -1
        time_pattern = re.compile('[-.0-9长期]{2,}')
        if self.N == 4:
            txt = self.result[3]["words"].replace(' ', '')

            txt = txt.replace('.', '').replace(
                ':', '').replace('B', '8').replace(';', '')
            for i, num in enumerate(txt):
                if num.isdigit() or '长期' in num:
                    index = i
                    break
            if index >= 0:
                time["time"] = ''.join(time_pattern.findall(txt[index:]))
                self.res.update(time)

        else:
            for i in range(self.N):
                txt = self.result[i]["words"].replace('.', '').replace(
                    ':', '').replace('B', '8').replace(';', '')
                # box =  self.result[i]["position"]
                for j, num in enumerate(txt):
                    if num.isdigit() or '长期' in num:
                        index = j
                        break
                if "有效" in txt or "期" in txt:
                    time["time"] = ''.join(time_pattern.findall(txt[index:]))
                    self.res.update(time)

        self.res['time'] = re.sub('[^0-9长期]', '', self.res['time'])
        if '长期' in self.res['time']:
            self.time_app = '长期'
            if len(self.res['time']) == 10:
                self.res['time'] = '-'.join(
                    [self.res['time'][:8], '长期'])
        elif len(self.res['time']) == 16:
            self.time_app = self.res['time'][8:]
            self.res['time'] = '-'.join(
                [self.res['time'][:8], self.res['time'][8:]])
        else:
            self.time_app = ''


class Police:
    """
    公安核查
    """

    def __init__(self, result):
        self.result = union_rbox(result, 0.5)
        #        self.result = self.predeal(self.result)
        self.N = len(self.result)
        self.check_status = 0
        self.res = {}
        self.res["name"] = ""
        self.res["No"] = ""
        try:
            self.name()
        except Exception as e:
            print(e)
        try:
            self.idNO()
        except Exception as e:
            print(e)

    #        self.res["confidence"] = ""
    #        self.confidence()

    def predeal(self, result):
        new = []
        for res in result:
            res["position"] = (res['cx'], res['cy'],
                               res['w'] + res['cx'], res['cy'] + res['h'])
            new.append(res)
        return new

    def name(self):
        name = {}
        name["name"] = ""
        for i in range(self.N):
            txt = self.result[i]["words"].replace(' ', '')
            if "姓名" in txt:
                name_list = extract_name(txt)
                if len(name_list) > 0:
                    name["name"] = name_list[0]
                    self.res.update(name)
                    break
        print(name)
        if name["name"] == "":
            for i in range(self.N):
                txt = self.result[i]["words"].replace(' ', '')
                name_list = extract_name(txt)
                if len(name_list) > 0:
                    name["name"] = name_list[0]
                    self.res.update(name)
                    break

    def idNO(self):
        No = {}
        for i in range(self.N):
            txt = self.result[i]["words"]
            txt = txt.replace('.', '').replace(':', '')
            txt = txt.replace('B', '8')
            # 身份证号码
            res = re.findall('\d*[X|x]', txt)
            res += re.findall('\d{15,18}', txt)

            if len(res) > 0 and check_idcard(res[0]):
                No['No'] = res[0]
                self.check_status = 1
                self.res.update(No)
                break
            if len(res) > 0 and (not check_idcard(res[0])):
                No['No'] = res[0]
                self.res.update(No)
                break


# if __name__ == "__main__":
#     #    pass
#     from apphelper.post import getocr

#     result = getocr('idhead-02-018.jpg')
#     loss_temp = Idcard(result)
#     #    result_new = union_rbox(result,0)
#     for key in loss_temp.res.keys():
#         print('{}: {}'.format(key, loss_temp.res[key]))
