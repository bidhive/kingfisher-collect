import scrapy

from kingfisher_scrapy.base_spider import LinksSpider
from kingfisher_scrapy.util import parameters


class GeorgiaReleases(LinksSpider):
    """
    Swagger API documentation
      https://odapi.spa.ge/api/swagger.ui
    """
    name = 'georgia_releases'
    data_type = 'release_package'
    next_page_formatter = staticmethod(parameters('page'))

    def start_requests(self):
        url = 'https://odapi.spa.ge/api/releases.json'
        yield scrapy.Request(url, meta={'file_name': 'page-1.json'})
