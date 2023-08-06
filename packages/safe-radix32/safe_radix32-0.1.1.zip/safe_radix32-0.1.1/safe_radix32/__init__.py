"""
safe_radix32
Radix32 encode long integers with a safe alphabet.

:copyright: 2021 Nándor Mátravölgyi
:license: Apache2, see LICENSE for more details.
"""
import os

__author__ = "Nándor Mátravölgyi"
__copyright__ = "Copyright 2021 Nándor Mátravölgyi"
__author_email__ = "nandor.matra@gmail.com"
__version__ = "0.1.1"


if os.environ.get("SAFE_RADIX32_PUREPYTHON"):
    from .pure import encode_safe_radix32, decode_safe_radix32, SAFE_RADIX32_ALPHABET, SAFE_RADIX32_ALPHABET_RE
else:
    try:
        from ._cython import encode_safe_radix32, decode_safe_radix32, SAFE_RADIX32_ABC, SAFE_RADIX32_ALPHABET_RE
    except ImportError:
        from .pure import encode_safe_radix32, decode_safe_radix32, SAFE_RADIX32_ALPHABET, SAFE_RADIX32_ALPHABET_RE


encode = encode_safe_radix32
decode = decode_safe_radix32

ALPHABET = SAFE_RADIX32_ALPHABET
ALPHABET_RE = SAFE_RADIX32_ALPHABET_RE
