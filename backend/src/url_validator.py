import re


def is_valid_url(url: str) -> bool:
    regex = re.compile(
        r"^(https?://)"  # обязательный http:// или https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+"  # домен
        r"(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # .com, .ru и т.д.
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # или IP
        r"(?::\d+)?"  # порт
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return re.match(regex, url.strip()) is not None
