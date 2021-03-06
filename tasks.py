import time
from proj import app
from conf import config
from core.obj import Input
from core.obj import Over
from core.utils import down_without
from core.utils import down
from core.utils import pic2object
from core.utils import convert2word


@app.task
def analysis(data):
    obj = Input(data)
    # step1 down
    status, pic_lists, page_lists = down(obj.url, obj.type)
    if not status:
        return {"info": "error url"}
    # step2 yolo
    pic_cut_objs_lists = pic2object(obj.modelId, pic_lists)

    # # step3 ocr2word
    res_lists = convert2word(obj.modelId, pic_lists,
                             page_lists, pic_cut_objs_lists)

    return Over(res_lists).json


@app.task
def analysis_without_down(data):
    obj = Input(data)
    # step1 down
    status, pic_lists, page_lists = down_without(obj.url, obj.type)
    if not status:
        return {"info": "error url"}
    # step2 yolo
    pic_cut_objs_lists = pic2object(obj.modelId, pic_lists)

    # # step3 ocr2word
    res_lists = convert2word(obj.modelId, pic_lists,
                             page_lists, pic_cut_objs_lists)

    return Over(res_lists).json
