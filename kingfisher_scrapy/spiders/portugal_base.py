import scrapy
from twisted.internet import reactor, defer

from kingfisher_scrapy.base_spider import LinksSpider
from kingfisher_scrapy.util import parameters


class PortugalBase(LinksSpider):
    default_from_date = '2010-01-01'
    next_page_formatter = staticmethod(parameters('offset'))
    # The API return 429 error after a certain number of requests
    download_delay = 1

    number_of_retries = 0
    max_number_of_retries = 5
    wait_time = initial_wait_time = 60

    def start_requests(self):
        url = self.url
        if self.from_date and self.until_date:
            url = f'{url}&contractStartDate={self.from_date}&contractEndDate={self.until_date}'

        yield scrapy.Request(url, meta={'file_name': 'offset-1.json'})

    def retry(self, response, request):
        self.logger.info(f'Response status {response.status} waiting {self.wait_time} seconds before continue, '
                         f'attempt {self.number_of_retries}')
        d = defer.Deferred()
        reactor.callLater(self.wait_time, d.callback, request)
        self.number_of_retries += 1
        # if it fails again for the same request, we wait more
        self.wait_time *= 2
        return d

    def parse(self, response):
        # after a undefined number of requests (around 36100?), the API returns 5XX errors.
        # After waiting a few seconds the URL works again
        if not self.is_http_success(response):
            if self.number_of_retries < self.max_number_of_retries:
                self.retry(response, scrapy.Request(response.request.url, dont_filter=True, meta=response.request.meta))
            else:
                self.number_of_retries = 0
                self.wait_time = self.initial_wait_time
                self.logger.info(f'Response status {response.status}, maximum attempts reached, giving up')
                yield self.build_file_error_from_response(response)
        else:
            self.number_of_retries = 0
            self.wait_time = self.initial_wait_time
            yield from super().parse(response)
