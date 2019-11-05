# coding=utf8
import time
import json
from lxml import etree
from selenium import webdriver


class TaobaoSpider():
    def __init__(self):
        option = webdriver.ChromeOptions()
        # 设置为开发者模式，防止被各大网站识别出来使用了Selenium
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 不加载图片,加快访问速度
        option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 去掉提示：Chrome正收到自动测试软件的控制
        option.add_argument('disable-infobars')
        # 设置为无头模式
        # option.add_argument('--headless')
        # 添加user_agent
        # ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
        # option.add_argument('user-agent=' + ua)
        # 如果没有在环境变量指定Chrome位置
        # self.driver = webdriver.Chrome(executable_path="./..."), options=option)

        self.start_url = "https://www.taobao.com/"
        self.parsed_count = 0  # 抓取页面计数器。
        self.refresh_count = 0  # 创建刷新计数器。若保存成功，清零；若失败，次数加一并刷新页面。
        self.driver = webdriver.Chrome(options=option)  # 启动
        # 窗口最大化
        # self.driver.maximize_window()

    # 从文件获取cookie
    def get_cookie(self):
        with open("./tbcookies.json", "r") as f:
            cookie = json.load(f)
            return cookie

    # 解析当前页，获取item
    def get_contents(self):
        self.parsed_count += 1
        time.sleep(2.5)  # 等待2.5s
        selector = etree.HTML(self.driver.page_source)  # 创建选择器
        need_li = selector.xpath("//div[@class='grid g-clearfix']/div[@class='items']/div[@class='item J_MouserOnverReq  ']")
        self.contents = []
        for i in range(len(need_li)):
            for need in need_li[i][0]:  # 此处若不加[0]，可能会出现同种商品输出2次
                item = {}
                item["title"] = need.xpath("//img[@class='J_ItemPic img']/@alt")[i]
                item["price"] = need.xpath("//div[@class='price g_price g_price-highlight']/strong/text()")[i].strip()
                item["sales"] = need.xpath("//div[@class='row row-1 g-clearfix']/div[@class='deal-cnt']/text()")[i].strip()
                item["store"] = need.xpath("//div[@class='shop']/a[@class='shopname J_MouseEneterLeave J_ShopInfo']/span[2]/text()")[i].strip()
                item["city"] = need.xpath("//div[@class='row row-3 g-clearfix']/div[@class='location']/text()")[i].strip()
                # print(item)
                self.contents.append(item)

    # 循环  点击下一页按钮，解析和保存直至最后一页或者达到max_page
    def repeat_parse(self, max_page):
        driver = self.driver
        while True:
            nextpage = driver.find_elements_by_xpath(
                "//div[@class='inner clearfix']/ul[@class='items']/li[@class='item next']/a[@class='J_Ajax num icon-tag']/span")
            try:
                if nextpage:
                    nextpage[0].click()  # 点击下一页
                    self.get_contents()  # 解析当前页
                    self.itempipeline()  # 保存内容
                    self.refresh_count = 0  # 刷新计数器归零
                    self.last_url = driver.current_url  # 获取最后的url
                    driver.save_screenshot("successful.png")  # 保存快照
                    if max_page <= self.parsed_count:
                        break
                    continue
                elif self.refresh_count < 10:
                    self.refresh_count += 1
                    driver.refresh()  # 刷新，防止空白页机制
                else:
                    print(self.last_url)  # 打印最后url
                    break
            except:
                driver.refresh()
                time.sleep(3)
                movelock = driver.find_elements_by_xpath("//span[@class='nc-lang-cnt']")
                if movelock:
                    print(self.last_url)  # 打印最后url
                    driver.save_screenshot("fail_lock.png")  # 保存快照
                    # 可尝试使用ActionChains+pynput解锁
                    print("出现滑块解锁")
                    break

    # 保存数据
    def itempipeline(self):
        with open("./taobaofilco.json", "a", encoding="utf8") as f:
            f.write(json.dumps(self.contents, indent=4, ensure_ascii=False) + "," + "\n")

    # 主程序
    def run(self):
        driver = self.driver
        driver.get(self.start_url)  # 发送首页第一次请求
        cookies = self.get_cookie()  # 获取cookie
        driver.delete_all_cookies()  # 删除现有的所有cookies
        for cookie in cookies:  # 添加cookie
            if 'expiry' in cookie:
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(3)
        driver.get(self.start_url)  # 再次发送请求
        time.sleep(3)
        driver.find_element_by_id('q').clear()  # 清空搜索框
        driver.find_element_by_id('q').send_keys('filco机械键盘')  # 输入搜索内容
        driver.find_element_by_class_name('btn-search').click()  # 点击搜索
        self.get_contents()  # 解析url
        self.itempipeline()  # 保存数据
        self.repeat_parse(3)  # 循环  点击下一页按钮，解析和保存直至下一页按钮不存在
        driver.save_screenshot("end.png")  # 保存结束快照
        driver.quit()  # 结束webdriver
        print("抓取结束")


if __name__ == '__main__':
    tbspider = TaobaoSpider()  # 实例化
    tbspider.run()  # 调用主程序