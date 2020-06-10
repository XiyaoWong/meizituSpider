# -*- coding: utf-8 -*-
import re
import time
from pprint import pprint

import scrapy

from meizituSpider.items import MeizituspiderItem


class MeizituSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ['meizitu.com']
    start_urls = ['https://www.meizitu.com/']

    def parse(self, response):
        html = response.text
        category_post_links = set(re.findall(r'https://www\.meizitu\.com/a/.*?\.html', html))
        post_links = set(re.findall(r'https://www\.meizitu\.com/a/\d+.html', html))
        for post_link in post_links:
            yield scrapy.Request(
                post_link,
                callback=self.parse_detail
            )

        category_links = category_post_links.difference(post_links)
        tag_links = set(re.findall(r'href="(https://www\.meizitu\.com/tag/.*?\.html)"', html))
        page_links = {"https://www.meizitu.com" + link for link in re.findall(r"<a href='(/a/.*?\.html)'>", html)}
        next_links = category_links | tag_links | page_links
        for next_link in next_links:
            yield scrapy.Request(
                next_link,
                callback=self.parse
            )

    def parse_detail(self, response):
        html = response.text
        item = MeizituspiderItem()

        try:
            title = re.findall(r'<h2><a href="https://www\.meizitu\.com/a/\d+\.html">(.*?)</a></h2>', html)[0]
        except Exception:
            title = "无标题" + str(int(time.time()))

        try:
            tag_str = re.findall(r'<p>Tags:(.*?\s+)</div>\s+<div class="metaLeft">', html)[0]  # type: str
            space = re.compile(r'\s{1,}')
            tag_str = space.sub("", tag_str)
            tags = [tag for tag in tag_str.split(",") if tag]
        except Exception:
            pass
        tags.append("mm")

        try:
            day = re.findall(r'<div class="day">(.*?)</div>', html)[0]
            month, year = re.findall(r'<div class="month_Year">(.*?)&nbsp;(.*?)</div>', html)[0]
            date = f"{year}-{month}-{day}"
        except Exception:
            date = "0000-00-00"

        imgs = re.findall(r'<img alt=".*?".*?src="(.*?\.jpg)" /><br />', html)
        # pprint(title)
        # pprint(tags)
        # pprint(date)
        # pprint(imgs)

        if imgs:
            item["title"] = title
            item["tags"] = tags
            item["date"] = date
            item["imgs"] = imgs
            return item
