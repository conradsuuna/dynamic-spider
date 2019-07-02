import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

#scrapy crawl article -o articles.json -t json/csv/xml
class infoSpider(scrapy.Spider):
    name = "jk"
    start_urls = [
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=535E52&9=515E5A5F',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=5C5D5C5B5A5958242D&9=515E5A5E',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=5F5C&9=515E5A5D',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=5C5D5C5B5A5958242D&9=515E5A5C',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=535E51&9=515E5A5B',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=545E&9=515E5A5A',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=535E52&9=515E5A59',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=535E52&9=515E5A58',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=5D5A51&9=515E5A27',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=525D5827&9=515E5950',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=525E585A&9=515E595F',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=5E515F&9=515E595E',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=52525E5F&9=515D5150',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=525D5B5B&9=515D515E',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=525C5B5C&9=515D515D',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=5F5A50&9=515D515A',
        'https://abri.une.edu.au/online/cgi-bin/i4.dll?1=2C2D352E&2=2820&3=56&5=2B3C2B3C3A&7=5F5F5A&9=515D5159',
    ]

    def parse(self, response):
        for link in response.xpath('//table[@id="MemberDetails"]'):
            name = link.xpath('tr/td[.//strong]/strong[contains(text(),"Membership Name")]/parent::td/following-sibling::td/text()').extract()
            for new_name in name:
                new_name = new_name.replace('\r\n','')
            yield{
                'name':new_name,
                'email':link.xpath('tr/td/a[contains(@href, "@")]/text()').extract()
            }

        next_button = response.xpath('//table[@class="PageHead"]/tr/td/a')
        for button in next_button:
            if button.xpath('text()').get() == 'Next':
                next_page = button.xpath('@href').get()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)
