from . import text, attr, comp, link

def get_querier(type):
    if type == 'text':
        return text
    elif type == 'attr':
        return attr
    elif type == 'comp':
        return comp
    elif type == 'link':
        return link
    else:
        raise ValueError('get_querier type')