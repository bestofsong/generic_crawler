import scrapy
import os
import json
from ruamel.yaml import YAML
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

        conf_file = getattr(self, 'conf', None)
        if conf_file is None:
            raise ValueError('Missing spider arg - conf(config file). Pass that using: -a url=xxxxxxx')

        with open(conf_file, 'r') as conf_file_handle:
            _name, ext = os.path.splitext(conf_file)
            if ext == '.yml' or ext == '.yaml':
                yaml = YAML(typ='safe')
                self.config_data = yaml.load(conf_file_handle)
                with open('compare.yml', 'w') as fff:
                    yaml.dump(self.config_data, fff)
            else:
                self.config_data = json.load(conf_file_handle)

        discover = self.config_data.get('discover', None)
        if discover is None or discover.get('start', None) is None:
            if getattr(self, 'url', None) is None:
                raise ValueError('No seed url, pass -a url=xxx or add discover: { type, start, next }')
            discover = discover if discover is not None else {'type': 'list'}
            discover['start'] = self.url
            self.config_data['discover'] = discover
        if self.config_data['discover'].get('type', None) is None:
            raise ValueError('discover.type cannot be None')

    def start_requests(self):
        url = getattr(self, 'url', None)
        if url is None:
            url = self.config_data['discover']['start']
        yield scrapy.Request(url, callback=self.parse,
                             errback=self.errback_httpbin)

    def parse(self, response):
        # self.logger.info('Got successful response from {}'.format(response.url))
        link = self.config_data['link']
        q = self.config_data['query']
        ctx = query_ctx.Ctx(ctx_node=response, logger=self.logger, resp=response)
        query_res = root_query.query(q, ctx)
        for item in query_res:
            yield item

        if getattr(self, 'nofollow', None) == 'true':
            return
        if link is None:
            return
        follow_url = response.xpath(link).get()
        if follow_url is not None and not isinstance(follow_url, str):
            raise ValueError('下一页链接查询失败: %s' % follow_url)
        if follow_url is not None and len(follow_url) > 0:
            yield response.follow(url=follow_url, callback=self.parse, priority=-1)

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
