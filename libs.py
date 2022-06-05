""" libs
"""

import hashlib

def cheap_hash(string,length=6):
    res = hashlib.sha256(string.encode()).hexdigest()
    if length < len(res):
        return res[:length]
    else:
        raise Exception(f"{len(res)} > {length}")
