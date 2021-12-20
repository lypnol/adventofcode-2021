from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    d = s.splitlines()
    p = d[0]
    L = d[2:]
    m = len(L)
    n = len(L[0])
    a1 = "."*(n+6)
    a2 = "#"*(n+6)

    for i in range(m):
      L[i] = "..." + L[i] + "..."

    L = [a1,a1,a1] + L + [a1,a1,a1]

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

    if p[0] == ".":
      L2 = [a1]
    else:
      L2 = [a2]
    for i in range(1, m + 5):
      v = p[0]
      for j in range(1, n + 5):
        v += compute(i,j)
      v += p[0]
      L2.append(v)
    if p[0] == ".":
      L2 += [a1]
    else:
      L2 += [a2]
    L = L2

    r = 0
    for i in range(1, m + 5):
      for j in range(1, n + 5):
        if compute(i,j) == "#":
          r += 1
    return r