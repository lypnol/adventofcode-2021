from tool.runners.python import SubmissionPy
from collections import defaultdict

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    d = defaultdict(list)
    b = defaultdict(bool)
    for i in s.splitlines():
      [j,k] = i.split("-")
      d[j].append(k)
      d[k].append(j)
      if j.upper() == j:
        b[j] = True
      if k.upper() == k:
        b[k] = True

    def parkour(s, w, t):
      w = set(w)
      w.add(s)
      r = 0
      for i in d[s]:
        if i == "end":
          r += 1
          continue
        if i in w and not b[i]:
          if not t and i != "start":
            r += parkour(i, w, True)
          continue
        r += parkour(i, w, t)
      return r
        

    return parkour("start", set(), False)
