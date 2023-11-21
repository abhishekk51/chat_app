import hashlib


def hash_user_ids(user_ids: list):
    if not user_ids:
        return None

    # Concatenate all user IDs as a string
    concatenated_ids = ''.join(map(str, user_ids))

    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the bytes representation of the concatenated IDs
    sha256.update(concatenated_ids.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_ids = sha256.hexdigest()

    return hashed_ids
