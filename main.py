#!/usr/bin/env python

from setup import setup

call_setup = setup()

if __name__ == '__main__':
    if call_setup.is_posix():
        call_setup._install_packages()
        call_setup._install_modules()
