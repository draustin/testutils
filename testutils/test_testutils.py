

import pytest

from testutils import compare_other_process_repr, load_and_save_repr


class X:
    pass

def test_compare_other_process_repr():
    compare_other_process_repr(5)
    with pytest.raises(AssertionError):
        compare_other_process_repr(X())


