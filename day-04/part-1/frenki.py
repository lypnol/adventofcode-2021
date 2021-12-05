from tool.runners.python import SubmissionPy

class Grid:
  def __init__(self):
    self.values = {}
    self.marked = [[False for i in range(5)] for i in range(5)]

  def add(self, value, x, y):
    self.values[value] = (x,y)
  
  def hasWon(self, x, y):
    return all(self.marked[x][i] for i in range(5)) or all(self.marked[i][y] for i in range(5))

  def mark(self, value):
    if not value in self.values.keys():
      return False
    (x,y) = self.values[value]
    self.marked[x][y] = True
    return self.hasWon(x,y)
  
  def score(self):
    r = 0
    for k in self.values.keys():
      (x,y) = self.values[k]
      if not self.marked[x][y]:
        r += int(k)
    return r

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    d = s.splitlines()
    v = d[0].split(",")
    g = []
    for i in d[1:]:
      if i == "":
        g.append(Grid())
        x = -1
      else:
        x += 1
        k = [j for j in i.split(" ") if j != ""]
        for y in range(5):
          g[-1].add(k[y], x, y)

    for i in v:
      for r in g:
        if r.mark(i):
          return int(i) * r.score()
