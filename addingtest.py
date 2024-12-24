import unittest
from add_numbers import adding

import pytest
import pandas as pd

def test_read_file():
    try:
        df = pd.read_excel("data.xlsx")
        assert not df.empty, "The file should not be empty."
    except Exception as e:
        pytest.fail(f"Reading the file failed: {e}")


if __name__ == '__main__':
    unittest.main()
