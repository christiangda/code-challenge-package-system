import cmd


class PMShell(cmd.Cmd):
    """
    My memory structure for DEPENDENCIES is a dict where key is a pkg and value is a list of pkgs dependencies:

    # Storage for packages dependencies
    DEPENDENCIES =
            {
                'pkg1': ['pkg2', 'pkg4'],
                'pkg2': ['pkg3', 'pkg4'],
                'pkg3': [],
                'pkg4': ['pkg3']
            }

    # Storage for who depend of witch package
    IS_DEPENDENCY =
            {
                'pkg4': ['pkg1','pkg2']
            }

    # Storage for packages installed
    INSTALLED_PACKAGES = {'pkg1', 'pkg2'}

    """
    DEPENDENCIES = dict()
    INSTALLED_PACKAGES = set()
    IS_DEPENDENCY = dict()

    prompt = '(PM)>'

    def do_DEPEND(self, arg):
        pkg_list = arg.split()
        if len(pkg_list) < 2:
            print('USAGE: DEPEND pkg1 pkg2 [pkg3 ...]')
            return

        pkg = pkg_list[0]

        # Package dependencies
        if pkg in self.DEPENDENCIES:
            self.DEPENDENCIES[pkg] = set(pkg_list[1:])
        else:
            self.DEPENDENCIES[pkg] = set(pkg_list[1:])

        # If package if dependency of
        for dep in pkg_list[1:]:
            if dep in self.IS_DEPENDENCY:
                self.IS_DEPENDENCY[dep].add(pkg)
            else:
                self.IS_DEPENDENCY[dep] = set()
                self.IS_DEPENDENCY[dep].add(pkg)

    def do_INSTALL(self, arg):
        if len(arg.split()) != 1:
            print('Could not be empty or more than one package a time')
            print('USAGE: INSTALL pkg')
            return

        if arg not in self.INSTALLED_PACKAGES:
            if arg in self.DEPENDENCIES:
                for pkg_dep in self.DEPENDENCIES[arg]:
                    if pkg_dep not in self.INSTALLED_PACKAGES:
                        self.INSTALLED_PACKAGES.add(pkg_dep)
                        print('    {} successfully installed'.format(pkg_dep))

                # Install the package itself after install dependencies
                self.INSTALLED_PACKAGES.add(arg)
                print('    {} successfully installed'.format(arg))

            else:
                self.INSTALLED_PACKAGES.add(arg)
                print('    {} successfully installed'.format(arg))
        else:
            print('    {} is already installed'.format(arg))

    def do_REMOVE(self, arg):
        if len(arg.split()) != 1:
            print('Could not be empty or more than one package a time')
            print('USAGE: REMOVE pkg')
            return

        if arg in self.IS_DEPENDENCY:
            print('    {} is still needed'.format(arg))
        elif arg not in self.INSTALLED_PACKAGES:
            print('    {} is not installed'.format(arg))
        else:
            self.INSTALLED_PACKAGES.remove(arg)
            print('    {} successfully removed'.format(arg))

            # Check dependencies and delete its from its dependencies list
            if arg in self.DEPENDENCIES:
                for dep in self.DEPENDENCIES[arg]:
                    # If a package is saved as dependency of other package
                    if arg in self.IS_DEPENDENCY[dep]:
                        self.IS_DEPENDENCY[dep].remove(arg)
                        if (dep in self.IS_DEPENDENCY) and (len(self.IS_DEPENDENCY[dep]) == 0):
                            print('    {} is no longer needed'.format(dep))
                            self.IS_DEPENDENCY.pop(dep)
                            self.do_REMOVE(dep)

    def do_LIST(self, arg):
        if len(arg.split()) != 0:
            print('Arguments are not accepted')
            return

        for pkg in self.INSTALLED_PACKAGES:
            print('    {}'.format(pkg))

    def do_END(self):
        return True

    def do_DEBUG(self, arg):
        print('INSTALLED_PACKAGES = {}'.format(self.INSTALLED_PACKAGES))
        print('DEPENDENCIES = {}'.format(self.DEPENDENCIES))
        print('IS_DEPENDENCY = {}'.format(self.IS_DEPENDENCY))


if __name__ == "__main__":
    PMShell().cmdloop()
