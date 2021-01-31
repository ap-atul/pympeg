""" Utilities """

import string
from random import sample

def gen_labels(n=1):
    """ Randomly generate label of size 3 with alphabets """
    length = 3
    if n == 1:
        return ''.join(sample(string.ascii_letters, length))
    return [''.join(sample(string.ascii_letters, length)) for _ in range(n)]
