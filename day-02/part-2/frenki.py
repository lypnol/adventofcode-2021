from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
      h = 0
      d = 0
      a = 0
      for n in s.splitlines():
        i, v = n.split(" ")
        if i == "forward":
          c = int(v)
          h += c
          d += c * a
        elif i == "down":
          a += int(v)
        else:
          a -= int(v)
      return d * h
