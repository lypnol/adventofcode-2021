from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
      r = -1
      p = -1
      for i in s.splitlines():
        v = int(i)
        if v > p:
          r += 1
        p = v
      return r
