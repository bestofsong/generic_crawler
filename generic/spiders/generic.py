import scrapy
import json
from ..data_querier import \
    root as root_query, \
    ctx as query_ctx

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class GenericSpider(scrapy.Spider):
    name = "generic"

    def __init__(self, name = None, **kwargs):
        scrapy.Spider.__init__(self, name, **kwargs)

        if getattr(self, 'url', None) is None:
            raise ValueError('Missing spider arg - url(starting page url). Pass that using: -a conf=xxxxxxx')
        if getattr(self, 'conf', None) is None:
            raise ValueError('Missing spider arg - conf(config file). Pass that using: -a url=xxxxxxx')

        with open(self.conf, 'r') as f:
            self.config_data = json.load(f)

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse,
                             errback=self.errback_httpbin)

    def parse(self, response):
        # self.logger.info('Got successful response from {}'.format(response.url))
        link = self.config_data['link']
        q = self.config_data['query']
        ctx = query_ctx.Ctx(ctx_node=response, logger=self.logger, resp=response)
        query_res = root_query.query(q, ctx)
        for item in query_res:
            yield item

        follow_url = response.xpath(link).get()
        if follow_url is not None and not isinstance(follow_url, str):
            raise ValueError('下一页链接查询失败: %s' % follow_url)
        if follow_url is not None and len(follow_url) > 0:
            yield response.follow(follow_url, self.parse)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)