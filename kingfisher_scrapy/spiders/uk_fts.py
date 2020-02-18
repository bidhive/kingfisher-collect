import hashlib
import json

import scrapy

from kingfisher_scrapy.base_spider import BaseSpider


class UKContractsFinder(BaseSpider):
    name = 'uk_fts'

    def start_requests(self):
        yield scrapy.Request(
            # This URL was provided by the publisher and is not the production URL.
            url='https://enoticetest.service.xgov.uk/api/1.0/ocdsReleasePackages',
            meta={'kf_filename': 'start.json'},
            headers={'Accept': 'application/json'},
        )

    def parse(self, response):

        if response.status == 200:

            yield self.save_response_to_disk(
                response,
                response.request.meta['kf_filename'],
                data_type='release_package_in_ocdsReleasePackage_in_list_in_results'
            )

            json_data = json.loads(response.text)
            if not self.sample and json_data['nextCursor']:
                yield scrapy.Request(
                    url="https://enoticetest.service.xgov.uk/api/1.0/ocdsReleasePackages?cursor=" + json_data['nextCursor'],
                    meta={'kf_filename': hashlib.md5(json_data['nextCursor'].encode('utf-8')).hexdigest() + '.json'},
                    headers={'Accept': 'application/json'}
                )
        else:
            yield {
                'success': False,
                'file_name': response.request.meta['kf_filename'],
                'url': response.request.url,
                'errors': {'http_code': response.status}
            }