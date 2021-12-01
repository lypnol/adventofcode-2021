from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
      r = 0
      t = s.splitlines()
      for i in range(len(t)):
        if i < 3:
          continue
        if int(t[i]) > int(t[i-3]):
          r += 1
      return r
