# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem


class TencentpostionSpider(scrapy.Spider):

    #爬虫名
    name = 'tencentPosition'

    #爬虫作用范围
    allowed_domains = ['tencent.com']

    url = "http://hr.tencent.com/position.php?&start="
    offset = 0

    #起始url
    start_urls = [url + str(offset)]

    #拉取到空数据处理（因为xpath在extract()[0],如果是空数据，会报错 "IndexError: list index out of range " ）
    def infoprocessing(self,info):
        if len(info) != 0:
            return info[0]
        else:
            return str('None')

    def parse(self, response):

        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):

            #初始化模型对象
            item = TencentItem()

            #职位名称
            # item['positionname'] = each.xpath("./td[1]/a/text()").extract()[0]
            EachPositionname = each.xpath("./td[1]/a/text()").extract()
            item['positionname'] = self.infoprocessing(EachPositionname)

            #详细链接
            # item['positionlink'] = each.xpath("./td[1]/a/@href").extract()[0]
            EachPositionlink = each.xpath("./td[1]/a/@href").extract()
            item['positionlink'] = self.infoprocessing(EachPositionlink)

            #职位类别
            # item['positionType'] = each.xpath("./td[2]/text()").extract()[0]
            EachpositionType = each.xpath("./td[2]/text()").extract()
            item['positionType'] = self.infoprocessing(EachpositionType)

            #招聘人数
            # item['positionNum'] = each.xpath("./td[3]/text()").extract()[0]
            EachpositionNum = each.xpath("./td[3]/text()").extract()
            item['positionNum'] = self.infoprocessing(EachpositionNum)

            #工作地点
            # item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]
            Eachworklocation = each.xpath("./td[4]/text()").extract()
            item['workLocation'] = self.infoprocessing(Eachworklocation)

            #发布时间
            # item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]
            EachpublishTime = each.xpath("./td[5]/text()").extract()
            item['publishTime'] = self.infoprocessing(EachpublishTime)

            yield item

        if self.offset < 3000:
            self.offset += 10

        #每次处理完一页的数据之后，重新发送下一页页面请求
        #self.offset自层10，同事拼接为新的url，并调用回调函数self.parse处理Response
        yield scrapy.Request(self.url + str(self.offset),callback=self.parse)


