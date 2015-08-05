import os
import shutil
import sys
import unittest

from mann import batch_sweep

HERE = os.path.abspath(os.path.dirname(__file__))


def test_chmod_recursive():
    print(unittest, file=sys.stderr)
    root_dir = os.path.join(HERE, 'test_chmod_recursive_root')
    sub_dir = os.path.join(HERE, 'test_chmod_recursive_root', 'sub')
    sub_sub_dir = os.path.join(HERE,
                               'test_chmod_recursive_root', 'sub', 'subsub')
    if os.path.exists(root_dir):
        batch_sweep.chmod_recursive(root_dir,
                                    dir_chmod=0o777, file_chmod=0o777)
        shutil.rmtree(root_dir)

    os.makedirs(sub_sub_dir)

    for test_dir in [root_dir, sub_dir, sub_sub_dir]:
        open(os.path.join(test_dir, 'test_file.txt'), 'w').close()

    batch_sweep.chmod_recursive(root_dir)
    # unittest.TestCase.assertRaises(PermissionError, shutil.rmtree, root_dir, )
    batch_sweep.chmod_recursive(root_dir, dir_chmod=0o777, file_chmod=0o777)
    shutil.rmtree(root_dir)
