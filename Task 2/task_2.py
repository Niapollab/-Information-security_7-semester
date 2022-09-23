#!/usr/bin/env python
from bisect import bisect_left
from typing import AbstractSet, Sequence
import string


class VigenereEncryptor:
    __alphabet: list[str]

    def __init__(self, alphabet: AbstractSet[str]) -> None:
        self.__alphabet = [*sorted(alphabet)]

    def encode(self, text: str, key: Sequence[str]) -> str:
        return ''.join(self.__alphabet[(self.__index_in_alphabet(text[i]) + self.__index_in_alphabet(key[i % len(key)])) % len(self.__alphabet)]
            for i in range(len(text)))

    def decode(self, text: str, key: Sequence[str]) -> str:
        return self.encode(text, [self.__alphabet[((len(self.__alphabet) - self.__index_in_alphabet(key_segment))) % len(self.__alphabet)] for key_segment in key])

    def __index_in_alphabet(self, value: str) -> int:
        i = bisect_left(self.__alphabet, value)

        if i != len(self.__alphabet) and self.__alphabet[i] == value:
            return i

        return -1


def main() -> int:
    text = input('Input text: ')
    key = input('Input key: ')

    encryptor = VigenereEncryptor(set(string.ascii_uppercase))

    encoded = encryptor.encode(text, key)
    print('Encoded text:', encoded)

    decoded = encryptor.decode(encoded, key)
    print('Decoded text:', decoded)

    return 0


if __name__ == "__main__":
    main()
