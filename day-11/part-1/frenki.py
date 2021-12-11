from tool.runners.python import SubmissionPy

def flash(L,i, j):
  L[i][j] = -1
  r = 1
  if i > 0:
    if j > 0:
      if L[i-1][j-1] != -1:
        L[i-1][j-1] += 1
        if L[i-1][j-1] == 10:
          L, p = flash(L, i-1, j-1)
          r += p
    if j < 9:
      if L[i-1][j+1] != -1:
        L[i-1][j+1] += 1
        if L[i-1][j+1] == 10:
          L, p = flash(L, i-1, j+1)
          r += p
    if L[i-1][j] != -1:
      L[i-1][j] += 1
      if L[i-1][j] == 10:
        L, p = flash(L, i-1, j)
        r += p
  if i < 9:
    if j > 0:
      if L[i+1][j-1] != -1:
        L[i+1][j-1] += 1
        if L[i+1][j-1] == 10:
          L, p = flash(L, i+1, j-1)
          r += p
    if j < 9:
      if L[i+1][j+1] != -1:
        L[i+1][j+1] += 1
        if L[i+1][j+1] == 10:
          L, p = flash(L, i+1, j+1)
          r += p
    if L[i+1][j] != -1:
      L[i+1][j] += 1
      if L[i+1][j] == 10:
        L, p = flash(L, i+1, j)
        r += p
  if j > 0:
    if L[i][j-1] != -1:
      L[i][j-1] += 1
      if L[i][j-1] == 10:
        L, p = flash(L, i, j-1)
        r += p
  if j < 9:
    if L[i][j+1] != -1:
      L[i][j+1] += 1
      if L[i][j+1] == 10:
        L, p = flash(L, i, j+1)
        r += p
  return L, r

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    r = 0
    L = [[int(i[j]) for j in range(10)] for i in s.splitlines()]
    for _ in range(100):
      for i in range(10):
        for j in range(10):
          if L[i][j] != -1:
            L[i][j] += 1
            if L[i][j] == 10:
              L, p = flash(L, i, j)
              r += p
      for i in range(10):
        for j in range(10):
          if L[i][j] == -1:
            L[i][j] = 0
    return r
