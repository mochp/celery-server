import time
from proj import app
from core import utils
from conf import config


@app.task
def analysis(jsons):
    url = jsons["input"]["url"]
    types = jsons["input"]["type"]
    modelId = jsons["input"]["url"]
    # step1 down
    status, pic_lists = utils.down(url, types)
    if status == 0:
        return {"info":"error url"}
    # step2 yolo
    pic_cut_objs_lists = utils.yolo(modelId, pic_lists)
    # step3 ocr2word
    res_lists = utils.ocr2word(pic_cut_objs_lists)
    return res_lists
