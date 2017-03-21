# SimpletourDevops
django+python+celery+saltstack+docker实现的运维管理后台

v1.0：完成资产信息录入及使用saltstack自动采集更新
      完成单机版docker主机的基本管理，日志实时刷新
##部署步骤
* 安装nginx
  ```
     yum install nginx -y
  ```

* 安装saltstack
  ```
     yum install salt-master -y
     yum install salt-minion -y
  ```
* 配置docker
  ```
     [root@localhost ~]# vim /etc/sysconfig/docker

     # /etc/sysconfig/docker

     # Modify these options if you want to change the way the docker daemon runs
     OPTIONS='--selinux-enabled -H 0.0.0.0:2375 -H unix:///var/run/docker.sock '
     DOCKER_CERT_PATH=/etc/docker
  ```
* 部署流程
以下为部署流程
 修改 settings.py中db连接
 ```
 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SimpletourDevops',
        'HOST': '192.168.2.232',
        'USER': 'root',
        'PORT': 3306,
        'PASSWORD': 'redhat',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
    }
}
 ```


 部署程序到/data

  ```
    [root@localhost ~]# mv /root/SimpletourDevops /data/
    [root@localhost ~]# cd /data/SimpletourDevops
    [root@localhost SimpletourDevops]#python manage.py  makemigrations
    [root@localhost SimpletourDevops]#python manage.py  migrate
  ```
 复制supervisor配置
   ```
     [root@localhost SimpletourDevops]# cp supervisord.conf  /etc/
     [root@localhost supervisord.d]# supervisord -c /etc/supervisord.conf     <--启动supervisor,如果启动用户非www，请自行修改
  ```
 修改配置文件
  ```
    在settings.py中添加STATIC_ROOT
    STATIC_ROOT = '/data/SimpletourDevops/static/suit'

  ```

  ```
  python manage.py collectstatic  <--生成静态文件
  ```
 配置nginx
 ```
  server {
      listen       80;
      server_name  localhost;
      access_log  /var/log/nginx/devops.simpletour.com.access.log  main;
      error_log  /var/log/nginx/devops.simpletour.com.error.log error;

      location / {
              include  uwsgi_params;
              uwsgi_pass  127.0.0.1:8098;
              uwsgi_read_timeout 600;
              uwsgi_connect_timeout 60;
              uwsgi_send_timeout 600;
              client_max_body_size 35m;
              proxy_http_version 1.1;
              proxy_set_header Upgrade $http_upgrade;
              proxy_set_header Connection "upgrade";
              uwsgi_ignore_client_abort on;
          }
          location ^~ /docker/getSocket{
              proxy_pass http://127.0.0.1:8099;
              proxy_http_version 1.1;
              proxy_set_header Upgrade $http_upgrade;
              proxy_set_header Connection "upgrade";
              proxy_set_header Host $host;
              uwsgi_ignore_client_abort on;
          }

          location /static {
              alias /data/SimpletourDevops/static/suit;
          }

  }
  
  

```
  



启动访问

### 首页及docker
      
![image](github.com/roddyofchina/SimpletourDevops/blob/master/images/login.png)
![image](github.com/roddyofchina/SimpletourDevops/blob/master/images/system_admin.png)
![image](github.com/roddyofchina/SimpletourDevops/blob/master/images/server.png)
![image](github.com/roddyofchina/SimpletourDevops/blob/master/images/docker.png)
![image](github.com/roddyofchina/SimpletourDevops/blob/master/images/docker_server.png)
![image](github.com/roddyofchina/SimpletourDevops/blob/master/images/log.png)
![image](github.com/roddyofchina/SimpletourDevops/blob/master/images/container_ssh.png)


### saltstack
![image](https://github.com/roddyofchina/SimpletourDevops/blob/master/images/keys.png)

![image](https://github.com/roddyofchina/SimpletourDevops/blob/master/images/job.png)

![image](https://github.com/roddyofchina/SimpletourDevops/blob/master/images/cmd.png)

![image](https://github.com/roddyofchina/SimpletourDevops/blob/master/images/soft.png)


### 后台

![image](https://github.com/roddyofchina/SimpletourDevops/blob/master/images/protal.png)
