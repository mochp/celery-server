from tqdm import tqdm
from scipy import misc, ndimage
import random
import math
import cv2
import os
import shutil
import pyltp
import numpy as np

LTP_DATA_DIR = r'/home/lcong/automl/models/ltp_data_v3.4.0'
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
segmentor = pyltp.Segmentor()
segmentor.load(cws_model_path)
postagger = pyltp.Postagger()
postagger.load(pos_model_path)
recognizer = pyltp.NamedEntityRecognizer()
recognizer.load(ner_model_path)


def extract_name(str_):
    words = segmentor.segment(str_)
    postages = postagger.postag(words)
    netags = recognizer.recognize(words, postages)
    ners = np.array(words)[np.array(netags) == 'S-Nh']
    return list(ners)


def get_conf(result, i):
    new = 0.98
    try:
        new = round(result[i]["score"], 2)
    except:
        pass
    return new


def str_count(string):
    '''找出字符串中的中英文、空格、数字、标点符号个数'''

    count = {}
    count_en = count_dg = count_sp = count_zh = count_pu = 0
    try:
        for s in string:
            # 英文
            if s > 'a' and s < 'z' or s > 'A' and s < 'Z':
                count_en += 1
            # 数字
            elif s.isdigit():
                count_dg += 1
            # 空格
            elif s.isspace():
                count_sp += 1
            # 中文
            elif s.isalpha():
                count_zh += 1
            # 特殊字符
            else:
                count_pu += 1
    except:
        pass

    count["EN"] = count_en
    count["DG"] = count_dg
    count["SP"] = count_sp
    count["ZH"] = count_zh
    count["PU"] = count_pu
    return count


def create(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    os.mkdir(os.path.join(path, "application"))
    os.mkdir(os.path.join(path, "idcard"))
    os.mkdir(os.path.join(path, "captial"))
    os.mkdir(os.path.join(path, "overdraw"))
    os.mkdir(os.path.join(path, "loss"))
    os.mkdir(os.path.join(path, "other"))


B = [['chart 1.00', (123, 123), (433, 1348)],
     ['seal_name 0.98', (922, 198), (956, 263)],
     ['seal_name 1.00', (884, 87), (967, 174)]]


def get_label(B):
    labels = []
    for loc in B:
        label = loc[0].split(" ")[0]
        labels.append(label)

    if "application" in labels:
        return "application"
    elif ("idcard_tail" in labels) or ("idcard_head" in labels) or ("police" in labels):
        return "idcard"
    elif "captia" in labels:
        return "captial"
    elif "overdraw" in labels:
        return "overdraw"
    elif "loss" in labels:
        return "loss"
    else:
        return "other"
    return "other"


def cut_index(labels):
    index = []
    init = 0
    number = 0
    for i, label in enumerate(labels):
        if label == "application" and (number > 2 or init == 0):
            index.append(i)
            init = 1
            number = 0
        number += 1
    return index


def idcard2sex(number):
    number = str(number)
    if "score" in number:
        number = number.split(" ")[0]
    NoSex = ""
    if len(number) == 18 and ((str_count(number)["DG"] == len(number))
                              or 'x' in number or 'X' in number):
        if int(number[-2]) % 2 == 1:
            NoSex = "男"
        else:
            NoSex = "女"
    return NoSex


def check_bankcard(card_num):
    if str_count(card_num)["DG"] < len(card_num) or len(card_num) != 16:
        return False
    s = 0
    card_num_length = len(card_num)
    for _ in range(1, card_num_length + 1):
        t = int(card_num[card_num_length - _])
        if _ % 2 == 0:
            t *= 2
            s += t if t < 10 else t % 10 + t // 10
        else:
            s += t
    return s % 10 == 0


def check_idcard(id_number):
    id_number = id_number.replace('X', 'x')
    if str_count(id_number)["DG"] < len(id_number)-1 or len(id_number) != 18:
        return False

    def id_number_validate(id_number):

        if type(id_number) in [str, list, tuple]:
            if len(id_number) == 18:
                return True
        raise Exception('Wrong argument')

    if id_number_validate(id_number):
        check = id_number[17]
        if type(id_number) == str:
            seq = map(int, id_number)
        elif type(id_number) in [list, tuple]:
            seq = id_number

        t = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        s = sum(map(lambda x: x[0] * x[1], zip(t, map(int, seq))))
        b = s % 11
        bd = {
            0: '1', 1: '0', 2: 'x', 3: '9', 4: '8', 5: '7',
            6: '6', 7: '5', 8: '4', 9: '3', 10: '2'
        }

        if bd[b] == check:
            return True
        else:
            return False


def rotate_image(filepath):
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # 霍夫变换
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    try:
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            if x1 == x2 or y1 == y2:
                misc.imsave(filepath.replace('.', '_rotated.'), img)
                continue
            t = float(y2-y1)/(x2-x1)
            rotate_angle = math.degrees(math.atan(t))
            if int(abs(t)) == 1:
                misc.imsave(filepath.replace('.', '_rotated.'), img)
                continue
            if rotate_angle > 45:
                rotate_angle = -90 + rotate_angle
            elif rotate_angle < -45:
                rotate_angle = 90 + rotate_angle
            rotate_img = ndimage.rotate(img, rotate_angle)
            misc.imsave(filepath.replace('.', '_rotated.'), rotate_img)
    except:
        misc.imsave(filepath.replace('.', '_rotated.'), img)
        pass


class Person(object):
    def __init__(self,pathList,pageList,):
        self.NO = ""
        self.Adds = ""
        self.Apply = ""
        self.Sex = ""
        self.Loss = ""
        self.Name = ""
        self.Nation = ""
        self.Overdraw = ""
        self.Sign = ""
