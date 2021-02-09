import pytest
from scrapy import Request
from scrapy.core.downloader import DownloaderMiddlewareManager
from twisted.internet.defer import Deferred
from twisted.trial.unittest import TestCase

from kingfisher_scrapy.middlewares import DelayedRequestMiddleware
from tests import spider_with_crawler


@pytest.mark.parametrize('meta', [
    None,
    {'wait_time': 1}
])
def test_middleware_output(meta):
    spider = spider_with_crawler()
    delay_middleware = DelayedRequestMiddleware()
    request = Request(f'http://example.com', meta=meta)
    returned_request = delay_middleware.process_request(request, spider)
    if not meta:
        assert returned_request is None
    else:
        assert isinstance(returned_request, Deferred)


def test_middleware_wait():

    def mock_download_func(spider, request):
        return request

    spider = spider_with_crawler()
    downloader_manager = DownloaderMiddlewareManager.from_crawler(spider.crawler)
    request = Request('http://example.com', meta={'wait_time': 1})
    # we send the request to all the download middlewares including the delayed one
    downloaded = downloader_manager.download(mock_download_func, request, spider)
    assert isinstance(downloaded, Deferred)
    # https://github.com/scrapy/scrapy/blob/28262d4b241744aa7c090702db9a89411e3bbf9a/tests/test_downloadermiddleware.py#L36
    results = []
    downloaded.addBoth(results.append)
    test = TestCase()
    test._wait(downloaded)
    returned_request = results[0]
    assert returned_request.url == request.url