from .choose_querier import choose_querier

def query(query_node, c):
    xpath = query_node['xpath']
    subq = query_node.get('query', [])
    if not isinstance(subq, list):
        subq = [subq]
    is_multivar = query_node.get('multivar', False)
    scope = query_node.get('scope', None)

    ctx_data = c.ctx_data
    if scope is not None:
        ctx_data[scope] = [] if is_multivar else dict()
        ctx_data = ctx_data[scope]

    ctx_node = c.ctx_node
    matched_nodes = ctx_node.xpath(xpath)

    for node in matched_nodes:
        d = dict() if is_multivar else ctx_data
        if is_multivar:
            ctx_data.append(d)

        ctx = c.dup()
        ctx.ctx_data = d
        ctx.ctx_node = node

        for qn in subq:
            t = qn['type']
            ret = choose_querier(t).query(qn, ctx)

            if ret is None:
                continue
            # 可以是子查询的request或子查询都完成之后的item
            for item in ret:
                yield item
