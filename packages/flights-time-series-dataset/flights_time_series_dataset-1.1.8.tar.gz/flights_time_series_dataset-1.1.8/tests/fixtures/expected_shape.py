import pytest

expected = {
    "0": {
        "y_shape": (73, 24, 1),
        "x_shape": (73, 24, 2),
        "y_test_shape": (1, 24, 1),
        "x_test_shape": (1, 24, 2),
    },
    "1": {
        "y_shape": (73, 24, 1),
        "x_shape": (73, 24, 2),
        "y_test_shape": (1, 24, 1),
        "x_test_shape": (1, 24, 2),
    }
}

@pytest.fixture
def expected_shape():
    def _expected_shape(augmentation):
        return expected[str(augmentation)]
    
    return _expected_shape