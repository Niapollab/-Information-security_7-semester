#!/usr/bin/env python
from itertools import islice
from math import sqrt
from random import randrange
from typing import Iterable, Sequence


def random_range(start: int, stop: int) -> Iterable[int]:
    while True:
        yield randrange(start, stop)


def is_prime(num: int) -> bool:
    if num == 2:
        return True

    if num & 1 == 0:
        return False

    for n in range(3, int(sqrt(num)) + 2, 2):
        if num % n == 0:
            return False

    return True


def extended_gcd(r1, r2, s1=1, s2=0, t1=0, t2=1) -> tuple[int, int]:
    if r2 == 0:
        return r1, \
            s1 + s2 if s1 < 0 else s1

    q, r = r1 // r2, r1 % r2
    s, t = s1 - s2 * q, t1 - t2 * q

    return extended_gcd(r2, r, s2, s, t2, t)


def fast_modular_exponent(base: int, exp: int, mod: int) -> int:
	y = 1

	bin_exp = bin(exp)[-1:1:-1]
	for cur_bin in bin_exp:
		if int(cur_bin):
			y = (base * y) % mod
		base = (base ** 2) % mod

	return y


def generate_key_pair(key_length: int) -> tuple[tuple[int, int], tuple[int, int]]:
    start_number = 10 ** key_length
    end_number = start_number * 10

    p, q = tuple(islice((number
                         for number in random_range(start_number, end_number)
                         if is_prime(number)), 2))

    n = p * q
    phi = (p - 1) * (q - 1)

    e, d = next((number, ret[1])
                for number in random_range(2, phi)
                if (ret := extended_gcd(number, phi))[0] == 1)

    return ((e, n), (d, n))


def encrypt(public_key: tuple[int, int], data: Sequence[int]) -> Sequence[int]:
    e, n = public_key
    return[fast_modular_exponent(byte, e, n) for byte in data]


def decrypt(private_key: tuple[int, int], data: Sequence[int]) -> bytes:
    return bytes(encrypt(private_key, data))


def main() -> int:
    KEY_LENGTH = 8

    public_key, private_key = generate_key_pair(KEY_LENGTH)
    print(f'Public key for session: {public_key}; Private key for session: {private_key}')

    text_bytes = input('Input text: ').encode('utf-8')

    encoded_message = encrypt(public_key, text_bytes)
    print(f'Encoded message: {encoded_message}')

    decoded_message = decrypt(private_key, encoded_message).decode('utf-8')
    print(f'Decoded message: {decoded_message}')

    return 0


if __name__ == "__main__":
    main()
