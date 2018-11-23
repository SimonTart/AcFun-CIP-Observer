# AcFun-CIP-Observer
AcFun Comment Instrumentality Project Observer（A站评论补全计划之观察者)

## 简介
用于抓取A站文章区和视频区下面的评论

## 使用
### 所需软件
- MySQL 5.7
- python3.6 及以上
### 使用
#### 配置
##### 通过环境变量配置
```
DB_HOST mysql host
DB_USER mysql 登录用户名
DB_PASSPORT mysql 登录密码
DB_NAME 数据库名
PYTHON_ENV 运行环境 # 线上环境，需要设置为production
```
##### 通过配置稳健配置
修改`config.py`中的`db`
#### 安装依赖
```bash
pip install < requirements.txt //安装依赖
```
#### 建表
```bash
alembic upgrade head //建表
```
#### 运行
在项目目录下创建logs文件之后运行
```bash
python  spider.py
```

## 相关资源
[AcFun-CIP-Observer](https://github.com/SimonTart/AcFun-CIP-Observer)

[AcFun-CIP-Extension](https://github.com/SimonTart/AcFun-CIP-Extension)

[AcFun-CIP-Official-Site](https://github.com/SimonTart/AcFun-CIP-Official-Site)
