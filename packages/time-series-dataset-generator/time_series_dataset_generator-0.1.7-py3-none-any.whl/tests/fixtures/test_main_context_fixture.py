import pytest

result = {
    "auto": {
        "mean_r2_score": -20,
        "final_r2_score": -30,
        "n_cv_splits": 2,
        'past_pattern_length': 24,
        'future_pattern_length': 12,
        'except_last_n': 72,
    },
    "1": {
        "mean_r2_score": 0,
        "final_r2_score": -1,
        "n_cv_splits": 4,
        'past_pattern_length': 56,
        'future_pattern_length': 12,
        'except_last_n': 72,
    }
}

@pytest.fixture
def test_main_context():
    def _test_main_context(stride):
        return result[str(stride)]
    
    return _test_main_context