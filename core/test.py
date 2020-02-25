from proj import celery_download, celery_cutpdf
from conf import config

import os
import json
import shutil

def respon(jsondata):
    res = check.checkdata(jsondata)
    if res["info"] == "right format":
        new = {"data":[],"info":"right format"}
        parse = res["data"]
        for i,obj in enumerate(parse):
            if obj["output"]["status"] == "success":
                token = chain(celery_download.s(obj) | celery_cutpdf.s())()
                obj["output"]["token"] = token.id
            new["data"].append(obj)
    return res


if os.path.exists(config.PATH_INIT):
    shutil.rmtree(config.PATH_INIT)
os.makedirs(config.PATH_INIT)
os.makedirs(config.PATH_PDF_CUT)
os.makedirs(config.PATH_PDF_DOWN)
os.makedirs(config.PATH_PIC_DOWN)



with open("conf/new.json","r") as f:
    jsondata = json.load(f)
res = respon(jsondata)
