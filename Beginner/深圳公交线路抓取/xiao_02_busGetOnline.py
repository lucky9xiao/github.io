# coding=utf-8
import requests
from bs4 import BeautifulSoup


class BusStation:
    def __init__(self):
        """初始化

        """
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"}

    def get_bus_url(self, bus_name):
        """获取并返回路线url

        :param bus_name:
        :return:
        """
        start_url = "https://shenzhen.8684.cn/so.php?q={}&k=pp".format(bus_name)
        return start_url

    def judge_url(self, test_url):
        """判断url是否能获取站点，并给出选择。

        :param test_url:
        :return:
        """
        res = requests.get(test_url, headers=self.headers)
        cont = res.content.decode()
        soup = BeautifulSoup(cont, "lxml")
        bus_station = soup.select("div.bus-lzlist.mb15")
        # print(bus_station)
        if len(bus_station) == 0:
            bus_list = soup.select("div.list.clearfix > a")
            # print(bus_list)
            print("您是不是要找以下路线:\n")
            i = 0
            for bus in bus_list:
                print("%s[%d]  " % (bus.get_text(), i))
                i += 1
            try:
                select = input("请输入您的选择： ")
                # url_num = soup.select("div.list.clearfix")[int(select)]
                url_num = soup.select("div.list.clearfix > a")[int(select)]
                # print(url_num)
                url_num = url_num.attrs["href"]
                url = "https://shenzhen.8684.cn{}".format(str(url_num))
                # print(url)
                return url
            except Exception as e:
                print(e)
        else:
            url = test_url
            return url

    def get_data(self, url):
        """获取并显示数据

        :param url:
        """
        response = requests.get(url, headers=self.headers)
        content = response.content.decode()
        soup = BeautifulSoup(content, "lxml")
        bus_num = soup.select("div[class=name]")[0].get_text().replace("公交车路", "")
        trip_time = soup.select(".bus-desc > li")[0].get_text()
        destination_left = soup.select("div[class=trip]")[0].get_text()
        destination_right = soup.select("div[class=trip]")[1].get_text()

        print("\n%s\n%s\n\n[1]运行方向：%s" % (bus_num, trip_time, destination_left))
        bus_station_left = soup.select("div.bus-lzlist.mb15")[0]
        station_list_0 = []
        for station in bus_station_left.select("li"):
            station_list_0.append(station.get_text())
        print("->".join(station_list_0))

        print("\n\n[2]运行方向：%s" % (destination_right))
        bus_station_right = soup.select("div.bus-lzlist.mb15")[1]
        station_list_1 = []
        for station in bus_station_right.select("li"):
            station_list_1.append(station.get_text())
        print("->".join(station_list_1))
        print("\n")

    def run(self):
        """实现主要程序

        """
        # 1. 获取查询线路url
        bus_name = input("请输入您要查询的深圳交通线路: ")
        test_url = self.get_bus_url(bus_name)

        # 2. 判断是否为确认url并获取
        url = self.judge_url(test_url)
        print(url)

        # 3. 提取数据
        self.get_data(url)


if __name__ == '__main__':
    bus_station = BusStation()
    bus_station.run()