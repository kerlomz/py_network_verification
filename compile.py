#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

import sys
import os
import logging
from os.path import splitext
from glob import glob


def main(*filenames):

    logging.info('Given filenames = ' + '\n'.join(filenames))
    logging.info('Current dir contents: \n    ' + '\n    '.join(os.listdir('.')))

    _files = [f for g in filenames for f in glob(g)]
    logging.info('Detected files: \n    ' + '\n    '.join(_files))

    # Collect all the extensions to process
    extensions = []
    for f in _files:
        basename, ext = splitext(f)
        extensions.append((basename, f))

    sys.argv = [sys.argv[0], 'build_ext', '--inplace']

    from setuptools import setup, Extension
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    import Cython.Compiler.Options
    Cython.Compiler.Options.annotate = False

    # Create module objects
    ext_modules = []
    for n, f in extensions:
        # The name must be plain, no path
        module_name = os.path.basename(n)
        obj = Extension(module_name, [f], extra_compile_args=["-O2"])
        ext_modules.append(obj)

    setup(
        cmdclass={'build_ext': build_ext},
        include_dirs=[],
        ext_modules=cythonize(ext_modules, language_level=3),
    )


compiled_suffix = ".cp37-win_amd64.pyd"
final_suffix = ".pyd"
origin_suffix = ".pyx"
c_suffix = ".c"

files = ["core", "verification", "constants"]
os.chdir("nv_client/nv")
for file in files:
    _compiled = "{}{}".format(file, compiled_suffix)
    _origin = "{}{}".format(file, origin_suffix)
    _c = "{}{}".format(file, c_suffix)
    _final = "{}{}".format(file, final_suffix)
    if os.path.exists(_compiled):
        os.remove(_compiled)
    if os.path.exists(_final):
        os.remove(_final)
    print('----------------', file)
    main(_origin)
    os.remove(_c)
    os.renames(_compiled, _final)
