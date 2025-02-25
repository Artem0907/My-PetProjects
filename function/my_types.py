class MyIterable:
    def __init__(self, *data) -> None:
        self.data = list(data)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            value = self.data[self.index]
            self.index += 1
            return value
        else:
            self.index = 0
            raise StopIteration
