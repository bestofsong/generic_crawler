from .ctx import Qc
from .comp import query as comp_query

def query(query_node, c):
    type_ = query_node['type']
    if type_ != 'comp':
        raise ValueError('0级查询必须是comp类型')
    xpath = query_node['xpath']

    nodes = c.ctx_node.xpath(xpath)
    print('post count: %d' % len(nodes))
    for ii, n in enumerate(nodes):
        print(' post: %d' % ii)
        if ii == 1:
            print('stop processing')
            break
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
        print(qc)
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
        elif qc.val > 0:
            print('query_counter: %d > 0, meaning subquery is ongoing...' % qc.val)
            qc.unlock()
        else:
            print('query_counter: %d < 0, meaning subquery already finished, rarely happens...' % qc.val)
            qc.unlock()

