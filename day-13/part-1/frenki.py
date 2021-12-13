from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    d = {}
    for i in s.splitlines():
      if len(i) <= 10:
        if i == "":
          continue
        [x,y] = i.split(",")
        d[(x,y)] = "#"
        continue
      [_,_,c] = i.split(" ")
      [l,p] = c.split("=")
      break
    r = 0
    p = int(p)

    if l == "x":
      for (y,x) in d.keys():
        if int(y) < p and (str(2 * p - int(y)), x) in d.keys():
          continue
        r += 1

    if l == "y":
      for (y,x) in d.keys():
        if int(x) < p and (y, str(2 * p - int(x))) in d.keys():
          continue
        r += 1
    return r