from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self,s):
    d = s.splitlines()
    m = len(d)
    n = len(d[0])
    v = [[int(d[i][j]) for j in range(n)] for i in range(m)]
    L = [[0 for _ in range(n)] for _ in range(m)]

    def correct(i,j,d,b,g,h):
      if d and j < n-1:
        r = L[i][j] + v[i][j+1]
        if r < L[i][j+1]:
          L[i][j+1] = r
          correct(i,j+1, True, True, False, True)
      if g and j > 0:
        r = L[i][j] + v[i][j-1]
        if r < L[i][j-1]:
          L[i][j-1] = r
          correct(i,j-1, False, True, True, True)
      if b and i < m-1:
        r = L[i][j] + v[i+1][j]
        if r < L[i+1][j]:
          L[i+1][j] = r
          correct(i+1,j, True, True, True, False)
      if h and i > 0:
        r = L[i][j] + v[i-1][j]
        if r < L[i-1][j]:
          L[i-1][j] = r
          correct(i-1,j, True, False, True, True)


    L[-1][-1] = v[-1][-1]
    for i in range(m-2, -1, -1):
      L[i][-1] = v[i][-1] + L[i+1][-1]
    for j in range(n-2, -1, -1):
      L[-1][j] = v[-1][j] + L[-1][j+1]

    for i in range(m-2, -1, -1):
      for j in range(n-2, -1, -1):
        L[i][j] = v[i][j] + min(L[i+1][j], L[i][j+1])
        correct(i,j, True, True, False, False)

    return L[0][0] - v[0][0]
