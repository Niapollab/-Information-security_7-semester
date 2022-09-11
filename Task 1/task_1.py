#!/usr/bin/env python
def encode(text: str, key1: list[int], key2: list[int]) -> str:
    encoded_text = []
    key2_length = len(key2)

    for key_segment_2 in key2:
        for row_offset in range(len(key1)):
            key_segment_1 = key1[row_offset]

            encoded_text.append(text[(key_segment_1 - 1) * key2_length + (key_segment_2 - 1)])

    return ''.join(encoded_text)


def decode(text: str, key1: list[int], key2: list[int]) -> str:
    map_order = [*range(1, len(key2) + 1)]

    mapped_key_1 = [element for _, element in sorted(zip(key1, map_order))]
    mapped_key_2 = [element for _, element in sorted(zip(key2, map_order))]

    return encode(text, mapped_key_2, mapped_key_1)


def main() -> int:
    text = input('Input text: ')
    key1 = [int(key_segment.strip()) for key_segment in input('Input first key: ').split()]
    key2 = [int(key_segment.strip()) for key_segment in input('Input second key: ').split()]

    encoded = encode(text, key1, key2)
    print('Encoded text:', encoded)

    decoded = decode(encoded, key1, key2)
    print('Decoded text:', decoded)

    return 0


if __name__ == "__main__":
    main()
