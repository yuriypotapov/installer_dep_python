#!/usr/bin/env python

from setup import setup

call_setup = setup()


class main(object):

    def __init__(self):
        if call_setup.is_linux_posix():
            call_setup._install_modules(it_imptnt=True)
            if call_setup.access_packages_install:
                call_setup._install_packages()

if __name__ == '__main__':
    main()

