from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    d = {"0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101", "6": "0110", "7": "0111", "8": "1000", "9": "1001", "A": "1010", "B": "1011", "C": "1100", "D": "1101", "E": "1110", "F": "1111"}
    f = {"000": 0, "001": 1, "010": 2, "011": 3, "100": 4, "101": 5, "110": 6, "111": 7}
    v = ""
    for i in s:
      v += d[i]

    def compute(o, a):
      if o == 0:
        return sum(a)
      if o == 1:
        r = 1
        for i in a:
          r *= i
        return r
      if o == 2:
        return min(a)
      if o == 3:
        return max(a)
      if o == 5:
        if a[0] > a[1]:
          return 1
        return 0
      if o == 6:
        if a[0] < a[1]:
          return 1
        return 0
      if o == 7:
        if a[0] == a[1]:
          return 1
        return 0

    def readLitteral(i):
      b = ""
      while v[i] == "1":
        i += 1
        b += v[i:i+4]
        i += 4
      i += 1
      b += v[i:i+4]
      i += 4
      return i, int(b,2)

    def readOperator(i):
      o = f[v[i:i+3]]
      i += 3
      a = []
      if v[i] == "0":
        i += 1
        n = int(v[i:i+15], 2)
        i += 15
        j = i + n
        while i < j:
          i += 3
          if v[i:i+3] == "100":
            i, k = readLitteral(i+3)
            a.append(k)
          else:
            i, k = readOperator(i)
            a.append(k)
      else:
        i += 1
        m = int(v[i:i+11], 2)
        i += 11
        while m > 0:
          i += 3
          if v[i:i+3] == "100":
            i, k = readLitteral(i+3)
            a.append(k)
          else:
            i, k = readOperator(i)
            a.append(k)
          m -= 1

      return i, compute(o,a)

    i = 0
    r = 0
    # while i < len(v):
    r += f[v[i:i+3]]
    i += 3
    if v[i:i+3] == "100":
      i,n = readLitteral(i+3)
      r = n
    else:
      i,p = readOperator(i)
      r = p
    return r


