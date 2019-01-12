import re

def extract_text(t = '', match_start = None, match_end = None):
    if match_start is None and match_end is None:
        return t

    if match_start is not None:
        p1 = re.compile(match_start['matcher'], re.I | re.S)
        m1 = p1.search(t)
        if m1 is None or (m1.start() < 0 and match_start.get('required', False)):
            return ''
        left_include = match_start.get('include', True)
        left_index = m1.start() if left_include else m1.end()
    if match_end is not None:
        p2 = re.compile(match_end['matcher'], re.I | re.S)
        m2 = p2.search(t)
        if m2 is None or (m2.start() < 0 and match_end.get('required', False)):
            return ''
        right_include = match_end.get('include', True)
        right_index = m2.end() if right_include else m2.start()

    if match_start is None:
        return t[:right_index]
    elif match_end is None:
        return t[left_index:]
    else:
        return t[left_index:right_index]

