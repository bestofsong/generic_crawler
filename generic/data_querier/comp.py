from .ctx import Ctx, Qc
from .choose_querier import choose_querier

def query(query_node, c):
    xpath = query_node['xpath']
    subq = query_node.get('query', [])
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
        ctx.root_data = d
        ctx.ctx_data = d
        ctx.ctx_node = node
        ctx.query_counter = Qc(0)

        for qn in subq:
            t = qn['type']
            ret = choose_querier(t).query(qn, ctx)

            # 可以是子查询的request或子查询都完成之后的item
            if ret is not None:
                for item in ret:
                    yield item

        # 没有子查询或子查询已经完成
        qc = ctx.query_counter
        qc.lock()
        if qc.val == 0:
            qc.val = -1
            qc.unlock()
            yield ctx.root_data
        elif qc.val > 0:
            print('query_counter: %d > 0, meaning subquery is ongoing...' % qc.val)
            qc.unlock()
        else:
            print('query_counter: %d < 0, meaning subquery already finished, rarely happens...' % qc.val)
            qc.unlock()
