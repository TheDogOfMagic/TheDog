# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from pyquery import PyQuery as pq
from ..items import AnjukeItem

class SipderSpider(scrapy.Spider):
    name = 'sipder'
    allowed_domains = ['www.anjuke.com']
    start_urls = ['http://www.anjuke.com/']
    start_url = 'https://www.anjuke.com/fangjia/'
    provinces = ['guangzhou']
    years = [str(item) for item in range(2010, 2020)]

    def start_requests(self):
        for province in self.provinces:
            for year in self.years:
                yield Request(self.start_url+province+year, callback=self.province_requests)

    def province_requests(self, response):
        # print(response.text)
        if response.text:
            html = pq(response.text)
            city = html('.div-border .items .elem-l a')
            province = html('.main-content h2').text()
            province = province[province.find('年')+1:province.find('房价')]
            for item in self.to_items(province, html('.avger .fjlist-wrap .boxstyle2')):
                yield item
            for i in range(city.length):
                yield Request(city.eq(i).attr('href'), callback=self.city_parse)
        else:
            print('未爬取有效网页：错误函数province_requests')

    def city_parse(self, response):
        if response.text:
            html = pq(response.text)
            province = html('.crumbs_wrap_top .commCrumb .crumb a')
            province = province.eq(3).text()
            province = province[4:province.find('房价')]
            for item in self.to_items(province, html('.avger .fjlist-wrap .boxstyle2')):
                yield item
        else:
            print('未爬取有效网页：错误函数city_requests')

    def to_items(self, province, pq_fjlist_box):
        item = AnjukeItem()
        h3 = pq_fjlist_box('h3').text()
        pq_fjlist_box = pq_fjlist_box.eq(0)
        date = pq_fjlist_box('ul li.clearfix')

        item['province'] = province
        item['city'] = h3[h3.find('年')+1:h3.find('房价')]
        for i in range(date.length):
            year_month = date.eq(i)
            str_date = year_month('a b').text()
            str_price = year_month('span').text()
            item['year'] = str_date[0:str_date.find('年')]
            item['month'] = str_date[str_date.find('年')+1:str_date.find('月')]
            item['price'] = str_price[0:str_price.find('元')]
            yield item


    def parse(self, response):
        pass
