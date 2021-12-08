from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    r = 0
    for i in s.splitlines():
      j = i.split("|")[1].strip().split(" ")
      for k in j:
        if len(k) in [2,3,4,7]:
          r += 1
    return r