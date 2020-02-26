#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 09:45:15 2019
@author: nlp
"""
import os
import shutil
import urllib.request
from conf import config
from core.rpc import yolo_detec
from pdf2image import convert_from_path


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


def convert2word(modelId,pic_lists, pic_cut_objs_lists):
    result = []
    length = len(pic_lists)
    assert len(pic_lists) == len(pic_cut_objs_lists)
    for i in range(len(pic_lists)):
        path = pic_lists[i]
        objs = pic_cut_objs_lists[i]
        if modelId == 600:
            rec = analysis_lian(path,objs)
        else:
            rec = analysis_usual(path,objs)

        result.append(rec)
    return result


def get_without_ext_name_from_path(url):
    return os.path.splitext(os.path.split(url)[-1])[0]


def get_ext_name_from_path(url):
    return os.path.split(url)[-1]


def clear_history_data():
    if os.path.exists(config.PATH_INIT):
        shutil.rmtree(config.PATH_INIT)
    os.makedirs(config.PATH_INIT)
    os.makedirs(config.PATH_PDF_CUT)
    os.makedirs(config.PATH_PDF_DOWN)
    os.makedirs(config.PATH_PIC_DOWN)
    os.makedirs(config.PATH_TMP)
