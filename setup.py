from dependents import dependents
import getpass
import os
import sys
import apt
import platform
from colorama import Fore
import pip
from Tkinter import *


class setup(object):

    curr_os = os.name
    curr_platform = platform.system()
    access_packages_install = True

    def _get_all_modules(self):
        modules = dependents['sys_modules']
        return modules

    def _get_all_packages(self):
        packages = dependents['packages']
        return packages

    def is_linux_posix(self):
        if 'Linux' in self.curr_platform and 'posix' in self.curr_os:
            return True

    def is_root(self):
        if os.geteuid() == 0:
            return True

    def _install_modules(self, it_imptnt=False):
        modules = self._get_all_modules()
        cache = apt.cache.Cache()
        update = cache.update
        pkg = lambda module: cache[module]
        error_modules = []
        if self.is_root():
            for module in modules:
                try:
                    curr_pkg = pkg(module)
                    if curr_pkg.is_installed:
                        print Fore.BLUE + "%s - already installed" % module
                    else:
                        print Fore.GREEN + "%s installing..." % module
                        curr_pkg.mark_install()
                        try:
                            cache.commit()
                        except Exception, arg:
                            print Fore.RED + "ERROR, %s module failed install" % module
                            if it_imptnt:
                                error_modules[module] = arg
                except:
                    print Fore.RED + "Unable to locate package %s " % module
            for module, message in error_modules:
                sys.stdout.write(Fore.RED + "Package %s not installed!\n" % module)
        else:
            sys.exit("Modules not installed. Permission denied: 'Must be root'")
        if error_modules:
            self.access_packages_install = False
        return True

    def run_install_packeges(self, packages=[]):
        for package in packages:
            try:
                sys.stdout.write("%s searching...\n" % package)
                pip.main(['install', package])
            except Exception, arg:
                print arg
        return True

    def _install_packages(self):
        packages = self._get_all_packages()
        if hasattr(sys, 'real_prefix'):
            self.run_install_packeges(packages=packages)
        else:
            qust = raw_input("Virtualenv did not activated!Would you like install packages to global?[y/n]")
            if qust.lower() == 'y':
                self.run_install_packeges(packages=packages)
            else:
                sys.stdout.write("Packages not installed!\n")