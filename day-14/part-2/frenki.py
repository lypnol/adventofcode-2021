from tool.runners.python import SubmissionPy
from collections import defaultdict

class FrenkiSubmission(SubmissionPy):
  def run(self,s):
    c = s.splitlines()
    a = c[0]
    b = c[2:]
    d = defaultdict(int)
    for i in range(len(a) - 1):
      d[a[i:i+2]] += 1

    L = []
    for j in b:
      L.append(j.split(" -> "))

    for _ in range(40):
      d2 = d.copy()
      for [p,q] in L:
        if p in d.keys():
          d2[p] -= d[p]
          d2[p[0] + q] += d[p]
          d2[q + p[1]] += d[p]
      d = d2

    v = defaultdict(int)
    for i in d.keys():
      v[i[0]] += d[i]
    v[a[-1]] += 1

    return max(i for i in v.values()) - min(i for i in v.values())
