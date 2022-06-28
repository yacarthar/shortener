""" tools
"""

import hashlib
import uuid

def cheap_hash(string,length=6):
    res = hashlib.sha256(string.encode()).hexdigest()
    if length < len(res):
        return res[:length]
    else:
        raise Exception(f"{len(res)} > {length}")

def cheap_uuid(length=6):
    id_ = uuid.uuid4()
    return str(id_).split("-")[-1][:length]
