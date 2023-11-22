import hashlib


def hash_user_ids(user_ids: list):
    if not user_ids:
        return None

    concatenated_ids = ''.join(map(str, user_ids))
    sha256 = hashlib.sha256()
    sha256.update(concatenated_ids.encode('utf-8'))
    hashed_ids = sha256.hexdigest()
    return hashed_ids
