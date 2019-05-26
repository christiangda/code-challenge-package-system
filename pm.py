#!/usr/bin/env python3
import cmd


class PMShell(cmd.Cmd):
    """
    # Storage for packages dependencies
    DEPENDENCIES =
            {
                'pkg1': {'pkg2', 'pkg4'},
                'pkg2': {'pkg3', 'pkg4'},
                'pkg3': {'pkg1','pkg2'}
                'pkg4': {'pkg1','pkg3'}
            }

    # Storage for who depend on which package
    IS_DEPENDENCY =
            {
                'pkg4': {'pkg1','pkg3'}
            }

    # Storage for packages installed
    INSTALLED_PACKAGES = {'pkg1', 'pkg2'}
    """

    DEPENDENCIES = dict()
    INSTALLED_PACKAGES = set()
    IS_DEPENDENCY = dict()

    prompt = '(Package Manager)-->'

    def do_DEPEND(self, arg):
        pkg_list = arg.split()
        if len(pkg_list) < 2:
            print('USAGE: DEPEND pkg1 pkg2 [pkg3 ...]')
            return

        pkg = pkg_list[0]

        # Package dependencies
        self.DEPENDENCIES[pkg] = set(pkg_list[1:])

        # If package is dependency of
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

        # Install the package if not installed
        if arg not in self.INSTALLED_PACKAGES:
            # Package has dependencies?
            if arg in self.DEPENDENCIES:
                # Check package dependencies too
                for pkg_dep in self.DEPENDENCIES[arg]:
                    # Dependency package is not installed yet?
                    if pkg_dep not in self.INSTALLED_PACKAGES:
                        # Call this function again
                        self.INSTALLED_PACKAGES.add(pkg_dep)
                        print('    {} successfully installed'.format(pkg_dep))

                # Install the package itself after install dependencies
                self.INSTALLED_PACKAGES.add(arg)
                print('    {} successfully installed'.format(arg))

            else:
                # Install the package
                self.INSTALLED_PACKAGES.add(arg)
                print('    {} successfully installed'.format(arg))
        else:
            # Package were installed
            print('    {} is already installed'.format(arg))

    def do_REMOVE(self, arg):
        if len(arg.split()) != 1:
            print('Cannot be empty or more than one package a time')
            print('USAGE: REMOVE pkg')
            return

        # Package is a dependency of other package?
        if arg in self.IS_DEPENDENCY:
            print('    {} is still needed'.format(arg))
        # Package is not installed?
        elif arg not in self.INSTALLED_PACKAGES:
            print('    {} is not installed'.format(arg))
        else:
            # PAckage is installed, so remove it
            self.INSTALLED_PACKAGES.remove(arg)
            print('    {} successfully removed'.format(arg))

            # Check dependencies and delete its from its dependencies list
            # Package has dependencies?
            if arg in self.DEPENDENCIES:
                # Check every package dependency
                for dep in self.DEPENDENCIES[arg]:
                    # package is dependency of others packages?
                    if arg in self.IS_DEPENDENCY[dep]:
                        # remove package from reverse dependency list
                        self.IS_DEPENDENCY[dep].remove(arg)
                        # If package reverse dependency is empty, remove it from set
                        if (dep in self.IS_DEPENDENCY) and (len(self.IS_DEPENDENCY[dep]) == 0):
                            print('    {} is no longer needed'.format(dep))
                            self.IS_DEPENDENCY.pop(dep)
                            # call this function again for every dependency
                            self.do_REMOVE(dep)

    def do_LIST(self, arg):
        if len(arg.split()) != 0:
            print('Arguments are not accepted')
            return

        for pkg in self.INSTALLED_PACKAGES:
            print('    {}'.format(pkg))

    def do_END(self, arg):
        return True

    def do_EOF(self, arg):
        print()
        return True

    def do_DEBUG(self, arg):
        print('INSTALLED_PACKAGES = {}'.format(self.INSTALLED_PACKAGES))
        print('DEPENDENCIES = {}'.format(self.DEPENDENCIES))
        print('IS_DEPENDENCY = {}'.format(self.IS_DEPENDENCY))


if __name__ == "__main__":
    pm = PMShell()
    pm.cmdloop()
