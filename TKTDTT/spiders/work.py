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
        self.item["company"] = response.xpath('//h2[@class="desc-for-title mb-15"]/span/text()').extract()
        #self.item["salary"] = response.xpath('//div[@class="row row-standard"]/div[@class="col-md-7"]/p/span/text()').extract()[0]
        require = response.xpath('//div[@class="box multiple"]/div[@class="mw-box-item"]').extract()
        if len(require) > 2:
            self.item["require"] = re.sub(r'<.*?>', '. ', require[2])
        else:
            self.item["require"] = ""
        yield self.item