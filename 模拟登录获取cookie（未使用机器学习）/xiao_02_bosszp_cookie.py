# encoding=utf8
import time
import json
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from pynput.mouse import Button, Controller as c1


class Bosszp():
    def __init__(self):
        self.url = "https://login.zhipin.com/"

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

    def log_in(self):
        mouse = c1()
        driver = self.driver
        driver.get(self.url)
        driver.maximize_window()  # 窗口最大化
        time.sleep(1)  # 等1秒，等待页面加载
        while True:
            driver.refresh()  # 刷新页面
            time.sleep(2)  # 等2秒，等待页面加载
            # 滑块验证，并进行判断
            mouse.position = (933, 619)
            time.sleep(0.1)
            mouse.press(Button.left)
            time.sleep(0.2)
            mouse.move(50, 1)  # 鼠标移动
            time.sleep(0.2)
            mouse.move(60, -2)
            time.sleep(0.2)
            mouse.move(60, 2)
            time.sleep(0.2)
            mouse.move(110, 0)
            time.sleep(0.1)
            mouse.release(Button.left)
            time.sleep(1)
            element = driver.find_element_by_class_name('nc-lang-cnt').text
            if element == "验证通过":
                break
            else:
                continue
        # 输入账号
        driver.find_element_by_name("account").send_keys("user")
        time.sleep(1)
        # 输入密码
        driver.find_element_by_name("password").send_keys("password")
        time.sleep(1)
        # 点击登录
        driver.find_element_by_class_name("btn").click()
        time.sleep(5)
        # 获取登录用户名，若获取失败，抛出。
        try:
            user_name = driver.find_element_by_class_name("username").text
            print(user_name)
            print("登入成功")
        except Exception as e:
            print(e)
            driver.save_screenshot("zpfailure.jpg")
            print("登入失败，请重试")
        # 打印快照
        driver.save_screenshot("zpsuccessful.jpg")
        # 输出登入之后的cookies
        cookies = driver.get_cookies()
        # 关闭driver
        driver.quit()
        # 将cookies写入json文件中
        json_cookies = json.dumps(cookies)
        with open('zpcookies.json', 'w') as f:
            f.write(json_cookies)
        print(cookies)


if __name__ == "__main__":
    bosszp = Bosszp()  # 实例化
    bosszp.log_in()  # 调用登入方法