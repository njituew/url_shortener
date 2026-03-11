import pytest
from src.url_validator import is_valid_url


@pytest.mark.parametrize(
    "url,expected",
    [
        # --- Валидные URL ---
        ("http://example.com", True),
        ("https://example.com", True),
        ("http://localhost", True),
        ("http://127.0.0.1", True),
        ("http://127.0.0.1:8000", True),
        ("https://sub.domain.example.com", True),
        ("https://example.com/path?query=123", True),
        ("https://example.com/path/to/page", True),
        ("https://example.com/path#anchor", True),
        ("  https://example.com  ", True),  # strip() должен обрабатывать пробелы
        # --- Невалидная схема ---
        ("ftp://example.com", False),
        ("javascript:alert(1)", False),
        ("//example.com", False),
        # --- Неправильный формат ---
        ("example.com", False),  # нет схемы
        ("http:/example.com", False),  # одинарный слеш
        ("http://", False),  # нет хоста
        ("", False),  # пустая строка
        ("http://example .com", False),  # пробел в домене
    ],
)
def test_is_valid_url(url: str, expected: bool):
    assert is_valid_url(url) == expected
