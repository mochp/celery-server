# coding: utf8

import urllib.request
import json
import os


def download(obj, jpgpath, pdfpath):
    """    
    下载并且拆分pdf
    """
    res = {'status': 'success',
           'info': '',
           'type': obj["input"]["type"],
           'modelId': obj["input"]["modelId"],
           'filePath:': ''}

    img_url = obj["input"]["url"]
    img_name = os.path.split(img_url)[-1]
    if obj["input"]["type"] == "jpg":
        filename = os.path.join(jpgpath, img_name)
        res['filePath'] = filename
    else:
        filename = os.path.join(pdfpath, img_name)
        res['filePath'] = filename
    try:
        request = urllib.request.Request(img_url)
        response = urllib.request.urlopen(request)
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                f.write(response.read())  # 将内容写入图片
    except Exception as e:
        res['status'] = "failed"
        res['info'] = e
    return res


if __name__ == '__main__':
    test = {'input': {'type': 'jpg', 'modelId': 600, 'url': 'http://39.106.51.188:8010/download/pic_sifang/1579248027928056.jpg'},
            'output': {'status': 'success', 'info': '', 'token': '51a3afad-6135-4923-a563-6fe57d493ea8'}}

    # out = {'status': 'success',
    #         'info': '',
    #         'type': 'jpg',
    #         'modelId': 600,
    #         'filePath:': '1579248027928056.jpg',
    #         'url': 'http://39.106.51.188:8010/download/pic_sifang/1579248027928056.jpg'}

    # with open("../docs/downloadtask/res.json", "r") as f:
    #     obj = json.load(f)
    #     print(obj["data"][0])
    # # 下载要的图片
    # # test = {
    # #     "type": "jpg",
    # #     "modelId": 600,
    # #     "url": "http://39.106.51.188:8010/download/pic_sifang/1579248027928056.jpg"}
    # res = download(test,"./","./")
    # print(res)
