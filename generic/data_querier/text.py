import re
from ..data_type.from_str import from_str

def query(query_node, c):
    xpath = query_node.get('xpath', None)
    matcher = query_node.get('matcher', None)
    field = query_node.get('field', None)
    is_multivar = query_node.get('multivar', False)
    scope = query_node.get('scope', None)
    merge = query_node.get('merge', None)
    separator = merge.get('separator', '') if merge is not None else ''

    if field is not None and not isinstance(field, list):
        field = [field]

    ctx_data = c.ctx_data
    if scope is not None:
        if ctx_data.get(scope, None) is not None:
            if is_multivar or field is not None:
                ctx_data = ctx_data[scope]
        elif is_multivar:
            ctx_data[scope] = []
            ctx_data = ctx_data[scope]
        elif field is None:
            ctx_data[scope] = ''
        else:
            ctx_data[scope] = dict()
            ctx_data = ctx_data[scope]

    node = c.ctx_node.xpath(xpath) if xpath is not None else c.ctx_node
    for n in node:
        value = n.get()
        # in this case new scope is supposed to exists
        if matcher is None:
            if is_multivar:
                ctx_data.append(value)
            else:
                # in this case new scope is supposed to exists
                if field is None:
                    if len(ctx_data[scope]) == 0:
                        ctx_data[scope] = value
                    else:
                        ctx_data[scope] += separator + value
                else:
                    prop = field[0]['path']
                    type_ = field[0]['type']
                    ctx_data[prop] = from_str(value, type_)
        else:
            p = re.compile(matcher, re.MULTILINE | re.UNICODE | re.IGNORECASE)
            it = p.finditer(value)
            for m in it:
                if field is None:
                    for subs in m.groups(None):
                        if subs is None:
                            continue
                        subs = subs.strip()
                        if len(subs) == 0:
                            continue
                        if is_multivar:
                            ctx_data.append(subs)
                        else:
                            if len(ctx_data[scope]) == 0:
                                ctx_data[scope] = subs
                            else:
                                ctx_data[scope] += separator + subs
                else:
                    obj = dict()
                    for ii, fld in enumerate(field):
                        prop = fld['path']
                        type_ = fld['type']
                        if type_ == 'boolean':
                            obj[prop] = True
                            continue
                        str_value = m.group(ii + 1)
                        if str_value is None:
                            continue
                        str_value = str_value.strip()
                        if len(str_value) == 0:
                            continue
                        value = from_str(str_value, type_)
                        obj[prop] = value
                    if is_multivar:
                        ctx_data.append(obj)
                    else:
                        ctx_data.update(obj)



