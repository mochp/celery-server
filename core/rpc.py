import os
import requests
import json
import time
import base64
from conf import config


def yolo_detec(modelId=None, path=None):
    params = {'modelId': modelId, 'path': path}
    url = "http://localhost:8888/app"
    init, retry = 0, 5
    while True:
        res = requests.get(url, params=params)
        if res.ok:
            if res.text=="wrong id": # error modelId
                print("# error modelId")
                return []
            return eval(res.text)
        elif init > retry:
            return []
        else:
            print("try agin ...")
            init += 1
            time.sleep(3)


def write2word(path, detection=1):
    try:
        with open(path, 'rb') as f:
            image_data = base64.b64encode(f.read())
            image_data = str(image_data, encoding="utf-8")
        files = {'image': image_data, 'detection': detection}
        r = requests.post('http://localhost:8002/ocr3', json=json.dumps(files))
        res = r.json()["result"]
        result = [x["text"] for x in res]
    except:
        result = []
    return result


def ocr2word(path):
    try:
        data = {}
        img_base64 = base64.b64encode(open(path, 'rb').read())
        data['image_base64'] = img_base64
        data['app_key'] = config.APP_KEY
        data['app_secret'] = config.APP_SECRET
        response = requests.post(
            config.YIDAO_URL, data=data, headers=config.HEADERS)
        result = json.loads(response.content.decode('utf-8'))["result"]
    except:
        result = []
    return result
