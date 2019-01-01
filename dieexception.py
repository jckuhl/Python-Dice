class DieException(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.message = args[0]