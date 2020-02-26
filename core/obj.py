
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
    def __init__(self, obj=None, output=None):
        self.obj = obj
        self.output = output
        self.json = self.obj2json()

    def obj2json(self):
        out = {"input": self.obj,
               "output": self.output}
        return out


class Obj2Json:
    def __init__(self, page = None,label=None, words=None, box=None):
        self.box = box
        self.page = int(page)+1
        self.label = label
        self.words = words
        self.json = self.obj2json()

    def obj2json(self):
        out = {"label": self.label,
               "words": self.words,
               "box": self.box}
        return out


class TotalObjRespon:
    def __init__(self, ObjRespon=None):
        self.obj = ObjRespon
        self.json = self.obj2json()

    def obj2json(self):
        out = {"res": self.obj,
               "info": "right format"}
        return out


class Target:
    def __init__(self, obj=None):
        self.obj = obj
        self.label, self.score = self.cut()
        self.point, self.box = self.location()

    def cut(self):
        label, score = str(self.obj[0]).split()
        score = round(float(score), 2)
        return label, score

    def location(self):
        x1, y1 = self.obj[1]
        x2, y2 = self.obj[2]
        point = {"xmin": x1,
                 "ymin": y1,
                 "xmax": x2,
                 "ymax": y2}
        box = [x1, y1, x2, y1, x2, y2, x1, y2]
        return point, box


class Over:
    def __init__(self, result=None):
        self.obj = result
        self.json = self.obj2json()

    def obj2json(self):
        out = {"res": self.obj,
               "info": "success"}
        return out
