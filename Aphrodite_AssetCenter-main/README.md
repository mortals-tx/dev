### 0x01 构架
2022.01.21 thinkzheng 优化精简架构，增加对内外网、IPV6资产的整合。

排期进度: 

Rest API文档: 

相关技术:
```
后端：
Flask
Flask 蓝图(Blueprint)
sqlalchemy

前端:
Vue
vue-router
Ant-Design && element-ui # 历史原因，默认是Ant-Design，后来用elementUI比较熟练就加进去用了，看喜欢用哪种就用哪种
```
目录说明
```
├── app
│   ├── app # API相关核心目录
        ├── api
        │   ├── manager # web管理台相关Api
        │   └── restful # 资产相关Api
        ├── libs
        └── models # 数据库相关
│   ├── config.py # 配置文件
│   ├── gunicorn.py # gunicorn文件
│   ├── logs # 日志文件目录
│   ├── manager.py # app启动文件
│   └── requirements.txt # Python依赖版本
├── conf
│   ├── docker
│   ├── nginx
│   └── supervisor
└── web # 前端
    ├── src # web源码
```

### 0x02 环境搭建
这里使用阿里云的Ubuntu 18.04为例


#### 依赖应用环境
按照开发环境的版本，依赖

```
mysql:8.0.19
```

可以用docker安装依赖，根据`conf/docker`文件下的配置，按照自身情况进行修改，比如原本有，就不用了

根据[docker官方文档](https://docs.docker.com/)或者[DaoCloud 软件中心](https://download.daocloud.io/)安装`docker`和`docker-compose`，如果获取镜像速度慢需要修改镜像地址

运行`docker-compose up`即可完成以上依赖

#### web环境
根据[nvm](https://github.com/nvm-sh/nvm)GitHub地址的指示安装nvm环境，并配置环境变量

```
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash   #github无法访问可以用代理proxychains 
$ source ~/.bashrc
$ nvm install 10.15.3  # 安装node
$ npm config set registry https://registry.npm.taobao.org  # 改淘宝镜像
$ cd ATField/web  # 切换到web环境
$ vim .env  # 添加env环境变量如下

NODE_ENV=production
VUE_APP_PREVIEW=false
VUE_APP_API_BASE_URL=/api

$ npm install  # 安装依赖(有时候安装某个模块报错一直装不上，可以先单独装完报错模块 npm install yorkie@2.0.0 --ignore-scripts , 再执行npm install)
$ npm run build  # 编译前端，完成后dist文件夹内容为我们所需
```

#### app环境
根据[pyenv](https://github.com/pyenv/pyenv)GitHub地址的指示安装pyenv环境，并配置环境变量

根据[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)GitHub地址的指示安装pyenv环境，并配置环境变量

```
# pyenv install的速度很慢，可以新建文件夹~/.pyenv/cache，从Python官网下载好对应版本的tar.xz文件，放在这个目录中，就不用下载可以直接安装
$ sudo apt-get install gcc build-essential zlib1g-dev libbz2-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev libffi-devel  # python安装容易缺少依赖
$ pyenv install 3.8.0  # 确定python版本
$ pyenv virtualenv 3.8.0 atfield-venv  # 创建虚拟环境
$ cd ATField/app  # 切换到app环境
$ pyenv activate atfield-venv  # 启动虚拟环境
$ pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com # 下载python依赖
$ vim .env  # 添加env环境变量如下

FLASK_SECRET_KEY=654321
FLASK_SQLALCHEMY_DATABASE_URI=mysql+cymysql://mysql:z8zce3Ct34uabtNo@127.0.0.1:3306/atfield

$ export FLASK_APP=manager.py  # 设置flask应用，参考 https://dormousehole.readthedocs.io/en/latest/quickstart.html#id5
$ flask deploy  # 创建数据库表等操作
```

#### supervisor
假设nginx稳定，依赖应用的稳定性有docker负责，supervisor负责我们自己编写的代码的稳定

```
$ sudo apt-get install supervisor  # 安装superivisor
$ cd ATField/conf/supervisor  # 切换到supervisor配置文件
$ cp ./* /etc/supervisor/conf.d  # 将配置拷贝到supervisor的默认配置位置
# 之后修改配置中路径、用户名等参数
$ supervisorctl
supervisor> start atfiled_app
supervisor> exit
```

#### nginx
根据[nginx官网](http://nginx.org/)提供的方式安装nginx

```
$ cd ATField/conf/nginx # 切换到nginx配置文件
$ cp ./* /etc/nginx/conf.d  # 将配置拷贝到nginx的默认配置位置
# 之后修改配置中路径、用户名等参数，注意nginx用户不能访问以下目录
$ nginx -t  # 检查配置
$ nginx -s reload  # 启动
```

#### 调试API
关掉gunicorn,单独启动Flask后再调试
```
sudo supervisorctl stop atfield_app
ps -axu |grep gunicorn |awk '{print $2}'|xargs kill -9
flask run   或 python manager.py
```

#### Web开发
路由:`web\src\config\router.config.js`
API: `web\src\api`  
视图文件: `web\src\views`
