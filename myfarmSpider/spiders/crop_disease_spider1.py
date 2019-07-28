import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from myfarmSpider.items import DiseasesItem

class infoSpider(CrawlSpider):
    name = "crop_disease1"
    start_urls = ['https://www.apsnet.org/edcenter/foreducators/Pages/Plant-Disease-Lessons.aspx']
    allowed_domains = ['www.apsnet.org']
    rules = [
                Rule(
                    LinkExtractor(
                        canonicalize=True,
                        unique=True,
                        deny=("https://www.apsnet.org/members/",'https://www.apsnet.org/meetings/',
                            'https://apsjournals.apsnet.org/','https://www.apsnet.org/careers/',
                            'https://www.apsnet.org/edcenter/disimpactmngmnt/','https://www.apsnet.org/edcenter/foreducators/',
                            'https://www.apsnet.org/edcenter/resources/','https://www.apsnet.org/About/',
                            'https://my.apsnet.org/APS/','https://www.apsnet.org/Pages/','https://www.apsnet.org/apsstore/',
                            'https://www.apsnet.org/online/'
                        ),
                        allow=('https://www.apsnet.org/edcenter/disandpath/fungalasco/pdlessons/Pages/Anthracnoseofturfgrass.aspx',
                            'https://www.apsnet.org/edcenter/disandpath/fungalasco/pdlessons/Pages/ApplePowderyMildew.aspx',
                            'https://www.apsnet.org/edcenter/disandpath/fungalasco/pdlessons/Pages/BlackKnot.aspx'
                        )
                    ),
                    follow=True,
                    callback="parse_items"
                )
            ]
    
    def parse_items(self, response):
        items = []
        content = response.xpath("//div[@data-name='ContentPlaceHolderMain']")
        for data in content:
            item = DiseasesItem()
            disease_name = data.xpath("span/div/strong[1]/text()").extract()
            crop_name = data.xpath("span/div/strong[last()]/text()").extract()
            signs_and_symptoms = data.xpath("span/div/p[count(preceding::h2) = 1]/text()").extract()
            control = data.xpath("span/div/p[preceding::h2[4]][position()<4]/text()").extract()
            item['crop_name'] = crop_name
            item['disease_name'] = disease_name
            item['signs_and_symptoms'] = signs_and_symptoms
            item['control'] = control
            items.append(item)
            items = list(dict.fromkeys(items))
        return items
