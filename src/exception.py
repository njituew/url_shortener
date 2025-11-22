class ShortenerBaseError(Exception):
    pass


class NoOriginalUrlFoundError(ShortenerBaseError):
    pass


class SlugAlreadyExistsError(ShortenerBaseError):
    pass


class InvalidURL_Error(ShortenerBaseError):
    pass
