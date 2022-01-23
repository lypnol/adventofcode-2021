import errno
import subprocess

from tool.runners.exceptions import CompilationError, RuntimeError
from tool.runners.wrapper import SubmissionWrapper


class SubmissionNode(SubmissionWrapper):
    def __init__(self, file):
        SubmissionWrapper.__init__(self)
        self.file = file

    def language(self):
        return "js"

    def exec(self, input):
        try:
            return subprocess.check_output(["node", self.file, input]).decode()
        except OSError as e:
            if e.errno == errno.ENOENT:
                # executable not found
                raise CompilationError(e)
            else:
                # subprocess exited with another error
                raise RuntimeError(e)

    def __call__(self):
        return SubmissionNode(self.file)
