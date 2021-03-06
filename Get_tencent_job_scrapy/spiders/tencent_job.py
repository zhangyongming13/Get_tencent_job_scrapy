import scrapy
import time
import random
from Get_tencent_job_scrapy.items import Tencentitem
from functools import reduce


url = ['https://hr.tencent.com/position.php?&start=0']


class Tencent_job(scrapy.Spider):
    name = 'tencent_job'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0']
    url_init = 'https://hr.tencent.com/'
    flag = 1

    def parse(self,response):
        # 使用xpath选取， //表示在整个文档中匹配 tr表示div类型，@表示选取元素
        try:
            page_number = int(response.xpath("//a[@class='active']/text()").extract()[0]) - 1
            serial_number = 1
            data = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
            for each in data:  # in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
                item = Tencentitem()
                # 职位名
                # .表示从当前的路劲（即从上面的选择之后的路径） /表示当前路劲的根目录 @表示选取元素
                item['Job_id'] = serial_number + page_number * 10  # 生成每条记录的序号
                serial_number = serial_number + 1
                item["Job_name"] = each.xpath("./td[1]/a/text()").extract()[0]
                # 详细链接
                item["Job_link"] = 'https://hr.tencent.com/' + each.xpath("./td[1]/a/@href").extract()[0]
                # 职位类别
                try:
                    item["Job_kind"] = each.xpath("./td[2]/text()").extract()[0]
                except:
                    item["Job_kind"] = '空'
                # 招聘人数
                item["number"] = each.xpath("./td[3]/text()").extract()[0]
                # 工作地点
                item["place"] = each.xpath("./td[4]/text()").extract()[0]
                # 发布时间
                item["pubdate"] = each.xpath("./td[5]/text()").extract()[0]
                # meta用来传递已经爬取的数据
                # 进行岗位的具体工作职责和工作要求的爬取，重新定义request
                response_work = scrapy.Request(item["Job_link"], meta={'item':item}, callback=self.detail_parse)
                yield response_work
                # yield item
        except:
            print('该页爬取不成功！')
            recall_url = response._url
            time.sleep(30)
            yield scrapy.Request(recall_url, callback=self.parse)

        try:
            # 尝试获取下一页的链接，如果获取不到的话表明已经是最后一页了
            next_page = response.xpath("//a[@id='next']/@href").extract()[0]
            # print(next_page + '11111111111111')
            if next_page == 'javascript:;':  # 判断是否还有下一页
                print('爬取结束1！')
                pass
            else:
                url = self.url_init + next_page
                time.sleep(7 + random.randint(20, 100) / 20)
                yield scrapy.Request(url, callback=self.parse)  # 进行下一页链接的内容爬取
        except:
            print('爬取结束2！')

    def detail_parse(self, response_work):  # 爬取岗位链接内的具体内容
        item = response_work.meta['item']  # 接收已经爬取的数据
        # data = response_work.css("position_detail > div > table > tbody > tr:nth-child(3)")
        data = response_work.xpath("//tr[@class='c']")
        # position_detail > div > table > tbody > tr:nth-child(3)
        each_duty_work = data[0].xpath("./td/ul[@class='squareli']/li")  # 获取工作职责
        text_duty_work = []
        for i in each_duty_work:
            try:  # 因为有些li没有text文本（需要的数据）所以要进行错误判断
                work = i.xpath("./text()").extract()[0]
                text_duty_work.append(work + u' ')
            except:
                pass
        # 利用reduce对text_duty_work这个list的所有元素进行+的拼接操作
        item['duty_work'] = reduce(lambda x, y: str(x) + str(y), text_duty_work)
        data_Job_requirement = data[1].xpath("./td/ul[@class='squareli']/li")
        text_Job_requirement = []
        for i in data_Job_requirement:
            try:
                work = i.xpath("./text()").extract()[0]
                text_Job_requirement.append(work + u' ')
            except:
                pass
        item['Job_requirement'] = reduce(lambda x, y: str(x) + str(y), text_Job_requirement)
        yield item
