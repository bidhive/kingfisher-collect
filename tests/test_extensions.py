from unittest.mock import Mock, patch

import pytest
from scrapy.exceptions import NotConfigured

from kingfisher_scrapy.extensions import KingfisherAPI
from tests import spider_with_crawler


def spider_after_open(tmpdir, **kwargs):
    spider = spider_with_crawler(**kwargs)
    spider.crawler.settings['FILES_STORE'] = tmpdir
    spider.crawler.settings['KINGFISHER_API_URI'] = 'http://httpbin.org/anything'
    spider.crawler.settings['KINGFISHER_API_KEY'] = 'xxx'

    return spider


def test_from_crawler():
    spider = spider_with_crawler()
    spider.crawler.settings['KINGFISHER_API_URI'] = 'http://httpbin.org/anything'
    spider.crawler.settings['KINGFISHER_API_KEY'] = 'xxx'
    spider.crawler.settings['KINGFISHER_API_LOCAL_DIRECTORY'] = 'data'

    extension = KingfisherAPI.from_crawler(spider.crawler)

    assert extension.directory == 'data'


@pytest.mark.parametrize('api_url,api_key', [
    (None, None),
    ('http://httpbin.org/anything', None),
    (None, 'xxx'),
])
def test_from_crawler_missing_arguments(api_url, api_key):
    spider = spider_with_crawler()
    spider.crawler.settings['KINGFISHER_API_URI'] = api_url
    spider.crawler.settings['KINGFISHER_API_KEY'] = api_key

    with pytest.raises(NotConfigured) as excinfo:
        KingfisherAPI.from_crawler(spider.crawler)

    assert str(excinfo.value) == 'KINGFISHER_API_URI and/or KINGFISHER_API_KEY is not set.'


@pytest.mark.parametrize('sample,is_sample,path', [
    (None, False, 'test/20010203_040506/file.json'),
    ('true', True, 'test_sample/20010203_040506/file.json'),
])
@pytest.mark.parametrize('note', ['', 'Started by NAME.'])
@pytest.mark.parametrize('encoding,encoding2', [(None, 'utf-8'), ('iso-8859-1', 'iso-8859-1')])
@pytest.mark.parametrize('directory', [False, True])
@pytest.mark.parametrize('ok', [True, False])
def test_item_scraped_file(sample, is_sample, path, note, encoding, encoding2, directory, ok, tmpdir, caplog):
    spider = spider_after_open(tmpdir, sample=sample, note=note)

    if directory:
        spider.crawler.settings['KINGFISHER_API_LOCAL_DIRECTORY'] = str(tmpdir.join('xxx'))

    extension = KingfisherAPI.from_crawler(spider.crawler)
    spider.save_data_to_disk(b'{"key": "value"}', 'file.json', url='https://example.com/remote.json')

    with patch('requests.post') as mocked:
        response = Mock()
        response.ok = ok
        response.status_code = 400
        mocked.return_value = response

        data = {
            'success': True,
            'file_name': 'file.json',
            'url': 'https://example.com/remote.json',
            # Specific to this test case.
            'data_type': 'release_package',
        }
        if encoding:
            data['encoding'] = encoding

        extension.item_scraped(data, spider)

        if not ok:
            message = 'Failed to post [https://example.com/remote.json]. API status code: 400'

            assert len(caplog.records) == 1
            assert caplog.records[0].name == 'test'
            assert caplog.records[0].levelname == 'WARNING'
            assert caplog.records[0].message == message

        expected = {
            'collection_source': 'test',
            'collection_data_version': '2001-02-03 04:05:06',
            'collection_sample': is_sample,
            'file_name': 'file.json',
            'url': 'https://example.com/remote.json',
            # Specific to this test case.
            'data_type': 'release_package',
            'encoding': encoding2,
        }
        if note:
            expected['collection_note'] = note
        if directory:
            expected['local_file_name'] = tmpdir.join('xxx', path)

        with open(tmpdir.join(path), 'rb') as f:
            assert mocked.call_count == 1
            assert mocked.call_args[0] == ('http://httpbin.org/anything/api/v1/submit/file/',)
            assert mocked.call_args[1]['headers'] == {'Authorization': 'ApiKey xxx'}
            assert mocked.call_args[1]['data'] == expected
            assert len(mocked.call_args[1]) == 3

            if directory:
                assert mocked.call_args[1]['files'] == {}
            else:
                assert len(mocked.call_args[1]['files']) == 1
                assert len(mocked.call_args[1]['files']['file']) == 3
                assert mocked.call_args[1]['files']['file'][0] == 'file.json'
                assert mocked.call_args[1]['files']['file'][1].read() == f.read()
                assert mocked.call_args[1]['files']['file'][2] == 'application/json'


