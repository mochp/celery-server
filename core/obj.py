

class Inputs:
    def __init__(self, jsons):
        self.url = jsons["url"]
        self.type = jsons["type"]
        self.modelId = jsons["modelId"]


class Output:
    def __init__(self, status=None, info=None, token=None):
        self.status = status
        self.info = info
        self.token = token
        self.json = self.obj2json()

    def obj2json(self):
        out = {"status": self.status,
               "info": self.info,
               "token": self.token}
        return out

class ObjRespon:
    def __init__(self,obj=obj,output=output):
        self.obj = obj
        self.output = output
        self.json = self.obj2json()

    def obj2json(self):
        out = {"input": self.obj,
               "output": self.output}
        return out

class TotalObjRespon:
    def __init__(self,ObjRespon=ObjRespon):
        self.obj = ObjRespon
        self.json = self.obj2json()

    def obj2json(self):
        out = {"res": self.obj,
               "info": "right format"}
        return out

