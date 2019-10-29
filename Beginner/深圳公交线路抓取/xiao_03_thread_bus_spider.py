# coding=utf-8
import requests
import json
import threading
from lxml import etree
from queue import Queue


class ThreadBusSpidier:
    def __init__(self):
        """初始化

        self.line_queue:放置线路名称的队列
        self.url_queue:放置目标网页的队列
        self.html_queue:放置获取的html内容的队列
        self.content_queue:放置所需内容的队列
        """
        self.line_list = "https://shenzhen.8684.cn/line{}"
        self.url_temp = "https://shenzhen.8684.cn{}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"}
        self.line_queue = Queue()
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()
        self.all_progress = []  # 用于设置进度条
        self.a = 0  # 用于设置进度条

    def get_url_list(self):
        """获取目标网页列表

        res:用于获取公交路线的响应
        con:用于获取公交路线的内容
        """
        while True:
            line_url = self.line_queue.get()
            res = requests.get(line_url, headers = self.headers)
            con = etree.HTML(res.content.decode()).xpath(".//div[@class='list clearfix']/a/@href")
            for i in con:
                url = self.url_temp.format(i)
                self.all_progress.append(url)
                self.url_queue.put(url)
            self.line_queue.task_done()  # 用于减少计数

    def parse_url(self):
        """用获取的目标网页发送请求，获取响应。

        """
        while True:
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            self.html_queue.put(response.content.decode())
            self.url_queue.task_done()

    def get_content_list(self):
        """提取数据

        html:解析形成的html对象
        content_list:放置所需内容的列表
        item:获取的目标内容
        """
        while True:
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            content_list = []
            item = {}
            item_title = html.xpath(".//div[@class='info']/h1/text()")
            item["title"] = item_title[0] if len(item_title)>0 else None
            item_time = html.xpath(".//div/ul[@class='bus-desc']/li/text()")
            item["time"] = item_time[0] if len(item_time)>0 else None
            item["price"] = item_time[1] if len(item_time) > 0 else None
            item_trip = html.xpath(".//div[@class='trip']/text()")
            item_trip_left = item_trip[0] if len(item_trip) > 0 else None
            item_trip_right = item_trip[1] if len(item_trip) > 1 else None
            item_trip_station = html.xpath(".//div[@class='bus-lzlist mb15']")
            item[item_trip_left] = item_trip_station[0].xpath(".//ol/li/a/text()") if len(item_trip_station) > 0 else None
            item[item_trip_right] = item_trip_station[1].xpath(".//ol/li/a/text()") if len(item_trip_station) > 1 else None
            content_list.append(item)
            self.content_queue.put(content_list)
            self.html_queue.task_done()

    def save_content_list(self, ):
        """保存内容

        """
        while True:
            content_list = self.content_queue.get()
            for i in content_list:
                file_save = open("./record.json", "a")
                data = json.dump(i, file_save, ensure_ascii=False, indent=2)
                file_save.close()
                # 设置显示下载进度
                self.a += 1
                print("\r下载进度：%.2f%%" % (self.a*100/len(self.all_progress)), end="")
            self.content_queue.task_done()

    def run(self):
        """主程序

        thread_list:多线程列表
        """
        thread_list = []
        # 1. 获取url列表
        for i in range(1,7):
            self.line_queue.put(self.line_list.format(i))
        for i in range(3):
            t_url = threading.Thread(target=self.get_url_list)
            thread_list.append(t_url)
        # 2. 遍历，发送请求，获取响应
        for i in range(12):
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)
        # 3. 提取数据
        for i in range(8):
            t_html = threading.Thread(target=self.get_content_list)
            thread_list.append(t_html)
        # 4. 保存
        for i in range(3):
            t_save = threading.Thread(target=self.save_content_list)
            thread_list.append(t_save)

        # 5. 设置主线程结束，子线程结束。
        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，该线程不重要。
            t.start()

        # 6. 让主线程等待阻塞，等待队列的任务完成之后再完成。
        for q in [self.line_queue, self.url_queue, self.html_queue, self.content_queue]:
            q.join()
        print("\n下载结束")


if __name__ == '__main__':
    bus_spider = ThreadBusSpidier()
    bus_spider.run()
