from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    d = s.splitlines()
    p = d[0]
    L = d[2:]
    m = len(L)
    n = len(L[0])
    a1 = "."*(102 + n)
    a2 = "#"*(102 + n)

    for i in range(m):
      L[i] = "."*51 + L[i] + "."*51

    L = [a1 for _ in range(51)] + L + [a1 for _ in range(51)]

    def compute(i,j):
      a = L[i-1][j-1:j+2]
      b = L[i][j-1:j+2]
      c = L[i+1][j-1:j+2]
      d = a+b+c
      e = ""
      for k in d:
        if k == "#":
          e += "1"
        else:
          e += "0"
      return p[int(e, 2)]

    for k in range(49):
      if k % 2 == 1 or p[0] == ".":
        L2 = [a1 for _ in range(49 - k)]
      else:
        L2 = [a2 for _ in range(49 - k)]
      for i in range(49 - k, m + 53 + k):
        if k % 2 == 1 or p[0] == ".":
          v = "."*(49-k)
        else:
          v = "#"*(49-k)
        for j in range(49 - k, n + 53 + k):
          v += compute(i,j)
        if k % 2 == 1 or p[0] == ".":
          v += "."*(49-k)
        else:
          v += "#"*(49-k)
        L2.append(v)
      if k % 2 == 1 or p[0] == ".":
        L2 += [a1 for _ in range(49 - k)]
      else:
        L2 += [a2 for _ in range(49 - k)]
      L = L2

    r = 0
    for i in range(1, m + 101):
      for j in range(1, n + 101):
        if compute(i,j) == "#":
          r += 1
    return r