@pytest.mark.parametrize('sample,is_sample', [(None, False), ('true', True)])
@pytest.mark.parametrize('note', ['', 'Started by NAME.'])
@pytest.mark.parametrize('encoding,encoding2', [(None, 'utf-8'), ('iso-8859-1', 'iso-8859-1')])
@pytest.mark.parametrize('ok', [True, False])
def test_item_scraped_file_item(sample, is_sample, note, encoding, encoding2, ok, tmpdir, caplog):
    spider = spider_after_open(tmpdir, sample=sample, note=note)

    extension = KingfisherAPI.from_crawler(spider.crawler)

    with patch('requests.post') as mocked:
        response = Mock()
        response.ok = ok
        response.status_code = 400
        mocked.return_value = response

        data = {
            'success': True,
            'file_name': 'file.json',
            'url': 'https://example.com/remote.json',
            # Specific to this test case.
            'data_type': 'release_package',
            'number': 1,
            'data': b'{"key": "value"}',
        }
        if encoding:
            data['encoding'] = encoding

        extension.item_scraped(data, spider)

        if not ok:
            message = 'Failed to post [https://example.com/remote.json]. API status code: 400'

            assert len(caplog.records) == 1
            assert caplog.records[0].name == 'test'
            assert caplog.records[0].levelname == 'WARNING'
            assert caplog.records[0].message == message

        expected = {
            'collection_source': 'test',
            'collection_data_version': '2001-02-03 04:05:06',
            'collection_sample': is_sample,
            'file_name': 'file.json',
            'url': 'https://example.com/remote.json',
            # Specific to this test case.
            'data_type': 'release_package',
            'encoding': encoding2,
            'number': 1,
            'data': b'{"key": "value"}',
        }
        if note:
            expected['collection_note'] = note

        mocked.assert_called_once_with(
            'http://httpbin.org/anything/api/v1/submit/item/',
            headers={
                'Authorization': 'ApiKey xxx',
            },
            data=expected,
        )


@pytest.mark.parametrize('sample,is_sample', [(None, False), ('true', True)])
@pytest.mark.parametrize('ok', [True, False])
def test_item_scraped_file_error(sample, is_sample, ok, tmpdir, caplog):
    spider = spider_after_open(tmpdir, sample=sample)

    extension = KingfisherAPI.from_crawler(spider.crawler)

    with patch('requests.post') as mocked:
        response = Mock()
        response.ok = ok
        response.status_code = 400
        mocked.return_value = response

        data = {
            'success': False,
            'file_name': 'file.json',
            'url': 'https://example.com/remote.json',
            # Specific to this test case.
            'errors': {'http_code': 500},
        }

        extension.item_scraped(data, spider)

        if not ok:
            message = 'Failed to post [https://example.com/remote.json]. File Errors API status code: 400'

            assert len(caplog.records) == 1
            assert caplog.records[0].name == 'test'
            assert caplog.records[0].levelname == 'WARNING'
            assert caplog.records[0].message == message

        expected = {
            'collection_source': 'test',
            'collection_data_version': '2001-02-03 04:05:06',
            'collection_sample': is_sample,
            'file_name': 'file.json',
            'url': 'https://example.com/remote.json',
            # Specific to this test case.
            'errors': '{"http_code": 500}',
        }

        mocked.assert_called_once_with(
            'http://httpbin.org/anything/api/v1/submit/file_errors/',
            headers={
                'Authorization': 'ApiKey xxx',
            },
            data=expected,
        )


@pytest.mark.parametrize('sample,is_sample', [(None, False), ('true', True)])
@pytest.mark.parametrize('ok', [True, False])
def test_spider_closed(sample, is_sample, ok, tmpdir, caplog):
    spider = spider_after_open(tmpdir, sample=sample)

    extension = KingfisherAPI.from_crawler(spider.crawler)

    with patch('requests.post') as mocked:
        response = Mock()
        response.ok = ok
        response.status_code = 400
        mocked.return_value = response

        extension.spider_closed(spider, 'finished')

        mocked.assert_called_once_with(
            'http://httpbin.org/anything/api/v1/submit/end_collection_store/',
            headers={
                'Authorization': 'ApiKey xxx',
            },
            data={
                'collection_source': 'test',
                'collection_data_version': '2001-02-03 04:05:06',
                'collection_sample': is_sample,
            },
        )

        if not ok:
            assert len(caplog.records) == 1
            assert caplog.records[0].name == 'test'
            assert caplog.records[0].levelname == 'WARNING'
            assert caplog.records[0].message == 'Failed to post End Collection Store. API status code: 400'


def test_spider_closed_other_reason(tmpdir):
    spider = spider_after_open(tmpdir)

    extension = KingfisherAPI.from_crawler(spider.crawler)

    with patch('requests.post') as mocked:
        extension.spider_closed(spider, 'xxx')

        mocked.assert_not_called()
