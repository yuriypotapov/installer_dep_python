from dependents import dependents
import getpass
import os
import sys
import platform
from colorama import Fore
import pip


class Setup(object):

    curr_os = os.name
    curr_platform = platform.system()
    access_packages_install = True
    error_modules = []

    def _get_all_modules(self):
        modules = dependents['sys_modules']
        return modules

    def _get_all_packages(self):
        packages = dependents['packages']
        return packages

    def is_linux_posix(self):
        if 'Linux' in self.curr_platform and 'posix' in self.curr_os:
            return True

    def is_linux_fedora(self):
        if 'Linux' in self.curr_platform and 'fedora' in self.curr_platform:
            return True

    def is_root(self):
        if os.geteuid() == 0:
            return True

    def run_install_module(self, cache, modules, it_imptnt):
        pkg = lambda module: cache[module]

        for module in modules:
            try:
                curr_pkg = pkg(module)
                if curr_pkg.is_installed:
                    print Fore.BLUE + "%s - already installed" % module
                else:
                    print Fore.GREEN + "\n %s installing..." % module
                    curr_pkg.mark_install()
                    try:
                        cache.commit()
                    except Exception, arg:
                        print Fore.RED + "ERROR, %s module failed install" % module
                        if it_imptnt:
                            self.error_modules[module] = arg
            except:
                print Fore.RED + "Unable to locate package %s " % module
        for module, message in self.error_modules:
            sys.stdout.write(Fore.RED + "Package %s not installed!\n" % module)

    def _install_modules_l_posix(self, it_imptnt):
        import apt

        modules = self._get_all_modules()
        cache = apt.cache.Cache()
        update = cache.update

        self.run_install_module(cache=cache, modules=modules, it_imptnt=it_imptnt)
        if self.error_modules:
            self.access_packages_install = False
        return True

    def _install_modules_f_posix(self):
         import yum
         modules = self._get_all_modules()
         yumex = yum.YumBase()
         yumex.conf.assumeyes = True

         for module in modules:
            if yumex.rpmdb.searchNevra(name=module.strip()):
                sys.stdout.write("%s - already installed")
            else:
                sys.stdout.write("%s installing ...")
                yumex.install(name=module.strip())

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