"""Browser tests need Playwright; without it this directory is skipped. Fixtures live in tests/conftest.py."""
import pytest

pytest.importorskip("playwright")
