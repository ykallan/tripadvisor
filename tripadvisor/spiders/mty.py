# -*- coding: utf-8 -*-
import scrapy


class MtySpider(scrapy.Spider):
    name = 'mty'
    # allowed_domains = ['tripadvisor.cn']
    start_urls = ['https://www.tripadvisor.cn/Hotels-g294211-China-Hotels.html']
    base_https = 'https://www.tripadvisor.cn'

    def parse(self, response):
        shiqus = response.xpath('//div[@class="leaf_geo_list_wrapper"]/div[@class="geo_wrap"]/a/@href').getall()
        for shiqu in shiqus:
            # print(self.base_https+shiqu)
            yield scrapy.Request(url=self.base_https+shiqu, callback=self.parse_shiqu_hotel)
            break

        next_page = response.xpath('//a[@class="nav next ui_button primary"]/@href').get()
        if next_page:
            yield scrapy.Request(url=self.base_https+next_page, callback=self.next_shiqu)

    def next_shiqu(self, response):
        shiqus = response.xpath('//ul[@class="geoList ui_columns is-multiline"]/li/a/@href').getall()
        for shiqu in shiqus:
            yield scrapy.Request(url=self.base_https+shiqu, callback=self.parse_shiqu_hotel)
            break

        next_page = response.xpath('//a[@class="nav next ui_button primary"]/@href').get()
        if next_page:
            yield scrapy.Request(url=self.base_https+next_page, callback=self.next_shiqu)

    def parse_shiqu_hotel(self, response):
        hotel_urls = response.xpath('//div[@class="listing_title"]/a/@href').getall()
        for hotel in hotel_urls:
            yield scrapy.Request(url=self.base_https+hotel, callback=self.parse_detail_hotel)

        next_page = response.xpath('//div[@data-targetevent="update-main_pagination_bar:dusty_hotels_resp"]//a[@class="nav next ui_button primary"]/@href').get()
        if next_page:
            yield scrapy.Request(url=self.base_https+next_page,callback=self.parse_shiqu_hotel)

    def parse_detail_hotel(self, response):
        hotel_name = response.xpath('//h1[@class="hotels-hotel-review-atf-info-parts-Heading__heading--2ZOcD"]/text()').get()
        loc = response.xpath('//div[@class="hotels-hotel-review-atf-info-parts-ATFInfo__businessListingWrapper--1ugx9"]//span[2]/span/text()').get()
        might_price = response.xpath('//div[@class="hotels-hotel-offers-DominantOffer__price--D-ycN"]/text()').get()
        if not might_price:
            price_resource = response.xpath('//div[@class="ui_column is-4 hotels-hotel-offers-DetailChevronOffer__logo--2JJsC"]/img/@alt').getall()
            prices = response.xpath('//div[@class="hotels-hotel-offers-DetailChevronOffer__price--py2LH"]/text()').getall()
            for i in range(len(prices)):
                print(price_resource[i], prices[i])

        print(hotel_name, loc, might_price)





