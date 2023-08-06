from io import StringIO
from random import sample

"""
Fast password module using the "io" and "random" modules.
"""

ASCII_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
SYMBOLS = r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

def securestr(length, chars_in=None):
    """
    Makes a secure string password.

    Usage:
    passwordtools.securestr(length, [chars_in])
    """
    if chars_in is None:
        chars = ASCII_LETTERS + DIGITS + "@%+!?-"
    else:
        chars = ASCII_LETTERS + DIGITS + chars_in
    out = StringIO()
    out.writelines(sample(chars, length))
    password = out.getvalue()
    if len(password) < length:
        password += sample("@%+!?-", 1)[0]
    return password


def pin(length):
    """
    Makes a secure PIN.

    Usage:
    passwordtools.pin(length)
    """
    out = StringIO()
    out.writelines(sample(DIGITS, length))
    password = out.getvalue()
    if len(password) < length:
        password += sample(DIGITS, 1)[0]
    return password


def check(password):
    """
    Checks a password's security.

    Usage:
    passwordtools.check(password)
    """
    lengthsecure = len(password) >= 8
    upsecure = any(x.isupper() for x in password)
    lowsecure = any(x.islower() for x in password)
    specialsecure = any(c in SYMBOLS for c in password)
    digitsecure = any(c in DIGITS for c in password)
    securitydict = {
        "password": password,
        "eight_length": lengthsecure,
        "has_uppercase": upsecure,
        "has_lowercase": lowsecure,
        "has_specialchar": specialsecure,
        "has_digit": digitsecure
    }
    return securitydict
