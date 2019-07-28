import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from myfarmSpider.items import DiseasesItem

class infoSpider(CrawlSpider):
    name = "crop_disease"
    '''https://plantdiseasehandbook.tamu.edu/food-crops/vegetable-crops
        https://www.planetnatural.com/tomato-gardening-guru/pests-disease/
    '''
    start_urls = ['https://plantdiseasehandbook.tamu.edu/food-crops/']
    allowed_domains = ['plantdiseasehandbook.tamu.edu']
    rules = [
                Rule(
                    LinkExtractor(
                        canonicalize=True,
                        unique=True,
                        #deny=("http://www.google.com/")
                    ),
                    follow=True,
                    #cb_kwargs={'keyword': word},
                    callback="parse_items"
                )
            ]

    '''def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                    url,
                    callback=self.parse,
                    dont_filter=True
                )'''
    
    def parse_items(self, response):
        items = []
        crop_name = response.xpath('//h1[@class="entry-title"]/text()').extract()
        crop_disease = response.xpath('//div[@class="entry-content"]/div[@class="pf-content"]/p')
        for crop in crop_disease:
            item = DiseasesItem()
            disease_name = crop.xpath('strong/text()').extract()
            disease_details = crop.xpath('strong/following-sibling::text()').extract()
            item['crop_name'] = crop_name
            item['disease_name'] = disease_name
            item['signs_and_symptoms'] = disease_details
            # item['control'] = 'control'
            items.append(item)
            items = list(dict.fromkeys(items)) 
        
        crop_diseases_on_null = response.xpath('//div[@class="entry-content"]/div[@class="pf-content"]/table')
        for crop in crop_diseases_on_null:
            item = DiseasesItem()
            disease_name = crop.xpath('preceding-sibling::p[1]/strong/span/text()').extract()
            disease_details = crop.xpath('tbody/tr[3]/td[last()]/p/span/text()').extract()
            item['crop_name'] = crop_name
            item['disease_name'] = disease_name
            item['signs_and_symptoms'] = disease_details
            # item['control'] = 'control'
            items.append(item)
            items = list(dict.fromkeys(items)) 
        return items
