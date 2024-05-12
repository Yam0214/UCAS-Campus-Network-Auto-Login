# UCAS Campus Network Auto Login

> 推荐向学校网络中心申请固定ip和免连线，需要教师用户在国科大办事大厅进行申请操作。

中国科学院大学（国科大）校园网自动登录脚本。

参考[UCAS-CampusNetwork-AutoLogin](https://github.com/RDSJC/UCAS-CampusNetwork-AutoLogin)，可惜该脚本依靠`ping`命令判断网络连接状态的方式在我的环境中未能正常工作，且selenium库更新过后一些方法被弃用。

```shell
.
├── autologin.bat  # windows bat 脚本例程
├── autologin.py   # 自动登录脚本
├── autologout.py  # 自动登出脚本例程
├── config.json    # 账户信息写在该文件里
├── LICENSE
├── my_env         # 附带的 python 环境
├── README.md
```

## ubuntu

1. 安装对应版本的chrome浏览器和chromedriver [download](https://getwebdriver.com/)
2. 填写 config.json
3. 手动运行脚本或设置自动计划 [ref](https://zhuanlan.zhihu.com/p/350671948)

```shell
./my_env/bin/python autologin.py --driver_path ./chromedriver --log_path ./.log.auto_login --config_path ./config.json
```
- 参数解析
    - `--driver_path` /path/to/chromedriver/
    - `--config_path` /path/to/config.json/，config文件中填写账号密码
    - `--log_path` /path/to/log/ 日志文件保存路径
    - `--debug` 指定该 flag，则打印详细的运行信息，并且不写入日志文件
    - `--login_url` 指定 校园网的登录url
    - `--username` 指定用户名。如果config.json中为空，则使用此值
    - `--password` 指定密码。如果config.json中为空，则使用此值

## windows

1. 安装对应版本的chrome浏览器和chromedriver [download](https://getwebdriver.com/)
    - 注意系统
2. 填写 config.json
3. 手动运行脚本

```cmd
\my_env\bin\python autologin.py --driver_path chromedriver.exe --log_path log.auto_login --config_path config.json
```
- 参数解析同ubuntu


4. 定时启动需要编写bat脚本，设置定时任务，并设定启动位置为该项目文件夹所在。参考 https://zhuanlan.zhihu.com/p/430602325

```bat
@echo off

start my_env\bin\python autologin.py --driver_path \path\to\chromedriver.exe --log_path log.auto_login --config_path config.json

exit
```
