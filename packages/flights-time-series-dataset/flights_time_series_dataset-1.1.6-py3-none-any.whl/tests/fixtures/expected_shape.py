import pytest

expected = {
    "36":{
        "0": {
            "stride": 1,
            "y_shape": (73, 24, 1),
            "x_shape": (73, 24, 2),
            "y_test_shape": (36, 24, 1),
            "x_test_shape": (36, 24, 2),
        },
        "1": {
            "stride": 1,
            "y_shape": (73, 24, 1),
            "x_shape": (73, 24, 2),
            "y_test_shape": (36, 24, 1),
            "x_test_shape": (36, 24, 2),
        }
    },
    "1":{
        "0": {
            "stride": 'auto',
            "y_shape": (3, 24, 1),
            "x_shape": (3, 24, 2),
            "y_test_shape": (1, 24, 1),
            "x_test_shape": (1, 24, 2),
        },
        "1": {
            "stride": 'auto',
            "y_shape": (2, 24, 1),
            "x_shape": (2, 24, 2),
            "y_test_shape": (1, 24, 1),
            "x_test_shape": (1, 24, 2),
        }
    }
}

@pytest.fixture
def expected_shape():
    def _expected_shape(except_last, augmentation):
        return expected[str(except_last)][str(augmentation)]
    
    return _expected_shape