

class SingletonDependency:
    def after_inject(self):
        pass
    pass


class TransientDependency:
    target_name: str

    def after_inject(self):
        pass


    def __init__(self, name: str):
        self.target_name = name
        pass
