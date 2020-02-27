# celery-server

### 1、项目放到 /opt 目录下

### 2、指令 

+ 简单启动 

    `celery -A tasks worker -l info`

+ 多线程后台启动

    `celery multi start w1 -A proj -l info --pidfile=./logs/run/%n.pid --logfile=./logs/log/%n%I.log`

+ 暴力关闭

    `celery multi stop w1 -A proj -l info`

+ 等待任务结束关闭

    `celery multi stopwait w1 -A proj -l info`

### 3、清除队列

+ `sudo rabbitmqctl list_queues`
+ `sudo rabbitmqctl stop_app`
+ `sudo rabbitmqctl reset`
+ `sudo rabbitmqctl start_app`

### 4、设置账户
+ `sudo rabbitmqctl add_user apabi 10NsS2mM`
+ `sudo rabbitmqctl add_vhost /`
+ `sudo rabbitmqctl set_permissions -p / apabi ".*" ".*" ".*"`

### 5、pdf2image安装
+ `pip install pdf2image`