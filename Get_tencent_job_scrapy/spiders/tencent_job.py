import scrapy
import time
import random
from Get_tencent_job_scrapy.items import Tencentitem


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
                yield item
        except:
            print('该页爬取不成功！')
            time.sleep(20)
            pass

        try:
            next_page = response.xpath("//a[@id='next']/@href").extract()[0]
            # print(next_page + '11111111111111')
            if next_page == 'javascript:;':
                print('爬取结束1！')
                pass
            else:
                url = self.url_init + next_page
                time.sleep(10 + random.randint(20, 100) / 20)
                yield scrapy.Request(url, callback=self.parse)
        except:
            print('爬取结束2！')
