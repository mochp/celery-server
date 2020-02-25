import os
import sys
import time
from core.utils import clear_history_data


def command(cmd):
    if cmd == "clear":
        clear_history_data()
    
    elif cmd == "start":
        os.system("nohup celery -A tasks worker &")
        os.system("nohup celery -A tasks flower &")

    elif cmd == "stop":
        os.system("ps -ef | grep 'celery' |grep -v 'grep'|awk '{print $2}' | xargs kill -9")

    elif cmd == "restart":
        os.system("ps -ef | grep 'celery' |grep -v 'grep'|awk '{print $2}' | xargs kill -9")
        time.sleep(1)
        os.system("nohup celery -A tasks worker &")
        os.system("nohup celery -A tasks flower &")
  
    else:
        print("no such command!")


if __name__ == '__main__':
    command(sys.argv[1])