from unittest.mock import patch

import pytest
from scrapy.cmdline import execute


# tests/extensions/test_kingfisher_process_api.py fails if this test is run first.
@pytest.mark.order(-1)
@patch('scrapy.crawler.CrawlerProcess.crawl')
def test_command(crawl, caplog):
    with pytest.raises(SystemExit):
        execute(['scrapy', 'pluck', '--release-pointer', '/date'])

    assert len(crawl.mock_calls) > 0
    assert len(caplog.records) > 0
