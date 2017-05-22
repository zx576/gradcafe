# -*- coding: utf-8 -*-
import scrapy
from gradcafe.items import GradcafeItem
import re


class GcafeSpider(scrapy.Spider):
    name = "gcafe"
    allowed_domains = ["thegradcafe.com/survey/index.php"]
    # start_urls = ['http://thegradcafe.com/survey/index.php/']

    def __init__(self):
        # 初始化总页数和检查总页数
        self.TOTALPAGE = 10
        self.CHECKPAGE = True

    # 起始请求
    def start_requests(self):

        url = 'http://thegradcafe.com/survey/index.php?t=m&pp=250&o=&p='

        count = 1
        while count < self.TOTALPAGE:
            the_url = url + str(count)
            # 请求 the_url 页面，将响应数据发送到 parse 函数。
            yield scrapy.Request(the_url,callback=self.parse)
            count += 1


    def parse(self, response):

        # 使用 xpath 获取数据
        all_tr = response.xpath('//table[@id="my-table"]/tbody/tr')

        # 获取最大页面
        if self.CHECKPAGE:

            page_string = response.xpath('//div[@class="pagination"]')[0]
            page_string = page_string.xpath('string(.)')
            pattern = re.compile('over (\d+) pages')
            totalpage = re.findall(pattern,str(page_string))[0]
            self.TOTALPAGE = int(totalpage)
            self.CHECKPAGE = False


        # 逐行获取信息
        for tr in all_tr:

            # 建立一个数据存储实例
            item = GradcafeItem()

            all_td = tr.xpath('.//td')

            item['page_count'] = self.TOTALPAGE
            item['institution'] = all_td[0].xpath('./text()').extract()[0]
            item['program'] = all_td[1].xpath('./text()').extract()[0]

            decision_tag = all_td[2].xpath('.//span[@class="dAccepted"]/text() | .//span[@class="dRejected/text()"]')
            if decision_tag:
                item['decision'] = decision_tag[0].extract()[0]

            else:
                decision = 'default'

            item['date'] = all_td[2].xpath('./text()').extract()[0]

            st = all_td[3].xpath('./text()').extract()
            item['st'] = st[0] if st else 'default'

            item['date_added'] = all_td[4].xpath('./text()').extract()[0]

            notes = all_td[5].xpath('string(.)').extract()
            item['notes'] = ''.join(notes) if notes else 'default'

            # print('ins:{0}\t\t program:{1}\t\t decision:{2}\t\t data{3}\t\t st:{4}\t\t date_added:{5}\t\t note:{6}'.format(
            #     institution,program,decision,date,st,date_added,notes
            # ))
            # 返回该数据实例
            yield item
