from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
      L = [[0 for _ in range(1000)] for _ in range(1000)]
      r = 0
      for i in s.splitlines():
        [a,b] = [j.strip() for j in i.split("->")]
        [a1,b1] = a.split(",")
        [a2,b2] = b.split(",")
        x1 = int(a1)
        x2 = int(a2)
        y1 = int(b1)
        y2 = int(b2)
        if x1 == x2:
          if y1 > y2:
            y1,y2 = y2,y1
          for k in range(y1,y2+1):
            if L[x1][k] == 1:
              r += 1
              L[x1][k] = -1
              continue
            if L[x1][k] == 0:
              L[x1][k] = 1
        if y1 == y2:
          if x1 > x2:
            x1,x2 = x2,x1
          for k in range(x1,x2+1):
            if L[k][y1] == 1:
              r += 1
              L[k][y1] = -1
              continue
            if L[k][y1] == 0:
              L[k][y1] = 1
        else:
          if x2 < x1:
            x1,x2 = x2,x1
            y1,y2 = y2,y1
          if x2 > x1:
            if y2 > y1:
              for i in range(x2-x1+1):
                if L[x1+i][y1+i] == 1:
                  r += 1
                  L[x1+i][y1+i] = -1
                if L[x1+i][y1+i] == 0:
                  L[x1+i][y1+i] = 1
            if y2 < y1:
              for i in range(x2-x1+1):
                if L[x1+i][y1-i] == 1:
                  r += 1
                  L[x1+i][y1-i] = -1
                if L[x1+i][y1-i] == 0:
                  L[x1+i][y1-i] = 1
      return r