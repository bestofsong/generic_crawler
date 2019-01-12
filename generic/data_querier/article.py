from .choose_querier import choose_querier
from .utils import extract_text

def query(query_node, c):
    xpath = query_node.get('xpath', None)
    query = query_node.get('query')

    node = c.ctx_node.xpath(xpath) if xpath is not None else c.ctx_node
    article = ''
    for n in node:
        value = n.get()
        if len(article) > 0:
            article += '\n'
        article += value

    class ArticleNode:
        def __init__(self, a):
            self._a = a
            self.has_value = True

        def get(self):
            return self._a

        def __iter__(self):
            return ArticleNode(self._a)

        def __next__(self):
            if not self.has_value:
                raise StopIteration
            self.has_value = False
            return self

    if not isinstance(query, list):
        query = [query]

    for q in query:
        real_article = extract_text(
            article,
            q.get('match_start', None),
            q.get('match_end', None)
        )
        an = ArticleNode(real_article)
        cc = c.dup()
        cc.ctx_node = an
        querier = choose_querier(q['type'])
        res = querier.query(q, cc)
        if res is not None:
            for item in res:
                yield item

