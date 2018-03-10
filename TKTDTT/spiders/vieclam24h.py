# encoding: utf-8
import scrapy
from TKTDTT.items import TktdttItem
import re

class ViecLam24hSpider(scrapy.Spider):
    name = "vieclam24h"
    start_urls = [
        'https://vieclam24h.vn/tim-kiem-viec-lam-nhanh/?hdn_nganh_nghe_cap1=&hdn_dia_diem=&hdn_tu_khoa=&hdn_hinh_thuc=&hdn_cap_bac=',
    ]

    def parse(self, response):
        for tn in response.xpath('//div[@class="list-items "]/div/div/span'):
            src = tn.xpath('a/@href').extract_first()
            src = response.urljoin(src)
            yield scrapy.Request(src, callback=self.parse_src)

        next_pages = response.xpath('//li[@class="next"]/a/@href').extract()
        next_page = next_pages[len(next_pages) - 1]
        print("LOG")
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_src(self, response):
        self.item = TktdttItem()
        self.item["origin"] = "BùiHoàngLưu, CaoThanhTùng, NguyễnVõLinh, HàViếtTráng".decode('utf-8')
        self.item["url"] = response.request.url
        title = response.xpath('//div[@class="col-xs-12"]/h1[@class="text_blue font28 mb_10 mt_20 fws title_big"]/text()').extract()
        if len(title) > 0:
            self.item["title"] = title[0]
        else:
            self.item["title"] = ""
        des = response.xpath('//div[@class="row job_detail text_grey2 fw500 mt_6 mb_4"]').extract()
        if len(des) >0:
            desc = re.sub(r'<.*?>', ' ', des[0])
            desc = re.sub(r'\n', ' ', desc)
            desc = re.sub(r'\r', ' ', desc)
        else:
            desc = ""
        con = response.xpath('//div[@class="job_description bg_white mt_16 pb_18 box_shadow "]').extract()
        if len(con) > 0:
            cont = re.sub(r'<.*?>', ' ', con[0])
            cont = re.sub(r'\n', ' ', cont)
            cont = re.sub(r'\r', ' ', cont)
        else:
            cont = ""
        content = desc + "   " + cont
        self.item["content"] = content
        if self.item["content"] != "    " and self.item["title"] != "":
            yield self.item