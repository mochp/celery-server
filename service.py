import os
import time
import json
import yaml
import base64
import tornado.web
import tornado.ioloop
from tornado.escape import json_decode

from conf import config
from tasks import analysis
from tasks import analysis_without_down

import celery.states as states

from core.check import check_format_all
from core.check import check_obj_format
from core.check import check_obj_modelId

from core.obj import Output
from core.obj import ObjRespon
from core.obj import TotalObjRespon
from core.rpc import yolo_detec

from core.result import get_async_result

# def get_async_result(id):
#     res = app.AsyncResult(id)
#     if res.state == states.SUCCESS:
#         return str(res.result)
#     else:
#         return res.state


def check_input_json(jsons):
    # 检查json格式
    if not check_format_all(jsons):
        # 不通过直接返回错误信息
        return Output(status=config.STATUS_FAILTURE, info=config.INFO_WRONG_FORMAT).json

    result = []
    for i, obj in enumerate(jsons["data"]):
        # 检查obj格式
        if not check_obj_format(obj):
            output = Output(status=config.STATUS_FAILTURE,
                            info=config.INFO_WRONG_KEYS).json
            result.append(ObjRespon(obj=obj, output=output).json)
            continue
        # 检查modelid
        if not check_obj_modelId(obj):
            output = Output(status=config.STATUS_FAILTURE,
                            info=config.INFO_WRONG_MODELID).json
            result.append(ObjRespon(obj=obj, output=output).json)
            continue
        # 通过检查送进队列
        token = analysis.delay(obj).id
        # token = analysis.apply_async((obj),countdown=5).id
        output = Output(status=config.STATUS_SUCCESS,
                        info=config.INFO_RIGHT_FORMAT, token=token).json
        result.append(ObjRespon(obj=obj, output=output).json)

    return TotalObjRespon(ObjRespon=result).json


def respon_input_json(obj):
    if not check_obj_modelId(obj):
        output = Output(status=config.STATUS_FAILTURE,
                        info=config.INFO_WRONG_MODELID).json
        result = ObjRespon(obj=obj, output=output).json
    else:
        # 通过检查送进队列
        token = analysis_without_down.delay(obj).get(propagate=False)
        output = Output(status=config.STATUS_SUCCESS,
                        info=config.INFO_RIGHT_FORMAT, token=token).json
        result = ObjRespon(obj=obj, output=output).json

    return TotalObjRespon(ObjRespon=result).json


class AsyncHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        args = json_decode(self.request.body)
        print(args)
        respon = check_input_json(args)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()


class IdHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        ids = self.get_query_argument("id", "none")
        print("id:", ids)
        res = get_async_result(ids)
        respon = {"status": 1, "res": res}
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()


class FileUploadHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        args = eval(str(json_decode(self.request.body)))

        filename = str(time.time()).replace('.', '') + '.' + 'jpg'
        file_path = os.path.join(config.PATH_TMP, filename)
        print(file_path)

        # 保存图片
        with open(file_path, 'wb') as up:
            data = bytes(args['url'], encoding="utf8")
            up.write(base64.b64decode(data))

        args['url'] = file_path
        # args['modelId'] = int(args['modelId'])
        print(args)
        new = {'url': file_path,
               'modelId': int(args['modelId']),
               'type': args['type'], }
        print(new)
        respon = respon_input_json(new)
        print(respon)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()


class YoloHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        args = eval(str(json_decode(self.request.body)))
        # print(args["modelId"])
        filename = str(time.time()).replace('.', '') + '.' + 'jpg'
        file_path = os.path.join(config.PATH_TMP, filename)
        print(file_path)

        # 保存图片
        with open(file_path, 'wb') as up:
            data = bytes(args['base64'], encoding="utf8")
            up.write(base64.b64decode(data))

        # args['modelId'] = int(args['modelId'])
        res = yolo_detec(modelId=args["modelId"], path=file_path)
        new = {'status': "1",
               'res': str(res)}

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(new))
        self.finish()


app = tornado.web.Application([
    (r'/async', AsyncHandler),
    (r'/id', IdHandler),
    (r'/yolo', YoloHandler),
    (r'/server', FileUploadHandler)
])

if __name__ == '__main__':
    app.listen(8890)
    tornado.ioloop.IOLoop.instance().start()
