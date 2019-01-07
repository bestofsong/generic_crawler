class Ctx:
    def __init__(self, root_data = None, ctx_path = '', ctx_node = None, query_count = 0):
        self.root_data = root_data
        self.ctx_path = ctx_path
        self.ctx_node = ctx_node
        self.query_count = query_count

    @property
    def ctx_data(self):
        pass