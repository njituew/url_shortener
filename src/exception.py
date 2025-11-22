class ShortenerBaseError(Exception):
    pass


class NoOriginalUrlFoundError(ShortenerBaseError):
    pass
