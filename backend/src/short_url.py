import string
from secrets import choice


ALBPHABET = string.ascii_letters + string.digits


async def generate_random_slug() -> str:
    slug = ""
    for _ in range(6):
        slug += choice(ALBPHABET)
    return slug
