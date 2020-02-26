
class Input:
    def __init__(self, json=None):
        self.url = json["url"]
        self.type = json["type"]
        self.modelId = json["modelId"]



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
    def __init__(self,obj=None,output=None):
        self.obj = obj
        self.output = output
        self.json = self.obj2json()

    def obj2json(self):
        out = {"input": self.obj,
               "output": self.output}
        return out

class TotalObjRespon:
    def __init__(self,ObjRespon=None):
        self.obj = ObjRespon
        self.json = self.obj2json()

    def obj2json(self):
        out = {"res": self.obj,
               "info": "right format"}
        return out


class Over:
    def __init__(self,result=None):
        self.obj = result
        self.json = self.obj2json()

    def obj2json(self):
        out = {"res": self.obj,
               "info": "success"}
        return out