import re
from ..data_type.from_str import from_str

def query(query_node, c):
    xpath = query_node.get('xpath', None)
    field = query_node.get('field')
    scope = query_node.get('scope', None)

    ctx_data = c.ctx_data
    if scope is not None:
        ctx_data[scope] = dict()
        ctx_data = ctx_data[scope]

    node = c.ctx_node.xpath(xpath)[0] if xpath is not None else c.ctx_node
    if node is None:
        c.logger.error('xpath match none: %s' % xpath)
        return
    if field is None:
        c.logger.error('invalid attr node, missing field: %s' % query_node)
        return

    attributes = node.attrib()
    if attributes is None:
        return

    for k, _ in field.items():
        v = attributes.get(k, None)
        if v is None:
            continue
        field_def = field[k]
        path = field_def['path']
        type_ = field_def['type']
        matcher = field_def.get('matcher', None)
        if matcher is None:
            ctx_data[path] = from_str(v, type_)
        else:
            p = re.compile(matcher, re.MULTILINE | re.UNICODE)
            it = p.finditer(v)
            if it is None:
                continue
            res = []
            for m in it:
                groups = m.groups()
                if groups is None:
                    continue
                if len(groups) == 1:
                    res.append(from_str(groups[0], type_))
                else:
                    res.append([from_str(g, type_) for g in groups])
            if len(res) == 0:
                continue
            elif len(res) == 1:
                res = res[0]
            ctx_data[path] = res


