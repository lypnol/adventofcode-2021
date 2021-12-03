from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
      M = []
      L = []
      A = []
      B = []
      for i in s.splitlines():
        if i[0] == "1":
          A.append(i)
        else:
          B.append(i)
      if len(A) >= len(B):
        M = A
        L = B
      else:
        M = B
        L = A
      A = []
      B = []
      c = 1
      while len(M) > 1:
        for i in M:
          if i[c] == "1":
            A.append(i)
          else:
            B.append(i)
        if len(A) >= len(B):
          M = A
        else:
          M = B
        A = []
        B = []
        c += 1
      c = 1
      while len(L) > 1:
        for i in L:
          if i[c] == "1":
            A.append(i)
          else:
            B.append(i)
        if len(A) < len(B):
          L = A
        else:
          L = B
        A = []
        B = []
        c += 1
      return int(L[0], 2) * int(M[0], 2)
