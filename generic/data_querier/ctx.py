class Ctx:
    def __init__(self,
                 root_data = None,
                 ctx_data = None,
                 ctx_node = None,
                 query_counter = None,
                 logger = None,
                 resp = None):
        self.root_data = root_data
        self.ctx_data = ctx_data
        self.ctx_node = ctx_node
        self.query_counter = query_counter
        self.logger = logger
        self.resp = resp

    def dup(self):
        ret = Ctx(root_data=self.root_data,
                  ctx_data=self.ctx_data,
                  ctx_node=self.ctx_node,
                  query_counter=self.query_counter,
                  logger=self.logger)
        return ret

class Qc:
    def __init__(self, val = 0):
        self.val = val

    def lock(self):
        pass

    def unlock(self):
        pass
