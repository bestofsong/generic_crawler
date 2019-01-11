from .ctx import Qc
from .comp import query as comp_query

def query(query_node, c):
    type = query_node['type']
    if type != 'comp':
        raise RuntimeError('根节点必须是comp类型')

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

