import scrapy
from TKTDTT.items import TktdttItem
import re

class VnWorkSpider(scrapy.Spider):
    name = "work"
    start_urls = [
        'https://mywork.com.vn/tuyen-dung/38/it-phan-mem.html',
    ]

    def parse(self, response):
        for tn in response.xpath('//div[@class="row job-item"]/div/div/div/p'):
            src = tn.xpath('a/@href').extract_first()
            src = response.urljoin(src)
            yield scrapy.Request(src, callback=self.parse_src)

        next_pages = response.xpath('//li[@class="page-item"]/a/@href').extract()
        next_page = next_pages[len(next_pages)-1]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_src(self, response):
        self.item = TktdttItem()
        self.item["job"] = response.xpath('//div[@class="col-md-7"]/h1/span/text()').extract()
        # self.item["company"] = response.xpath('//h1[@class="comp-name"]/a/text()').extract()
        # self.item["area"] = response.xpath('//p/b/span/a/text()').extract()
        # salary = ""
        # for sl in response.xpath('//p/b/span[@class="norB colorG"]/text()').extract():
        #     salary = salary + "-" + sl
        # self.item["salary"] = salary
        # info_job = response.xpath('////div[@class="info_job"]/li[@class="home-col12"]/p/text()').extract()
        # self.item["exp"] = info_job[0]
        # self.item["quantum"] = info_job[2]
        # desjob = response.xpath('//div[@class="desjob-company"]').extract()
        # self.item["description"]  = re.sub(r'<.*?>', '', desjob[1])
        # self.item["benefit"] = re.sub(r'<.*?>', '', desjob[2])
        # self.item["require"] = re.sub(r'<.*?>', '', desjob[3])
        # self.item["cv"] = re.sub(r'<.*?>', '', desjob[4])
        # self.item["skill"] = response.xpath('//div[@class="desjob-company"]/div/span/a/text()').extract()
        # self.item["addresscompany"] = response.xpath('//div[@class="boxcontact-copmpany"]/table/tbody/tr[2]/td[2]/text()').extract()
        # self.item["deadline"] = response.xpath('//div[@class="boxcontact-copmpany"]/table/tbody/tr[4]/td[2]/text()').extract()

        yield self.item