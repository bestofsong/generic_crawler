from scrapy.utils.response import get_base_url
from .ctx import Qc
from .comp import query as comp_query

def query(query_node, c):
    type_ = query_node['type']
    if type_ != 'comp':
        raise ValueError('0级查询必须是comp类型')
    xpath = query_node['xpath']

    nodes = c.ctx_node.xpath(xpath)
    page = get_base_url(c.resp)
    c.logger.info('page: %s' % page)
    for ii, n in enumerate(nodes):
        cc = c.dup()
        qc = Qc(0)
        cc.query_counter = qc
        d = dict()
        cc.ctx_data = d
        cc.root_data = d
        cc.ctx_node = n
        qn = dict()
        qn.update(query_node)
        qn['xpath'] = '.'
        res = comp_query(qn, cc)
        if res is None:
            return
        for item in res:
            yield item

        # 没有子查询或子查询已经完成
        qc.lock()
        if qc.val == 0:
            qc.val = -1
            qc.unlock()
            yield d
        else:
            qc.unlock()
