from secrets import token_urlsafe


def make_nonce():
    return token_urlsafe(32)
