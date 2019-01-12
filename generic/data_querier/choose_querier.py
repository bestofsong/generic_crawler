def choose_querier(type):
    from . import text, attr, comp, link, scope, article

    if type == 'text':
        return text
    elif type == 'attr':
        return attr
    elif type == 'comp':
        return comp
    elif type == 'link':
        return link
    elif type == 'scope':
        return scope
    elif type == 'article':
        return article
    else:
        raise ValueError('get_querier type')