# coding=utf8
import time
import json
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from pynput.mouse import Button, Controller as c1
from pynput.keyboard import Key, Controller as c2


class Taobao():
    def __init__(self):
        self.url = "https://login.taobao.com/"

        # 如果没有在环境变量指定Chrome位置
        # driver = webdriver.Chrome(executable_path="./..."))

        # 设置为开发者模式，防止被各大网站识别出来使用了Selenium
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = Chrome(options=option)
        # 不加载图片,加快访问速度
        option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 添加user_agent
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
        option.add_argument('user-agent=' + ua)

    # 切换登录界面
    def switch_login(self, mouse):
        mouse.position = (1475, 303)  # 将鼠标移动至目标坐标
        time.sleep(0.5)
        mouse.press(Button.left)  # 按下左键，未放开
        time.sleep(0.5)
        mouse.release(Button.left)  # 释放左键
        time.sleep(1)

    # 输入账号
    def input_username(self, mouse, keyboard):
        mouse.position = (1251, 380)
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.5)
        mouse.release(Button.left)
        keyboard.type("us")  # 输入账号的一部分,分多次输入,防止被识别
        time.sleep(0.5)
        keyboard.type("er")  # 输入账号的另一部分
        time.sleep(0.5)

    # 输入密码（未出现滑块验证）
    def input_password_before(self, mouse, keyboard):
        mouse.position = (1251, 440)
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.5)
        mouse.release(Button.left)
        keyboard.type("pass")  # 输入密码的一部分，分多次输入，防止被识别
        time.sleep(0.5)
        keyboard.type("word")  # 输入密码的另一部分
        time.sleep(1.5)

    # 输入密码（已出现滑块验证）
    def input_password_later(self, mouse, keyboard):
        mouse.position = (1251, 440)
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.5)
        mouse.release(Button.left)
        keyboard.type("pass")
        time.sleep(0.5)
        keyboard.type("word")
        time.sleep(0.5)

    # 点击登录（未出现验证）
    def click_login(self, mouse):
        mouse.position = (1200, 500)
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.5)
        mouse.release(Button.left)
        time.sleep(2)

    # 点击登录（已出现验证）
    def click_login_later(self, mouse):
        mouse.position = (1224, 570)
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.5)
        mouse.release(Button.left)
        time.sleep(5)

    # 进行滑块验证
    def slide_code(self, mouse):
        mouse.position = (1200, 505)
        time.sleep(0.1)
        mouse.press(Button.left)
        time.sleep(0.2)
        mouse.move(50, 1)
        time.sleep(0.2)
        mouse.move(60, -2)
        time.sleep(0.2)
        mouse.move(60, 2)
        time.sleep(0.2)
        mouse.move(100, 0)
        time.sleep(0.1)
        mouse.release(Button.left)

    # 主程序
    def log_in(self):
        mouse = c1()
        keyboard = c2()
        driver = self.driver
        driver.get(self.url)
        driver.maximize_window()  # 页面最大化
        time.sleep(2)  # 睡2秒钟，等待页面加载
        while True:  # 循环直至登录成功
            driver.refresh()  # 刷新页面
            time.sleep(2)
            # 切换成账号密码登录（默认打开是快速登录界面）
            self.switch_login(mouse)
            # 输入账号
            self.input_username(mouse, keyboard)
            # 输入密码
            self.input_password_before(mouse, keyboard)
            # 点击登录（默认未出现滑块验证，若出现滑块验证，y坐标增加70）
            self.click_login(mouse)
            # 进行滑块验证
            self.slide_code(mouse)
            # 再次输入密码
            self.input_password_later(mouse, keyboard)
            # 点击登录
            self.click_login_later(mouse)
            # 登入后获取用户名，若获取失败，重新登录。
            try:
                user_name = driver.find_element_by_class_name("site-nav-login-info-nick ").text
                print(user_name)
                print("登入成功")
                break
            except Exception as e:
                print(e)
                self.driver.save_screenshot("tbfailture.png")
                continue
        # 打印快照
        self.driver.save_screenshot("successful.png")
        # 输出登陆之后的cookies
        cookies = self.driver.get_cookies()
        # 关闭driver
        driver.quit()
        # 将cookies写入json文件中
        json_cookies = json.dumps(cookies)
        with open('tbcookies.json', 'w') as f:
            f.write(json_cookies)
        print(cookies)


if __name__ == "__main__":
    taobao_cookie = Taobao()  # 实例化
    taobao_cookie.log_in()  # 调用登陆方法