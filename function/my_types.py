class MyIterable(object):
    def __init__(self, *data) -> None:
        self.data = list(data)
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.data):
            self._index += 1
            return self.data[self._index]
        else:
            self._index = 0
            raise StopIteration

    def __str__(self) -> str:
        return f"MyIterable({self.data})"

    def __repr__(self) -> str:
        return f"<class MyIterable({self.data})>"

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]
