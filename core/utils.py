#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 09:45:15 2019

@author: nlp
"""
import os
import shutil
from pdf2image import convert_from_path

def cutpdf(obj,cutpath):


    try:

        if obj['type']=='jpg':
            filePath = obj.get('filePath')
            obj.update(filePathList=[{"path":filePath}])
            return obj 
        else:
            pdfpath = obj.get('filePath')
            file_without_extend = os.path.splitext(os.path.split(pdfpath)[-1])[0]
            outpath = os.path.join(cutpath,file_without_extend)
            if os.path.exists(outpath):
                shutil.rmtree(outpath)
            os.mkdir(outpath)
            convert_from_path(pdfpath,fmt="jpg",use_cropbox=True, output_folder=outpath)
            #获取单页图片路径
            filePathList = []
            for root, dirs, files in os.walk(outpath):
                for f in files:
                    old = os.path.join(root, f)
                    new = os.path.join(root,file_without_extend +"-" + f.split("-")[-1])
                    os.rename(old, new)
                    filePathList.append({"path":new})
            # obj['filePathList'] = filePathList
            obj.update(filePathList=filePathList)
            return obj 
    except Exception as e:
        obj['status'] = 'failture'
        obj['info'] = e
        return obj


if __name__ == "__main__":

    out = {'status': 'success',
            'info': '',
            'type': 'pdf',
            'modelId': 600,
            'filePath': '/opt/automlserver/docs/downpdf/1579230136407715.pdf',
            'url': 'http://39.106.51.188:8010/download/pdf_sifang/15791453438465877.pdf'}
    
    print(cutpdf(out,"/opt/automlserver/docs/cutpdf"))
