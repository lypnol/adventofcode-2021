from tool.runners.python import SubmissionPy
from statistics import median

class FrenkiSubmission(SubmissionPy):
  def run(self,s):
    d = [int(i) for i in s.split(",")]
    m = int(median(d))
    r = 0
    for i in d:
      r += abs(m-i)
    return r

      
