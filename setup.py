#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension

cooccur_module = Extension('src/_cooccur',
                           sources=['GloVe/src/cooccur.c', 'src/cooccur_wrap.c'],
                           extra_compile_args=["-Dmain=cooccur_main"])

glove_module = Extension('src/_glove',
                         sources=['GloVe/src/glove.c', 'src/glove_wrap.c'],
                         extra_compile_args=["-Dmain=glove_main"])

shuffle_module = Extension('src/_shuffle',
                           sources=['GloVe/src/shuffle.c', 'src/shuffle_wrap.c'],
                           extra_compile_args=["-Dmain=shuffle_main"])

vocab_count_module = Extension('src/_vocab_count',
                         sources=['GloVe/src/vocab_count.c', 'src/vocab_count_wrap.c'],
                         extra_compile_args=["-Dmain=vocab_count_main"])

ext_mods = [cooccur_module, glove_module, shuffle_module, vocab_count_module]
py_mods = ['src/cooccur', 'src/glove', 'src/shuffle', 'src/vocab_count']

setup (name = 'glove_c_wrap',
       version = '1.0',
       author      = "Gabriel Barbutti",
       description = """SWIG wrap of GloVe""",
       ext_modules = ext_mods,
       py_modules = py_mods,
       )
