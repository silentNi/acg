# -*- coding: utf-8 -*-
import scrapy
from acg.items import AcgItem
import json
from scrapy.selector import Selector

class AcgimagesSpider(scrapy.Spider):
    name = 'acgimages'
    allowed_domains = ['acg.fi']
    # start_urls = ['http://www.acg.fi/anime/page/1']
    # start_urls = ['http://www.acg.fi/hentai/page/1']
    start_urls = ['http://www.acg.fi/zhifu/page/1']
    crawled_pages = []
    POST_PAGE = 20  # 模拟向服务器发送请求 获取更多的图集 实际浏览器下拉发送请求
    # base_url = "http://www.acg.fi/anime/page/"
    # base_url = "http://www.acg.fi/hentai/page/"
    base_url = "http://www.acg.fi/zhifu/page/"
    now_page = 1
    MAX_PAGE = 32
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    ajax_header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '18',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '_ga=GA1.2.331506283.1533087892; _gid=GA1.2.24306714.1533087892; _gat_gtag_UA_71781637_7=1',
        'Host': 'www.acg.fi',
        'Origin': 'http://www.acg.fi',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.header, callback=self.parse)
        # return super().start_requests()

    def parse(self, response):
        # ajax动态加载页面
        # ajax每次动态加载页面就相当于加载下一页的数据   就不需要怕爬取下一个的数据了
        # for i in range(5,100):

        # anime-->进过测试 paged=33时 msg="" 只能请求 5-32
        # hetai-->经过测试 paged=33时 msg="" 只能请求 2-32
        # zhifu-->经过测试 paged=36时 msg="" 只能请求 2-35
        for i in range(2,36):
            ajax_url = "http://www.acg.fi/wp-admin/admin-ajax.php?action=zrz_load_more_posts"

            form_data = {
                "type": "catL4",
                "paged": str(i)
            }#  anime-->catL1 hetai-->catL2 zhifu-->catL4
            # print(response.cookies.items())
            self.header['Referer'] = response.url
            yield scrapy.FormRequest(url=ajax_url, headers=self.header, formdata=form_data,
                                               callback=self.ajax_parse)
            # print(ajax_response.cookies.items())
            # print(ajax_response)
        # return ajax_response
        #当前页面的有效连接
        # urls=response.css('.grid-bor a[href^="http://www.acg.fi/anime/"]::attr(href)').extract()
        # urls=response.css('.grid-bor a[href^="http://www.acg.fi/hentai/"]::attr(href)').extract()
        urls=response.css('.grid-bor a[href^="http://www.acg.fi/zhifu/"]::attr(href)').extract()
        for url in urls:
            print(url)
            print(len(self.crawled_pages))
            if url not in self.crawled_pages:
                self.crawled_pages.append(url)
                yield scrapy.Request(url=url,callback=self.detail_parse)
        #下一页 最多到 page/32
        # if self.now_page <self.MAX_PAGE:
        #     self.now_page=self.now_page+1
        #     next_url=self.base_url+str(self.now_page)
        #     yield scrapy.Request(url=next_url,callback=self.parse)
        # pass

    def ajax_parse(self, response):
        # print(response.body)
        json_obj=json.loads(response.body.decode("utf-8"))
        msg=json_obj["msg"]
        print(msg)
        #成功获取AJAX请求数据 对数据进行分析处理
        selector=Selector(text=msg)
        # urls=selector.css('a[href^="http://www.acg.fi/anime/"]::attr(href)').extract()
        # urls=selector.css('a[href^="http://www.acg.fi/hentai/"]::attr(href)').extract()
        urls=selector.css('a[href^="http://www.acg.fi/zhifu/"]::attr(href)').extract()
        for url in urls:
            print(url)
            if url not in self.crawled_pages:
                self.crawled_pages.append(url)
                yield scrapy.Request(url=url,callback=self.detail_parse)
        pass

    def detail_parse(self, response):
        images = response.css('.entry-content>div img::attr(src)').extract()
        print("find %d images in current page." % len(images))
        item = AcgItem()
        item["url"] = response.url
        item["images"] = images
        yield item
