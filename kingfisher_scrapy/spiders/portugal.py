import json

import scrapy

from kingfisher_scrapy.base_spider import ZipSpider
from kingfisher_scrapy.util import components, handle_error


class Portugal(ZipSpider):
    name = 'portugal'
    data_type = 'record_package'
    encoding = 'iso-8859-1'
    zip_file_format = 'json_lines'

    download_warnsize = 0
    download_timeout = 9999

    def start_requests(self):
        # A CKAN API JSON response.
        url = 'https://dados.gov.pt/api/1/datasets/?q=ocds&organization=5ae97fa2c8d8c915d5faa3bf&page_size=20'
        yield scrapy.Request(url, meta={'kf_filename': 'page-1.json'}, callback=self.parse_list)

    @handle_error
    def parse_list(self, response):
        data = json.loads(response.text)
        for item in data['data']:
            for resource in item['resources']:
                description = resource['description']
                if description and 'ocds' in description.lower():
                    # Presently, only one URL matches.
                    yield self.build_request(resource['url'], formatter=components(-2))
