from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    d = {"0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101", "6": "0110", "7": "0111", "8": "1000", "9": "1001", "A": "1010", "B": "1011", "C": "1100", "D": "1101", "E": "1110", "F": "1111"}
    f = {"000": 0, "001": 1, "010": 2, "011": 3, "100": 4, "101": 5, "110": 6, "111": 7}
    v = ""
    for i in s:
      v += d[i]

    def readLitteral(i):
      while v[i] == "1":
        i += 5
      i += 5
      return i      

    def readOperator(i):
      p = 0
      if v[i] == "0":
        i += 1
        n = int(v[i:i+15], 2)
        i += 15
        j = i + n
        while i < j:
          p += f[v[i:i+3]]
          i += 3
          if v[i:i+3] == "100":
            i = readLitteral(i+3)
          else:
            i, k = readOperator(i+3)
            p += k
      else:
        i += 1
        m = int(v[i:i+11], 2)
        i += 11
        while m > 0:
          p += f[v[i:i+3]]
          i += 3
          if v[i:i+3] == "100":
            i = readLitteral(i+3)
          else:
            i, k = readOperator(i+3)
            p += k
          m -= 1
      return i, p



    i = 0
    r = 0
    # while i < len(v):
    r += f[v[i:i+3]]
    i += 3
    if v[i:i+3] == "100":
      i = readLitteral(i+3)
    else:
      i,p = readOperator(i+3)
      r += p
    return r


