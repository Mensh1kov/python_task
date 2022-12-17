#!/usr/bin/env python

import sys


def f0():
    # raise BaseException
    len(int())


def f1():
    # raise Exception
    len(int())


def f2():
    # raise ArithmeticError
    1 / 0


def f3():
    raise FloatingPointError
    # Цитата из python 3.11.0 documentation:
    #      exception FloatingPointError
    #      Not currently used.


def f4():
    # raise OverflowError
    1.23 ** 9999999999999


def f5():
    # raise ZeroDivisionError
    1 / 0


def f6():
    # raise AssertionError
    assert int() == str()


def f7():
    # raise AttributeError
    object.spam


def f8():
    # raise EnvironmentError
    open('nonexistent_file')


def f9():
    # raise ImportError
    import nonexistent_module


def f10():
    # raise LookupError
    dict()['nonexistent_key']


def f11():
    # raise IndexError
    list()[int()]


def f12():
    # raise KeyError
    dict()['nonexistent_key']


def f13():
    # raise NameError
    nonexistent_name


def f14():
    # raise SyntaxError
    eval('(')


def f15():
    # raise ValueError
    int(str())


def f16():
    # raise UnicodeError
    'не аски символы'.encode('ascii')


def check_exception(f, exception):
    try:
        f()
    except exception:
        pass
    else:
        print("Bad luck, no exception caught: %s" % exception)
        sys.exit(1)


check_exception(f0, BaseException)
check_exception(f1, Exception)
check_exception(f2, ArithmeticError)
check_exception(f3, FloatingPointError)
check_exception(f4, OverflowError)
check_exception(f5, ZeroDivisionError)
check_exception(f6, AssertionError)
check_exception(f7, AttributeError)
check_exception(f8, EnvironmentError)
check_exception(f9, ImportError)
check_exception(f10, LookupError)
check_exception(f11, IndexError)
check_exception(f12, KeyError)
check_exception(f13, NameError)
check_exception(f14, SyntaxError)
check_exception(f15, ValueError)
check_exception(f16, UnicodeError)

print("Congratulations, you made it!")
