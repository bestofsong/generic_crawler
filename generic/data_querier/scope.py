from .ctx import Ctx
from .choose_querier import choose_querier

def query(query_node, c):
    scope = query_node.get('scope')
    subq = query_node.get('query')
    if not isinstance(subq, list):
        subq = [subq]

    ctx_data = c.ctx_data
    ctx_data[scope] = dict()

    cc = c.dup()
    cc.ctx_data = ctx_data[scope]

    for q in subq:
        querier = choose_querier(q['type'])
        res = querier.query(q, cc)
        if res is not None:
            for item in res:
                yield item


