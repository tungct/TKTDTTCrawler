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
        self.item["url"] = response.request.url
        self.item["title"] = response.xpath('//h1[@class="main-title"]/span/text()').extract()
        content = response.xpath('//div[@class="box multiple"]/div[@class="mw-box-item"]').extract()
        if len(content) > 1:
            self.item["content"] = re.sub(r'<.*?>', '. ', content[2])
        else:
            self.item["content"] = ""
        yield self.item