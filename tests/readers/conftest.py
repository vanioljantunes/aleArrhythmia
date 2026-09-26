"""The reader tests run the readers in the real page, so they need Playwright too. Fixtures live in tests/conftest.py."""
import pytest

pytest.importorskip("playwright")
