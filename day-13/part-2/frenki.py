from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    d = {}
    t = []
    for i in s.splitlines():
      if len(i) <= 10:
        if i == "":
          continue
        [x,y] = i.split(",")
        d[(x,y)] = "#"
        continue

      [_,_,c] = i.split(" ")
      [l,p] = c.split("=")
      t.append([l, int(p)])
    r = 0

    for [l,p] in t:
      n = d.copy()
      if l == "x":
        for (y,x) in n.keys():
          if int(y) > p:
            d[(str(2 * p - int(y)), x)] = "#"
            d.pop((y,x))
          

      if l == "y":
        for (y,x) in n.keys():
          if int(x) > p:
            d[(y, str(2 * p - int(x)))] = "#"
            d.pop((y,x))

    res = []
    for r in range(max(int(y) for (_,y) in d) + 1):
      res.append("".join("#" if (str(x),str(r)) in d else "." for x in range(max(int(v) for (v,_) in d)+2)))
    return "\n".join(res)