import time
from proj import app
from conf import config
from core.obj import Input
from core.utils import down



@app.task
def analysis(data):
    obj = Input(data)
    # step1 down
    status, pic_lists = down(obj.url, obj.type)
    # if status == 0:
    #     return {"info":"error url"}
    # # step2 yolo
    # pic_cut_objs_lists = utils.yolo(modelId, pic_lists)
    # # step3 ocr2word
    # res_lists = utils.ocr2word(pic_cut_objs_lists)
    return jsons
