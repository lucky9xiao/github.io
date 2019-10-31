# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Wpaper.items import WpaperItem


class WallpaperSpider(CrawlSpider):
    name = 'WallPaper'
    allowed_domains = ['wallhaven.cc']
    start_urls = ['https://wallhaven.cc/toplist']

    rules = (
        # 匹配列表页的规则
        Rule(LinkExtractor(allow=r'.*/toplist\?page=\d'), follow=True),
        # 匹配详情页的规则
        Rule(LinkExtractor(allow=r'.*/w/[a-z0-9A-Z]{6}'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()

        img_true = response.xpath("//div[@class='scrollbox']/img[@id='wallpaper']/@src").get()
        img_small = "https://th.wallhaven.cc/small/{}/{}.jpg".format(img_true[-10:-8], img_true[-10:-4])
        Avatar = response.xpath("//dd[@class='showcase-uploader']/a[@class='avatar avatar-32']/img/@src").get()
        Uploader = response.xpath("//dd[@class='showcase-uploader']/a[@class='avatar avatar-32']/img/@alt").get()
        Category = response.xpath("//*[@id='showcase-sidebar']/div/div[1]/div[2]/dl/dd[2]/text()").get()
        Resolution = response.xpath("//*[@id='showcase-sidebar']/div/div[1]/h3/text()").get()
        Contrast = response.xpath("//div[@class='sidebar-content']/h3/@title").get()
        Size = response.xpath("//div[@class='sidebar-content']/div[@class='sidebar-section'][2]/dl/dd[3]/text()").get()
        tags_lis = response.xpath("//div[@class='sidebar-content']/div[@class='sidebar-section'][1]/ul[@id='tags']/li/a/text()").getall()
        Tags = ",".join(tags_lis)
        item = WpaperItem(img_true=img_true, img_small=img_small, Avatar=Avatar, Uploader=Uploader, Category=Category,
                          Resolution=Resolution, Contrast=Contrast, Size=Size, Tags=Tags)
        yield item
