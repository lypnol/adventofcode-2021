from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
      G = [0 for _ in range(12)]
      E = [0 for _ in range(12)]
      for i in s.splitlines():
        for l in range(len(i)):
          if i[l] == "0":
            G[l] += 1
          else:
            E[l] += 1
      a = 0
      b = 0
      for i in range(12):
        if G[i] > E[i]:
          a += 2**(12 - i - 1)
        else:
          b += 2**(12 - i - 1)
        
      return a * b
