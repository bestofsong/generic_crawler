import scrapy
from .comp import query as comp_query
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


def query(query_node, c):
    xpath = query_node['xpath']
    subq = query_node.get('query', [])

    ctx_node = c.ctx_node
    qc = c.query_counter
    resp = c.resp
    root_data = c.root_data

    link_nodes = ctx_node.xpath(xpath)
    if len(link_nodes) == 0:
        return
    link = link_nodes[0].get()
    if len(link) <= 0:
        raise ValueError('failed to extract link')
    abs_link = resp.urljoin(link)

    def link_request_parser(next_resp):
        cc = c.dup()
        cc.resp = next_resp
        cc.ctx_node = next_resp

        q = { 'type': 'comp', 'query': subq, 'xpath': '.' }
        res = comp_query(q, cc)
        if res is not None:
            for it in res:
                yield it

        qc.lock()
        qc.val -= 1
        if qc.val == 0:
            qc.val = -1
            qc.unlock()
            yield root_data
        elif qc.val > 0:
            print('query_counter: %d > 0, meaning subquery is ongoing...' % qc.val)
            qc.unlock()
        else:
            print('query_counter: %d < 0, meaning subquery already finished, rarely happens...' % qc.val)
            qc.unlock()

    qc.lock()
    qc.val += 1
    qc.unlock()

    def errback_http(failure):
        # log all failures
        qc.lock()
        qc.val -= 1
        qc.unlock()

        c.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            c.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            c.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            c.logger.error('TimeoutError on %s', request.url)

    c.logger.info('spawning new request: %s', abs_link)
    yield scrapy.Request(url=abs_link, callback=link_request_parser, errback=errback_http)

