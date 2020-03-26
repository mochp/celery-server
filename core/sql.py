import pymysql


class Param:
    def __init__(self, filePath, labelList):
        self.filePath = filePath
        self.labelList = labelList


def getMenuFeature(modlId):
    conn = pymysql.connect(host='172.18.89.119', port=3306, user='root',
                           passwd='10NsS2mM!@#$', db='automl', charset='utf8')
    cur = conn.cursor()
    cur.execute(
        "select model_file_path from model_info where model_id ='%s';" % (
            modlId))
    cur.rowcount
    modelPath = cur.fetchall()
    cur.execute(
        "select label_value from model_label where model_id = '%s'  order by id desc;" % (
            modlId))
    labelList = list(cur.fetchall())
    cur.close()
    param = Param(modelPath[0], labelList)
    path = param.filePath[0]

    total_lists = [x[0] for x in param.labelList]
    label = ','.join(total_lists)
    return path, label


def getTypeList(modelId):
    if int(modelId) == 600:
        return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    if int(modelId) == 500:
        return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    conn = pymysql.connect(host='172.18.89.119', port=3306, user='root',
                           passwd='10NsS2mM!@#$', db='automl', charset='utf8')

    cur = conn.cursor()
    cur.execute(
        "select label_type from model_label where model_id = '%s';" % (modelId))
    labelTypeList = list(cur.fetchall())
    cur.close()
    typeList = [x[0] for x in labelTypeList]
    return typeList


if __name__ == "__main__":
    typeList = getMenuFeature(767)
    print(typeList)
