from tool.runners.python import SubmissionPy
from collections import defaultdict

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    i = 15
    x1 = ""
    x2 = ""
    y1 = ""
    y2 = ""
    while s[i] != ".":
      x1 += s[i]
      i += 1
    i += 2
    while s[i] != ",":
      x2 += s[i]
      i += 1
    i += 4
    while s[i] != ".":
      y1 += s[i]
      i += 1
    i += 2
    y2 = s[i:]
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)

    d = defaultdict(list)
    c = defaultdict(list)
    e = defaultdict(int)

    for i in range(x2+1):
      if i * (i+1) // 2 < x1:
        continue
      v = 0
      j = i
      s = 0
      while v < x1:
        v += j
        j -= 1
        s += 1
      while v <= x2 and j > 0:
        d[i].append(s)
        v += j
        j -= 1
        s += 1
      if j == 0:
        e[i] = s
    
    for i in range(y1, -y1 + 1):
      v = 0
      j = i
      s = 0
      while v > y2:
        v += j
        j -= 1
        s += 1
      while v >= y1:
        c[i].append(s)
        v += j
        j -= 1
        s += 1
        

    r = 0
    for j in c.keys():
      for i in d.keys():
        t = False
        for a in c[j]:
          for b in d[i]:
            if a == b:
              t = True
              break
          if t:
            break
        if t:
          r += 1
      for i in e.keys():
        t = True
        for a in c[j]:
          if a < e[i]:
            t = False
            break
        if t:
          r += 1
    return r