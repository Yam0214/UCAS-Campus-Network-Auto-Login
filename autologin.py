from time import sleep
import json
import requests
import logging
import argparse
from pathlib import Path

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--driver_path", type=str, default="./chromedriver")
    parser.add_argument("--log_path", type=str, default=".auto_login.log")
    parser.add_argument("--config_path", type=str, default="./config.json")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--check_url", type="str", default="http://www.bilibili.com")
    parser.add_argument("--login_url", type=str, default="http://124.16.81.61")
    parser.add_argument("--username", type=str, default="")
    parser.add_argument("--password", type=str, default="")

    return parser.parse_args()


class AutoLogin:
    def __init__(self, args):
        self.driver_path = args.driver_path
        self._debug = args.debug

        config_path = Path(args.config_path)
        if config_path.exists():
            with open(config_path, "r", encoding="utf8") as file:
                json_dict = json.load(file)
        else:
            json_dict = {}
        self.login_url = json_dict.get("login_url", args.login_url)  # 校园网登录地址
        self.username = json_dict.get("username", args.username)  # 用户名
        self.password = json_dict.get("password", args.password)  # 密码
        # 联网判断地址
        self.check_url = args.check_url

        # 日志
        logging.basicConfig(
            filename=args.log_path if not self._debug else "",
            format="%(asctime)s [%(levelname)s] %(filename)s: %(message)s",
            datefmt="%y-%m-%d %H:%M:%S",
            level=logging.WARNING if not self._debug else logging.INFO,
        )

    def judge_net_state(self):
        """check net state by requests.get and return `False` if fail to link check_url."""
        response = requests.get(self.check_url)

        if not response.ok:
            # 无法链接 check url 甚至不会跳转 深澜软件，或许是WIFI链接错误
            logging.ERROR("Failed accessing to network.")
            return -1

        content = response.content.decode()
        soup = BeautifulSoup(content, features="lxml")
        if self._debug:
            print("响应页面标题：", soup.title.text, "\n校园网登陆页面：", soup.title.text == "深澜软件")
        if soup.title.text == "深澜软件":
            # 或者跳转深蓝软件
            logging.warning("failed linking to {}".format(self.check_url))
            return False

        else:
            logging.info("succeed linking to {}".format(self.check_url))
            return True

    def login(self):
        # 配置浏览器
        options = Options()
        options.add_argument("headless")  # 隐藏浏览器
        # 获取驱动
        driver = webdriver.Chrome(executable_path=self.driver_path, options=options)
        # 启动浏览器
        driver.get(self.login_url)
        # 设置定位等待时间(因网速原因需要等待网页加载好)
        driver.implicitly_wait(3)
        # 判断是否已经登录,已经登录则直接退出
        try:
            driver.find_element(By.ID, "logout")
            logging.info("already login.")
            driver.quit()
            return
        # 通过捕获"找不到登出元素异常"来判断未登录
        except Exception as e:
            logging.info("logged off.")

        # 设置定位等待时间
        driver.implicitly_wait(1)

        # 定位输入账号处并输入账号
        driver.find_element(By.ID, "username").send_keys(self.username)
        driver.implicitly_wait(1)

        # 定位密码并输入密码
        driver.find_element(By.ID, "password").send_keys(self.password)
        driver.implicitly_wait(1)

        # 定位登录并点击登录
        driver.find_element(By.ID, "login-account").click()
        driver.implicitly_wait(1)

        # 设置定位等待时间
        sleep(1)

        # 关闭浏览器
        driver.quit()
        logging.warning("auto login.")

    def run(self):
        # 判断联网状态
        try:
            state = self.judge_net_state()
        except:
            self.login()
        else:
            if state == -1:
                return
            if not state:
                self.login()


if __name__ == "__main__":
    args = parse_args()
    auto_login = AutoLogin(args)
    auto_login.run()
