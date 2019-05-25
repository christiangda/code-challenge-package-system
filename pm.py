import cmd


class PMShell(cmd.Cmd):
    """
    My memory structure for DEPENDECIES is a dict where key is a pkg and value is a list of pkgs dependencies:
    DEPENDENCIES =
            {
            'pkg1': ['pkg2', 'pkg4'],
            'pkg2': ['pkg3', 'pkg4'],
            'pkg3': [],
            'pkg4': ['pkg3']
            }

    # Set is an unordered collection with no duplicate elements.
    INSTALLED_PACKAGES = {'pkg1', 'pkg2'}

    """
    DEPENDENCIES = dict()
    INSTALLED_PACKAGES = set()

    prompt = '(PM)>'

    def do_DEPEND(self, arg):
        print('DEPEND {}'.format(arg))
        pkg_list = arg.split()
        if len(pkg_list) < 2:
            print('USAGE: DEPEND pkg1 pkg2 [pkg3 ...]')
            return

        pkg = pkg_list[0]
        if pkg in PMShell.DEPENDENCIES:
            PMShell.DEPENDENCIES[pkg] = pkg_list[1:]
        else:
            PMShell.DEPENDENCIES[pkg] = list()
            PMShell.DEPENDENCIES[pkg] = pkg_list[1:]

        # print(PMShell.DEPENDENCIES)

    def do_INSTALL(self, arg):
        if len(arg.split()) != 1:
            print('Could not be empty or more than one package a time')
            print('USAGE: INSTALL pkg')
            return

        if arg not in PMShell.INSTALLED_PACKAGES:
            """
                If package if not installed, firs install its dependencies
                but if doesn't has dependencies, install it
            """
            if arg in PMShell.DEPENDENCIES:

                for pkg_dep in PMShell.DEPENDENCIES[arg]:
                    if pkg_dep not in PMShell.INSTALLED_PACKAGES:
                        PMShell.INSTALLED_PACKAGES.add(pkg_dep)
                        print('    {} successfully installed'.format(pkg_dep))

                # Install the package itself after install dependencies
                PMShell.INSTALLED_PACKAGES.add(arg)
                print('    {} successfully installed'.format(arg))

            else:
                PMShell.INSTALLED_PACKAGES.add(arg)
                print('    {} successfully installed'.format(arg))

    def do_REMOVE(self, arg):
        if len(arg.split()) != 1:
            print('Could not be empty or more than one package a time')
            print('USAGE: REMOVE pkg')
            return

        if arg in PMShell.DEPENDENCIES:
            PMShell.INSTALLED_PACKAGES.remove(arg)

    def do_LIST(self, arg):
        if len(arg.split()) != 0:
            print('Arguments are not accepted')
            return

        for pkg in PMShell.INSTALLED_PACKAGES:
            print('    {}'.format(pkg))

    def do_END(self):
        return True

    def help_DEPEND(self):
        print("Add new packages")

    def help_INSTALL(self):
        print('Only one package a time')

    def do_DEBUG(self, arg):
        print('INSTALLED_PACKAGES = {}'.format(PMShell.INSTALLED_PACKAGES))
        print('DEPENDENCIES = {}'.format(PMShell.DEPENDENCIES))

    def __install(self, pkg):

        # Package has dependencies
        if pkg in PMShell.DEPENDENCIES:

            # Check every dependency to see if is installed
            for pkg_dep in PMShell.DEPENDENCIES[pkg]:
                if pkg_dep not in PMShell.INSTALLED_PACKAGES:
                    PMShell.INSTALLED_PACKAGES.add(pkg_dep)
                    print('    {} successfully installed'.format(pkg_dep))
        else:
            PMShell.INSTALLED_PACKAGES.add(pkg_dep)
            print('    {} successfully installed'.format(pkg_dep))


if __name__ == "__main__":
    PMShell().cmdloop()
