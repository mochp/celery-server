import requests
import json
import time


def yolo_detec(modelId=None,path=None):
    params = {'modelId': modelId,'path': path}
    url = "http://localhost:8888/app"
    init,retry = 0,10
    while True:
        res = requests.get(url,params=params)
        if res.ok:
            return eval(res.text)
        elif init>retry:
            assert retry < init
            return []
        else:
            print("try agin ...")
            init+=1
            time.sleep(2)
    


