from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    i = 20
    t = ""
    while s[i] != "y":
      i += 1
    i += 2
    while s[i] != ".":
      t += s[i]
      i += 1
    return (int(t)* (int(t) + 1))//2
