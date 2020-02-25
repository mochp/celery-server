# from proj import analysis
from conf import config
from core import check
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
                token = analysis.s(obj)()
                obj["output"]["token"] = token.id
            new["data"].append(obj)
    return res




with open("conf/new.json","r") as f:
    jsondata = json.load(f)

js = json.loads(jsondata)



