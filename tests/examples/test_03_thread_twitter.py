"""Smoke test for examples/03_thread_twitter.py.

Auto-generated stub (audit-project PS303). Replace with a real test
that runs the example end-to-end and asserts on its outputs.
"""

import importlib.util
from pathlib import Path


EXAMPLE = Path(__file__).resolve().parents[2] / "examples" / "03_thread_twitter.py"


def test_example_file_exists_on_disk():
    # Arrange
    expected_path = EXAMPLE
    # Act
    found = expected_path.exists()
    # Assert
    assert found, f"missing example file: {expected_path}"


def test_example_spec_has_resolvable_loader():
    # Arrange
    target = EXAMPLE
    # Act
    spec = importlib.util.spec_from_file_location("ex", target)
    # Assert
    assert spec is not None and spec.loader is not None


def test_example_module_object_creates_from_spec():
    # Arrange
    spec = importlib.util.spec_from_file_location("ex", EXAMPLE)
    # Act
    module = importlib.util.module_from_spec(spec)
    # Assert
    assert module is not None
