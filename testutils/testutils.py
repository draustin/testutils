import difflib
import getopt
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

        # Have to use shell=True to guarantee we get the right Python environment (e.g. conda). With shell=True,
        # need to use a string rather than sequence of arguments.
        subprocess.run('_run_load_and_save_repr -r '+pkl_path, shell=True)

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


def _run_load_and_save_repr():
    # For command line use.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'r:')
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o == '-r':
            print('loading and saving', a)
            load_and_save_repr(a)
    sys.exit(0)
