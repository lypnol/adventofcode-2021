from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    r = 0
    l = {")": "(", "]": "[", "}": "{", ">": "<"}
    v = {")": 3, "]": 57, "}": 1197, ">": 25137}
    for i in s.splitlines():
      a = ""
      # d = {"(": 0, "[": 0, "{": 0, "<": 0}
      for c in i:
        if c in l.keys():
          if len(a) == 0 or l[c] != a[-1]:
            r += v[c]
            break
          a = a[:-1]
          continue
        a += c
        # if c in d.keys():
        #   d[c] += 1
        #   continue
        # a = l[c]
        # if d[a] == 0:
        #   r += v[c]
        #   break
        # d[a] -= 1
    return r
