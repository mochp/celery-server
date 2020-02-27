from proj import app
import celery.states as states

# res = app.AsyncResult("e06884ed-5bd5-4e27-9250-80815e718a5b")

def get_async_result(id):
    res = app.AsyncResult(id)
    if res.state == states.SUCCESS:
        return str(res.result)
    else:
        return res.state

