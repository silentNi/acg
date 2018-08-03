# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class AcgPipeline(object):
    def process_item(self, item, spider):
        return item


class AcgImagesPipeline(ImagesPipeline):
    headers = {
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Accept-Encoding": 'gzip, deflate',
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Host": "img2.gov.com.de",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }

    def get_media_requests(self, item, info):
        self.headers["Referer"] = item["url"]
        if item["images"]:
            if item["images"][0].startswith("http://img.gov.com.de"):
                self.headers["Host"]="img.gov.com.de"
            if item["images"][0].startswith("http://img2.gov.com.de"):
                self.headers["Host"]="img2.gov.com.de"
        for image in item["images"]:
            print(type(image))
            yield scrapy.Request(url=image.strip(), headers=self.headers)
