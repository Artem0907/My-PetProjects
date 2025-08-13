from __future__ import annotations

from collections.abc import (
    Generator,
    Iterable,
    Iterator,
    Mapping,
    Sized,
    ItemsView,
    Buffer,
    Collection,
    Container,
    Sequence,
)
import sys
from time import sleep
from typing import Protocol

from tqdm import tqdm


class ProgressBar[_T]:
    def __init__(
        self,
        total: Sequence[_T] | int,
        prefix: str = "",
        units: str = "it",
        length: int = 50,
    ) -> None:
        self.prefix = prefix
        self.units = units
        self.total = total
        self.length = length
        self.current = 0
        self.original_stdout = sys.stdout
        sys.stdout = self

    def write(self, text: str) -> None:
        if text != "\n":
            total_length = str(
                len(self.total)
                if isinstance(self.total, Sequence)
                else self.total
            )
            total = (
                self.length
                + len(self.prefix)
                + 16
                + len(self.units)
                + (len(total_length) * 2)
            )

            self.original_stdout.write("\r" + " " * total + "\r" + text + "\n")
            self.update(0)

    def flush(self) -> None:
        self.original_stdout.flush()

    def update(self, n: int = 1) -> _T | int:
        self.current += n
        total_length = (
            len(self.total) if isinstance(self.total, Sequence) else self.total
        )
        if total_length < self.current:
            raise IndexError

        total_result = (
            self.total[self.current - 1]
            if isinstance(self.total, Sequence)
            else self.total
        )

        percent = f"{(100 * (self.current / total_length)):.1f}"
        filled = self.length * self.current // total_length
        bar = "@" * filled + "#" * (self.length - filled)
        self.original_stdout.write(
            f"\r{self.prefix}: {percent}%[{self.current}/{total_length}{self.units}] | {bar}"
        )
        return total_result

    def __iter__(self):
        return self

    def __next__(self) -> _T | int:
        try:
            return self.update(1)
        except KeyboardInterrupt:
            sys.exit(1)
        except IndexError:
            # self.update(0)
            # print("current stop")
            sys.stdout = self.original_stdout
            print()
            raise StopIteration from None


alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
iterable = [
    (string1 + string2 + string3 + string4 + string5)
    for string1 in alphabet
    for string2 in alphabet
    for string3 in alphabet
    for string4 in alphabet
    for string5 in alphabet
]
print(f"len(iterable_alphabet)={len(iterable)}")
print("started")
for index_ in ProgressBar[str](iterable, "test", "iters", 100):
    if iterable.index(index_) % 25000 == 0:
        print(
            f"current: {index_} ({iterable.index(index_) + 1}/{len(iterable)})"
            # index_
        )
    # sleep(0.05)
print("stopped")
