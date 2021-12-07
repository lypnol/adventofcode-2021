from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self,s):
    d = [int(i) for i in s.split(",")]
    v = sum(d)
    m = int(v / len(d))
    r1 = 0
    r2 = 0
    for i in d:
      a1 = abs(m-i)
      a2 = abs(m+1-i)
      r1 += a1*(a1+1)//2
      r2 += a2*(a2+1)//2
    return min(r1,r2)