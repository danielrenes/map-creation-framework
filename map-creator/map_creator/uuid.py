'''Supports only UUID version 4 which uses random numbers to generate the UUID.
'''

import random

digits = ['0', '1', '2', '3', '4', '5', '6', '7',
          '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']


def generate_uuid():
    def _generate_digit():
        index = random.randint(0, 15)
        return digits[index]

    def _generate_block(length):
        return ''.join(_generate_digit() for _ in range(length))

    return '-'.join(_generate_block(block_length)
                    for block_length in [8, 4, 4, 4, 12])
