# -*- coding: utf-8 -*-
import scrapy

from getoc.items import LessonItem, CourseItem


class Oc163Spider(scrapy.Spider):
    name = "oc163"
    allowed_domains = ("open.163.com",)

    def __init__(self, url=None, *args, **kwargs):
        super(Oc163Spider, self).__init__(*args, **kwargs)
        self.start_urls = (url,)

    def parse(self, response):
        course_name = ''.join(response.css('.mainwrap h2::text').extract())
        course = CourseItem(name=course_name)
        yield course
        table = response.css('table.m-clist')[-1]
        for idx, elem in enumerate(table.css('td.u-ctitle a')):
            lesson = LessonItem(idx=(idx+1))
            lesson['title'] = ''.join(elem.xpath('text()').extract())
            lesson['url'] = ''.join(elem.xpath('@href').extract())
            yield lesson
