from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    r = 0
    for i in s.splitlines():
      d = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}
      l = {2: [], 3: [], 4: [], 5: [], 6: [], 7:[]}
      j = i.split("|")
      for k in j[0].strip().split(" "):
        l[len(k)].append(k)
      d[1] = l[2][0]
      d[4] = l[4][0]
      d[7] = l[3][0]
      d[8] = l[7][0]
      for i in l[5]:
        s1 = 0
        s4 = 0
        for n in i:
          if n in d[1]:
            s1 += 1
          if n in d[4]:
            s4 += 1
        if s4 == 2:
          d[2] = i
          continue
        if s1 == 2:
          d[3] = i
          continue
        d[5] = i
      for i in l[6]:
        s1 = 0
        s4 = 0
        for n in d[1]:
          if n in i:
            s1 += 1
        for n in d[4]:
          if n in i:
            s4 += 1
        if s1 == 1:
          d[6] = i
          continue
        if s4 == 3:
          d[0] = i
          continue
        d[9] = i
      
      a = 0
      v = {2: [1], 3: [7], 4: [4], 5: [2,3,5], 6: [0,6,9], 7: [8]}
      b = j[1].strip().split(" ")
      for k in range(len(b)):
        le = len(b[k])
        u = v[le]
        if len(u) == 1:
          a += u[0] * 10**(3-k)
          continue
        for i in u:
          s = le
          for j in b[k]:
            if j in d[i]:
              s -= 1
          if s == 0:
            a += i * 10**(3-k)
            break
      r += a
    return r
