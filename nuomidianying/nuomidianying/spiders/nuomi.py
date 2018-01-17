# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urlencode
import re

from ..items import NuomidianyingItem

class NuomiSpider(scrapy.Spider):
    name = 'nuomi'
    allowed_domains = ['dianying.nuomi.com']
    start_urls = ['http://dianying.nuomi.com/']


    def start_requests(self):

        start_url="https://dianying.nuomi.com/movie/getmovielist?pagelets[]=pageletMovielist&type=new&pageNum=0"
        yield Request(start_url,callback=self.get_page_num)


    def get_page_num(self,response):

        pageNum=response.xpath('//div[contains(@id,"pagerInfo")]/@data-pagecount').extract_first()
        pageNum = int(re.findall(r'\d+',pageNum)[0])
        print(pageNum)
        start_url = "https://dianying.nuomi.com/movie/getmovielist?pagelets[]=pageletMovielist&"

        for page in range(1,pageNum+1):
            params={
                "type": "new",
                "cityId": "131",
                "pageNum": page,
                "pageSize": "10",
                "needMovieNews": "false"}

            index_url = start_url + urlencode(params)
            # print('=====>> 运行',start_url)
            yield Request(index_url,callback=self.parse_index)


    def parse_index(self, response):
        base_url = "https://dianying.nuomi.com/movie/detail?movieId="
        detail_urls= [base_url + re.findall(r"\d+",item)[0] for item in  response.xpath('//a/@data-data').extract()]
        for detail_url in detail_urls:
            yield Request(detail_url,callback=self.parse_detail)

    def parse_detail(self,response):

        title = response.xpath('//*[@id="detailIntro"]/div/div[2]/h4/text()').extract_first()
        desc = response.xpath('//*[@id="detailIntro"]/div/div[2]/div[2]/p[1]/text()').extract_first()
        director = response.xpath('//*[@id="detailIntro"]/div/div[2]/div[2]/p[2]/text()').extract_first().split("\xa0\xa0\xa0\xa0")[0]
        actor = response.xpath('//*[@id="detailIntro"]/div/div[2]/div[2]/p[2]/text()').extract_first().split("\xa0\xa0\xa0\xa0")[1]
        show_time = re.findall(r'\d+-\d+-\d+.*?', response.xpath('//*[@id="detailIntro"]/div/div[2]/div[2]/p[3]/text()').extract_first())[0]
        intro = response.xpath('//*[@id="intro"]/text()').extract_first()

        item = NuomidianyingItem()

        item["title"] = title
        item["desc"] = desc
        item["director"] = director
        item["actor"] = actor
        item["show_time"] = show_time
        item["intro"]= intro

        yield item


