import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from myfarmSpider.items import MyfarmspiderItem

#scrapy crawl article -o articles.json -t json/csv/xml
keywords = ['crop diseases']
class infoSpider(CrawlSpider):
    name = "find_disease"
    start_urls = []

    for word in keywords: 
        url = "http://www.google.com/search?q="+word+"&num=10&hl=en&start=0&sa=N"
        #url = 'https://extension.psu.edu/catalogsearch/result/?'
        start_urls.append(url) 
        #start_urls = ['http://agriculture.vic.gov.au/agriculture/pests-diseases-and-weeds/animal-diseases/beef-and-dairy-cows',]
        rules = [
                Rule(
                    LinkExtractor(
                        canonicalize=True,
                        unique=True,
                        #deny=("http://www.google.com/")
                    ),
                    follow=True,
                    cb_kwargs={'keyword': word},
                    callback="parse_items"
                )
            ]
   
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                    url,
                    callback=self.parse,
                    dont_filter=True
                )

    def parse_items(self, response, keyword):
        items = []

        #item = MyfarmspiderItem()
        #item['all_data'] = set(response.xpath('body//p/text()').extract())
        #item['all_data'] = set(response.xpath('//title/text()').extract())
        #items.append(item)
        #items = list(dict.fromkeys(items))

        '''# Checks if there is a next page link, and keeping parsing if True    
        next_page = response.xpath('(//a[contains(., "Next")])[1]/@href').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)'''
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        for link in links:
            item = MyfarmspiderItem()
            #item['internal_url'] = response.url#url_from
            item['internal_url'] = link.url
            item['all_data'] = set(response.xpath('//title/text()').extract())
            items.append(item)
            items = list(dict.fromkeys(items))
        return items
    