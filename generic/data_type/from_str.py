def from_str(s, t):
    if s is not None and (t == 'text' or t == 'keyword'):
        return str(s)
    elif s is not None and t == 'number':
        return int(s)
    elif s is not None and (t == 'float' or t == 'double'):
        return float(s)
    elif t == 'boolean':
        return True if s else False
    else:
        return s