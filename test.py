import time
from proj import app
from conf import config
from core.obj import Input
from core.obj import Over

from core.utils import down
from core.utils import pic2object
from core.utils import convert2word

data =          {
            "type": "jpg",
            "modelId": 600,
            "url": "http://39.106.51.188:8010/download/pic_lian/003.jpg"
        }
obj = Input(data)
# step1 down
status, pic_lists = down(obj.url, obj.type)

# step2 yolo
pic_cut_objs_lists = pic2object(obj.modelId, pic_lists)
# # step3 ocr2word
res_lists = convert2word(obj.modelId, pic_lists, pic_cut_objs_lists)

print(Over(res_lists).json)
