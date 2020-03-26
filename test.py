from service import check_input_json
from core.result import get_async_result
import json
import sys
from core.sql import getTypeList


if __name__ == '__main__':
    if sys.argv[1] == "test":
        with open("conf/test.json") as f:
            res = json.load(f)     
        token = check_input_json(res)
        print(token)

    elif sys.argv[1] == "id":
        res = get_async_result(sys.argv[2])
        print(res)

    elif sys.argv[1] == "model":
        res = getTypeList(sys.argv[2])
        print(res)