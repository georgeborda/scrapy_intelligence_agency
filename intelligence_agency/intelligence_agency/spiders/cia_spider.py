import scrapy

XPATH_LINKS_DESCLASSIFIED = '//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href'
XPATH_TITLE = '//h1[@class = "documentFirstHeading"]/text()'
XPATH_BODY = '//div[@class = "field-item even"]//p[not(child::strong and child::i) and not(@class)]/text()'

class CiaSpider(scrapy.Spider):
    
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections'
    ]

    custom_settings = {
        'FEEDS': {
            'cia.json' : {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True
            }
        }
    }


    def parse(self, response):
        links_desclassified = response.xpath(XPATH_LINKS_DESCLASSIFIED).getall()
        # Obtiene las url relativas

        for link in links_desclassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})
            # response.urljoin une la url absoluta con la url relativa que se encuentra en link


    def parse_link(self, response, **kwargs):
        link = kwargs['url']  # url absoluta + relativa
        title = response.xpath(XPATH_TITLE).get() 
        paragraph = ''.join(response.xpath(XPATH_BODY).getall())

        yield {
            'url': link,
            'title': title,
            'paragraph': paragraph
        }