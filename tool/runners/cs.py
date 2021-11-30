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
        subprocess.run(["cp", "aoc.csproj", self.temporary_directory])
        subprocess.run(["cp", file, self.temporary_directory])
        self.file = file

    def language(self):
        return "cs"

    def exec(self, input):
        try:
            return subprocess.check_output(
                [
                    "dotnet", 
                    "run", 
                    "--project", 
                    os.path.join(self.temporary_directory, "aoc.csproj"),
                    "--",
                    input
                ]
            ).decode()
        except OSError as e:
            if e.errno == errno.ENOENT:
                # executable not found
                return CompilationError(e)
            else:
                # subprocess exited with another error
                return RuntimeError(e)
        except subprocess.CalledProcessError as e:
            print(e.output.decode())

    def __call__(self):
        return SubmissionCs(self.file)