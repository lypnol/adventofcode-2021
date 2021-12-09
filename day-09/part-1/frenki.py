from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    r = 0
    sp = s.splitlines()
    l = len(sp)
    for i in range(l):
      k = sp[i]
      l2 = len(k)
      for j in range(l2):
        v = int(k[j])
        if i > 0 and int(sp[i-1][j]) <= v:
          continue
        if i < l - 1 and int(sp[i+1][j]) <= v:
          continue
        if j > 0 and int(k[j-1]) <= v:
          continue
        if j < l2 - 1 and int(k[j+1]) <= v:
          continue
        r += 1 + v
    return r

