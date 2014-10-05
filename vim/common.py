def normalize_string(str):
    """
    returns a slugified string
    >>> normalize_string('thIs is A  test  ')
    'thisisatest'

    """
    import re
    str = str.strip().lower()
    str = re.sub(r'\s+', '', str)
    return str

if __name__ == "__main__":
    import doctest
    doctest.testmod()
