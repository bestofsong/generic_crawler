import scrapy
from .comp import query as comp_query

def query(query_node, c):
    xpath = query_node['xpath']
    subq = query_node.get('query', [])

    ctx_node = c.ctx_node
    qc = c.qc
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

    yield scrapy.Request(abs_link, link_request_parser)

