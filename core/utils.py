#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 09:45:15 2019
@author: nlp
"""
import os
import time
import shutil
import urllib.request
from conf import config
from core.rpc import yolo_detec
from PIL import Image
from core.obj import Target, Obj2Json
from core.rpc import ocr2word
from core.image import rotate_cut_img
from pdf2image import convert_from_path
from core.application import helper

from core.application.apply import Apply
from core.application.captial import Captial
from core.application.verify import Verify
from core.application.idcard import Idcard, Idback, Police


def down(url, types):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    if (response.getcode() != 200):
        return False, []

    if types == "pdf":
        pdf_path = os.path.join(config.PATH_PDF_DOWN,
                                get_ext_name_from_path(url))
        with open(pdf_path, "wb") as f:
            f.write(response.read())
        pic_lists = cutpdf(pdf_path)

    else:
        pic_path = os.path.join(config.PATH_PIC_DOWN,
                                get_ext_name_from_path(url))
        with open(pic_path, "wb") as f:
            f.write(response.read())
        pic_lists = [pic_path]

    return True, pic_lists


def cutpdf(pdf_path):
    pdf_name = get_without_ext_name_from_path(pdf_path)
    cut_path = os.path.join(config.PATH_PDF_CUT, pdf_name)
    if os.path.exists(cut_path):
        shutil.rmtree(cut_path)
    os.mkdir(cut_path)

    convert_from_path(pdf_path, fmt="jpg", use_cropbox=True,
                      output_folder=cut_path)
    # 获取单页图片路径
    pic_lists = []
    for root, dirs, files in os.walk(cut_path):
        for f in files:
            old = os.path.join(root, f)
            new = os.path.join(root, pdf_name + "-" + f.split("-")[-1])
            os.rename(old, new)
            pic_lists.append(new)
    return pic_lists


def pic2object(modelId, pic_lists):
    pic_cut_objs_lists = []
    for i, path in enumerate(pic_lists):
        pic_cut_objs_lists.append(yolo_detec(modelId, path))
    return pic_cut_objs_lists


def convert2word(modelId, pic_lists, pic_cut_objs_lists):
    result = []
    length = len(pic_lists)
    assert len(pic_lists) == len(pic_cut_objs_lists)
    for i in range(len(pic_lists)):
        path = pic_lists[i]
        objs = pic_cut_objs_lists[i]
        if modelId == 600:
            rec = parse_lian(i, path, objs)
        else:
            rec = parse_usual(i, path, objs)

        result.append(rec)
    return result


def get_without_ext_name_from_path(url):
    return os.path.splitext(os.path.split(url)[-1])[0]


def get_ext_name_from_path(url):
    return os.path.split(url)[-1]


def parse_usual(page, path, objs):
    total = []
    for i, obj in enumerate(objs):
        target = Target(obj)
        gen_cut_path = cut_box_of_pic(path,target.box)
        words = ocr2word(gen_cut_path)
        str_list = [x["words"] for x in words]
        obj_json = Obj2Json(label=target.label,
                            page=page,
                            words=str_list,
                            box=target.box)
        total.append(obj_json.json)
    return total


def parse_lian(page, path, objs):
    total = []
    for i, obj in enumerate(objs):
        target = Target(obj)

        if target.label == "application":
            words = ocr2word(path)
            res = Apply(words).res
        elif target.label == "captia":
            words = ocr2word(path)
            res = Captial(words).res
        elif target.label == "idcard_head":
            gen_cut_path = cut_box_of_pic(path,target.box)
            words = ocr2word(gen_cut_path)
            res = Idcard(words).res
        elif target.label == "idcard_tail":
            gen_cut_path = cut_box_of_pic(path,target.box)
            words = ocr2word(gen_cut_path)
            res = Idback(words).res
        elif target.label == "police":
            gen_cut_path = cut_box_of_pic(path,target.box)
            words = ocr2word(gen_cut_path)
            res = Police(words).res
        elif target.label == "overdraw":
            words = ocr2word(path)
            res = Verify(words).res
        else:
            res = {}
            continue

        if res!={}:
            obj_json = Obj2Json(label=target.label,
                                words=res,
                                page=page,
                                box=target.box)
            total.append(obj_json.json)
    return total

def cut_box_of_pic(path,box):
    gen_cut_path = os.path.join(config.PATH_TMP, str(time.time()) + ".jpg")
    partImg, newbox = rotate_cut_img(Image.open(path),
                                        box,
                                        leftAdjustAlph=0.1,
                                        rightAdjustAlph=0.1)

    convert_cut_to_rgb(partImg, gen_cut_path)
    return gen_cut_path


def convert_cut_to_rgb(partImg, path):
    if len(partImg.split()) == 3:
        partImg.save(path)
    else:
        r, g, b, a = partImg.split()
        partImg = Image.merge("RGB", (r, g, b))
        partImg.save(path)


def clear_history_data():
    if os.path.exists(config.PATH_INIT):
        shutil.rmtree(config.PATH_INIT)
    os.makedirs(config.PATH_INIT)
    os.makedirs(config.PATH_PDF_CUT)
    os.makedirs(config.PATH_PDF_DOWN)
    os.makedirs(config.PATH_PIC_DOWN)
    os.makedirs(config.PATH_TMP)
