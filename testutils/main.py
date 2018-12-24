"""Previously this file was called testutils.py, but having the same name as the package seemed to confuse dill."""
import difflib
import os
import subprocess
import sys
import tempfile

import dill


def compare_other_process_repr(obj):
    with tempfile.TemporaryDirectory() as dir:
        pkl_path = os.path.join(dir, 'obj.pkl')
        with open(pkl_path, 'wb') as file:
            dill.dump(obj, file)

        # Run a script which loads the pickled object and saves its string representation.
        args = sys.executable, os.path.join(os.path.dirname(__file__), '_run_load_and_save_repr.py'), '-r', pkl_path
        subprocess.run(args, shell=False)

        txt_path = get_txt_path(pkl_path)
        with open(txt_path, 'r') as file:
            other_repr_lines = file.readlines()
        other_repr = ''.join(other_repr_lines)
    our_repr = repr(obj)
    if our_repr != other_repr:
        print('\n'.join(list(difflib.unified_diff(our_repr, other_repr))))
        raise AssertionError()


def get_txt_path(pkl_path):
    dir = os.path.dirname(pkl_path)
    name = os.path.splitext(os.path.basename(pkl_path))[0]
    txt_path = os.path.join(dir, name + '.txt')
    return txt_path


def load_and_save_repr(pkl_path):
    with open(pkl_path, 'rb') as file:
        obj = dill.load(file)
    txt_path = get_txt_path(pkl_path)
    with open(txt_path, 'w') as file:
        file.write(repr(obj))


class _TestClass:
    pass
