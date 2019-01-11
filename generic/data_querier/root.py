from .ctx import Qc
from .comp import query as comp_query

def query(query_node, c):
    type_ = query_node['type']

    cc = c.dup()
    qc = Qc(0)
    cc.query_counter = qc
    d = dict()
    cc.ctx_data = d
    cc.root_data = d

    res = comp_query(query_node, cc)
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

