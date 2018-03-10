# encoding: utf-8
import scrapy
from TKTDTT.items import TktdttItem
import re

class CareerBuilderSpider(scrapy.Spider):
    name = "careerbuilder"
    start_urls = [
        'https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-vi.html',
    ]

    def parse(self, response):
        for tn in response.xpath('//h3[@class="job"]'):
            src = tn.xpath('a/@href').extract_first()
            src = response.urljoin(src)
            yield scrapy.Request(src, callback=self.parse_src)

        next_pages = response.xpath('//a[@class="right"]/@href').extract()
        next_page = next_pages[len(next_pages)-1]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_src(self, response):
        self.item = TktdttItem()
        self.item["origin"] = "BùiHoàngLưu_CaoThanhTùng_NguyễnVõLinh_HàViếtTráng".decode('utf-8')
        self.item["url"] = response.request.url
        title = response.xpath('//div[@class="top-job-info"]/h1/text()').extract()
        if len(title) > 0:
            self.item["title"] = title[0]
        else:
            self.item["title"] = ""
        des = response.xpath('//div[@class="box2Detail"]').extract()
        if len(des) > 0:
            desc = re.sub(r'<.*?>', ' ', des[0])
            desc = re.sub(r'\n', ' ', desc)
            desc = re.sub(r'\r', ' ', desc)
        else:
            desc = ""
        con = response.xpath('//div[@class="MarBot20"]').extract()
        content = ""
        for cont in con:
            cont = re.sub(r'<.*?>', ' ', cont)
            cont = re.sub(r'\n', ' ', cont)
            cont = re.sub(r'\r', ' ', cont)
            content = content + " " + cont
        self.item["content"] = desc + "  " + content
        if self.item["content"] != "    " and self.item["title"] != "":
            yield self.item