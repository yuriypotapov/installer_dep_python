#!/usr/bin/env python
import ConfigParser

from setup import setup

call_setup = setup()


class main(object):

    def __init__(self):
        """Check is Ubuntu OS, run first run module install, after run packages install """
        if call_setup.is_linux_posix():
            it_imptnt = self.get_options('important_modules')
            call_setup._install_modules(it_imptnt=it_imptnt)
            if call_setup.access_packages_install:
                call_setup._install_packages()

    def get_options(self, option):
        """Return value from options, if option not set return False. If important_modules in config file not set return Fasle """
        config = ConfigParser.ConfigParser()
        option_res = False
        try:
            config.read('conf.cfg')
            option_res = config.get('options', option) if option else False
        except Exception, arg:
            print arg
        return option_res

if __name__ == '__main__':
    main()

