# EVA-ACFUN

### 运行抓取脚本
##### 数据库的配置
数据库使用mysql, mysql的配置有两种方式
1. 通过配置环境变量mysql相关信息：
```
DB_HOST mysql host
DB_USER mysql 登录用户名
DB_PASSPORT mysql 登录密码
DB_NAME 数据库名
PYTHON_ENV 运行环境，需要设置为productionproduction。
```
2. 修改配置文件
修改`config.py`中的`db`

##### 安装依赖和建表
```bash
pip install < requirements.txt //安装依赖
alembic upgrade head //建表
```

##### 运行
```bash
python  index.py // 请使用python3
```

### 恢复A站评论的插件
插件是在EXTENSION目录下。下载和安装教程可以参见[官网](http://acfun.trisolaries.com:7070/)

如果是自己搭建的抓取服务器，需要自行修改插件里面的URL地址。