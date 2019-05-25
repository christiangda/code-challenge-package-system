import unittest
import unittest.mock
import pm
import sys
import io


class PackagemanagerTest(unittest.TestCase):
    # # def setUp(self):
    # #     self.mock_stdin = unittest.mock.create_autospec(sys.stdin)
    # #     self.mock_stdout = unittest.mock.create_autospec(sys.stdout)

    # def setUp(self):
    #     self.input = io.StringIO("print test\nprint test2")
    #     self.output = io.StringIO()

    # def create(self):
    #     return pm.PMShell(stdin=self.input, stdout=self.output)

    def test_command(self):
        output = io.StringIO()
        cmd = pm.PMShell(stdout=output)
        cmd.onecmd('DEPEND pkg1 pkg2 pkg3')
        self.assertMultiLineEqual(output.getvalue(),
                                  ("(Cmd) test\n"
                                   "(Cmd) test2\n"
                                   "(Cmd) "))
        # cmd.onecmd('END')


if __name__ == '__main__':
    unittest.main()
