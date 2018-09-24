import hashlib


def token_generator(username, email):
    m = hashlib.sha256()
    m.update((username + email).encode())
    return m.hexdigest()
