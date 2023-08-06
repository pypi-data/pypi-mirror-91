# -*- coding: utf-8 -*-
# cython: c_string_encoding=ascii, language_level=3
"""
safe_radix32 implementation in cython

:copyright: 2021 Nándor Mátravölgyi
:license: Apache2, see LICENSE for more details.
"""
import re
from libc.stdlib cimport malloc, free

cdef int SAFE_BASE_BITS = 5
cdef int SAFE_MASK = (1 << SAFE_BASE_BITS) - 1
cdef char* SAFE_MAP = '2346789BCFGJKLMPQVWZbcfgjkmpqvwz'
cdef char* SAFE_MAP_SHIFTS = [60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0]
cdef int SAFE_MAP_SHIFTS_NUM = 13
cdef char TOP_SHIFT_MAX0 = (1 << (64 - SAFE_MAP_SHIFTS[0])) - 1
cdef char TOP_SHIFT_MAX1 = SAFE_MAP[TOP_SHIFT_MAX0]

cdef char* SAFE_UNMAP = [
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 1, 2, 255, 3, 4,
    5, 6, 255, 255, 255, 255, 255, 255, 255, 255, 7, 8, 255, 255, 9, 10, 255, 255, 11, 12,
    13, 14, 255, 255, 15, 16, 255, 255, 255, 255, 17, 18, 255, 255, 19, 255, 255, 255, 255,
    255, 255, 255, 20, 21, 255, 255, 22, 23, 255, 255, 24, 25, 255, 26, 255, 255, 27, 28,
    255, 255, 255, 255, 29, 30, 255, 255, 31, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255
]

SAFE_RADIX32_ALPHABET = <str>SAFE_MAP
SAFE_RADIX32_ALPHABET_RE = re.compile(r"^["+SAFE_RADIX32_ALPHABET+"]+$", re.ASCII)


def encode_safe_radix32(long v):
    """
    :raise OverflowError value is not C long (raised by cython at function call)
    """
    cdef char* c_string = <char *> malloc((SAFE_MAP_SHIFTS_NUM + 1) * sizeof(char))
    if not c_string:
        raise MemoryError
    cdef int leading_zeros = 0
    cdef int shift_i = 0
    while shift_i < SAFE_MAP_SHIFTS_NUM - 1:
        char_v = (v >> SAFE_MAP_SHIFTS[shift_i]) & SAFE_MASK
        if char_v > 0:
            if shift_i == 0:
                char_v &= TOP_SHIFT_MAX0
            leading_zeros = shift_i
            shift_i += 1
            c_string[0] = SAFE_MAP[char_v]
            break
        shift_i += 1
    else:
        leading_zeros = shift_i
    while shift_i < SAFE_MAP_SHIFTS_NUM:
        c_string[shift_i - leading_zeros] = SAFE_MAP[(v >> SAFE_MAP_SHIFTS[shift_i]) & SAFE_MASK]
        shift_i += 1
    c_string[shift_i - leading_zeros] = 0
    try:
        return <str>c_string
    finally:
        free(c_string)


def decode_safe_radix32(str v):
    """
    :raise UnicodeEncodeError if input contains invalid characters (encoding-related)
    :raise OverflowError if input contains invalid characters (alphabet-related) or value is not C long
    """
    cdef int l = len(v)
    if l > SAFE_MAP_SHIFTS_NUM:
        raise OverflowError
    cdef char* c_string = v
    if l == SAFE_MAP_SHIFTS_NUM and c_string[0] > TOP_SHIFT_MAX1:
        raise OverflowError
    cdef char x
    cdef long u = 0
    cdef int i = 0
    while True:
        x = SAFE_UNMAP[<int>c_string[i]]
        if x == -1:
            raise OverflowError
        u |= x
        i += 1
        if i >= l:
            break
        u <<= SAFE_BASE_BITS
    return u
