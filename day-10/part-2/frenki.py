from tool.runners.python import SubmissionPy

from statistics import median

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    r = []
    l = {")": "(", "]": "[", "}": "{", ">": "<"}
    d = {"(": 1, "[": 2, "{": 3, "<": 4}
    for i in s.splitlines():
      a = ""
      for c in i:
        if c in l.keys():
          if len(a) == 0 or l[c] != a[-1]:
            a = ""
            break
          a = a[:-1]
          continue
        a += c
      if a != "":
        v = 0
        for j in range(len(a)-1, -1, -1):
          v *= 5
          v += d[a[j]]
        r.append(v)
    return median(r)