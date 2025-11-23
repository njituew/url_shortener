import pytest
from backend.src.url_validator import is_valid_url


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("http://example.com", True),
        ("https://example.com", True),
        ("http://localhost", True),
        ("http://127.0.0.1", True),
        ("http://127.0.0.1:8000", True),
        ("https://sub.domain.example.com", True),
        ("https://example.com/path?query=123", True),
        ("ftp://example.com", False),  # invalid scheme
        ("example.com", False),  # missing scheme
        ("http:/example.com", False),  # malformed scheme
        ("http://", False),  # incomplete URL
        ("", False),
        ("http://example .com", False),
    ],
)
def test_is_valid_url(test_input, expected):
    assert is_valid_url(test_input) == expected
