# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlzhipin.items import CrawlzhipinItem


class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101280600/?query=python&page=1']
    # start_urls = ['https://www.zhipin.com/job_detail/d70748aa24d71c551nZ92Nm8FVc~.html']

    rules = (
        # 匹配职位列表页的规则
        Rule(LinkExtractor(allow=r'.+/c101280600/\?query=python&page=\d'), follow=False),
        # 匹配职位详情页的规则 652df29de1e46de4031z2di9F1c
        Rule(LinkExtractor(allow=r'.+job_detail/[a-zA-Z0-9_-]{27}~.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        name = response.xpath("///div[@class='info-primary']/div[@class='name']/h1/text()").get()
        name = name.strip() if name else None
        # print(name)
        salary = response.xpath("//div[@class='info-primary']/div[@class='name']/span[@class='salary']/text()").get()
        salary = salary.strip() if salary else None
        # print(salary)
        company_info = response.xpath(
            "//div[@class='job-primary detail-box']/div[@class='info-primary']/p//text()").getall()
        company = response.xpath(
            "//div[@class='job-detail']/div[@class='detail-content']/div[@class='job-sec']/div[@class='name']/text()").get()
        company = company.strip() if company else None
        city = company_info[0].strip() if len(company_info[0]) > 0 else None
        work_years = company_info[1].strip() if len(company_info[1]) > 0 else None
        education = company_info[2].strip() if len(company_info[2]) > 0 else None
        item = CrawlzhipinItem(name=name, salary=salary, city=city, work_years=work_years, education=education,
                               company=company)
        yield item
