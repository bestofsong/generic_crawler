from .ctx import Ctx
from .get_querier import get_querier

def query(query_node, c):
    # todo: wansong, use mutex in case multiple subquery happen concurrently
    type = query_node['type']
    xpath = query_node['xpath']
    q = query_node.get('query', [])

    ctx_node = c.ctx_node
    matched_nodes = ctx_node.xpath(xpath)
    for node in matched_nodes:
        ctx = Ctx(root_data=dict(), ctx_path='/', ctx_node=node)
        if type == 'attr':
            raise ValueError('todo')
        elif type == 'link':
            raise ValueError('todo')
        elif type == 'text':
            raise ValueError('todo')
        elif type == 'comp':
            pass
        else:
            raise ValueError('invalid query node type: %s' % type)

        for qn in q:
            t = qn['type']
            ret = get_querier(t).query(qn, ctx)

            # 可以是子查询的request或子查询都完成之后的item
            if ret is not None:
                for item in ret:
                    yield item

            # 没有子查询或子查询已经完成
            if ctx.query_count == 0:
                ctx.query_count = -1
                yield ctx.root_data
            elif ctx.query_count > 0:
                print('query_count: %d > 0, meaning subquery is ongoing...')
            else:
                print('query_count: %d < 0, meaning subquery already finished, rarely happens...')




