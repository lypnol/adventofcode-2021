from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self,s):
    r = [0,0,0]
    p = [[k for k in j] for j in s.splitlines()]
    l = len(p)
    for i in range(l):
      k = p[i]
      l2 = len(k)
      for j in range(l2):
        if k[j] in ["9", "-"]:
          continue
        k[j] = "-"
        v = [(i,j)]
        a = 1
        while len(v) > 0:
          (x,y) = v[0]
          v = v[1:]
          if x < l - 1:
            if p[x+1][y] not in ["9", "-"]:
              p[x+1][y] = "-"
              v.append((x+1,y))
              a += 1
          if x > 0:
            if p[x-1][y] not in ["9", "-"]:
              p[x-1][y] = "-"
              v.append((x-1,y))
              a += 1
          if y < l2 - 1:
            if p[x][y+1] not in ["9", "-"]:
              p[x][y+1] = "-"
              v.append((x,y+1))
              a += 1
          if y > 0:
            if p[x][y-1] not in ["9", "-"]:
              p[x][y-1] = "-"
              v.append((x,y-1))
              a += 1
        if a > r[0]:
          if a > r[1]:
            if a > r[2]:
              r = [r[1], r[2], a]
              continue
            r = [r[1], a, r[2]]
            continue
          r = [a, r[1], r[2]]
    return r[0] * r[1] * r[2]

