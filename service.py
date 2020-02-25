from conf import config
from tasks import analysis

from core.check import check_format_all
from core.check import check_obj_format
from core.check import check_obj_modelId

from core.obj import Output
from core.obj import ObjRespon
from core.obj import TotalObjRespon

def check_input_json(jsons):
    #检查json格式
    if not check_format_all():
        #不通过直接返回错误信息
        return Output(status=config.STATUS_FAILTURE,info=config.INFO_WRONG_FORMAT).json

    result = []
    for i, obj in enumerate(jsons):
        #检查obj格式
        if not check_obj_format(obj):
            output = Output(status=config.STATUS_FAILTURE,
                            info=config.INFO_WRONG_KEYS).json
            result.append(ObjRespon(obj=obj, output=output))
            continue
        #检查modelid
        if not check_obj_modelId(obj):
            output = Output(status=config.STATUS_FAILTURE,
                            info=config.INFO_WRONG_MODELID).json
            result.append(ObjRespon(obj=obj, output=output))
            continue
        #通过检查送进队列
        token = analysis.s(obj)().id
        output = Output(status=config.STATUS_SUCCESS,
                        info=config.INFO_RIGHT_FORMAT, token=token).json
        result.append(ObjRespon(obj=obj, output=output))

    return TotalObjRespon(ObjRespon=result).json

