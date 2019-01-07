def query(query_node, c):
    xpath = query_node['xpath']
    matcher = query_node['matcher']
    field = query_node['field']
    multivar = query_node.get('multivar', None)
    name = query_node.get('name', None)
    merge = query_node.get('merge', None)

    node = c.ctx_node.xpath(xpath)
    if multivar is None or len(multivar) == 0:
        node = node[0]


