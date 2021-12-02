from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
      h = 0
      d = 0
      for n in s.splitlines():
        i, v = n.split(" ")
        if i == "forward":
          h += int(v)
        elif i == "down":
          d += int(v)
        else:
          d -= int(v)
      return d * h
