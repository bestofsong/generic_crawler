from .choose_querier import choose_querier

def query(query_node, c):
    scope = query_node.get('scope', None)
    subq = query_node.get('query', None)
    is_multivar = query_node.get('multivar', False)

    if scope is None:
        raise ValueError('scope查询必须有scope字段')
    if subq is None:
        raise ValueError('scope查询必须有子查询')
    if is_multivar:
        raise ValueError('scope查询不支持多值')

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


