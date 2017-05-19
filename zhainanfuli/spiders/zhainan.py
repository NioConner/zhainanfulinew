# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from bs4 import BeautifulSoup
import re

from zhainanfuli.items import ZhainanfuliItem


class ZhainanSpider(Spider):
    name = "zhainan"
    allowed_domains = ["www.usezy.com"]
    start_urls = ['http://www.usezy.com/']
    url = 'http://www.usezy.com'

    def start_requests(self):
        yield Request(self.url,callback=self.parse)

    def parse(self, response):
        lis = BeautifulSoup(response.text, 'lxml').find_all('li')
        for li in lis:
            if len(li)>0:
                bush_url = li.find('a')['href']
                type = li.find('a').get_text()
                url = self.url+bush_url

                yield Request(url,callback=self.get_allpage,meta={'bush_url':bush_url})

    def get_allpage(self, response):
        page = BeautifulSoup(response.text, 'lxml').select(".pagebtn")
        max_page = re.findall(r'\d+', str(page))[0]
        # 获取分类后的最大页码数
        bush_url = 'index-'
        last_url = '.html'
        for i in range(2,int(max_page)):
            url = self.url + str(response.meta['bush_url']) + bush_url + str(i) + last_url

            yield Request(url,callback=self.parse_page)



    def parse_page(self, response):

        tds = BeautifulSoup(response.text, 'lxml').find_all('td' ,style="border-bottom: 1px solid #bde4c1; padding-left: 15px;")



        #先找到所有style为上图的td这些是分类页面下的条目
        for td in tds:
            bush_url = td.find('a')['href']
            name = td.find('a').get_text()
            mov_id = bush_url
            url = self.url+bush_url


            yield Request(url, callback=self.get_xfurl, meta={'name': name, 'mov_id':mov_id})

    def get_xfurl(self, response):
        item = ZhainanfuliItem()
        item['name'] = str(response.meta['name'])
        item['mov_id'] = str(response.meta['mov_id'])
        #item['type'] = str(response.meta['type'])#这个type好像不能传这么远
        pic = response.xpath('/html/body/table[2]/tbody/tr/td/div[2]/img/@src').extract()[0]
        if len(pic)>0:
            item['pic'] = pic
        else:
            item['pic'] = '没有相关图片'
        item['xplay_url'] = response.xpath('//*[@id="plist"]/table[2]/tbody/tr[2]/td/ul/li/input/@value').extract()[0]
        return  item



