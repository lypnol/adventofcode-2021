import os
import errno
import subprocess
import tempfile

from tool.runners.exceptions import CompilationError, RuntimeError
from tool.runners.wrapper import SubmissionWrapper


class SubmissionCs(SubmissionWrapper):
    def __init__(self, file):
        SubmissionWrapper.__init__(self)
        # Create a temporary directory to put the compiled java in,
        # in order to have it destroyed once we are done
        self.temporary_directory = tempfile.mkdtemp(prefix="aoc")
        try:
            subprocess.run(["cp", "aoc.csproj", self.temporary_directory], check=True)
            subprocess.run(["cp", file, self.temporary_directory], check=True)
            subprocess.run(
                [
                    "dotnet", 
                    "build", 
                    os.path.join(self.temporary_directory, "aoc.csproj"), 
                    "--output",
                    os.path.join(self.temporary_directory, "bin")
                ],
                check=True,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError as e:
            raise CompilationError(e)
        self.executable = os.path.join(self.temporary_directory, "bin", "aoc")
        self.file = file

    def language(self):
        return "cs"

    def exec(self, input):
        try:
            return subprocess.check_output([self.executable, input]).decode()
        except OSError as e:
            if e.errno == errno.ENOENT:
                # executable not found
                raise CompilationError(e)
            else:
                # subprocess exited with another error
                raise RuntimeError(e)

    def __call__(self):
        return SubmissionCs(self.file)