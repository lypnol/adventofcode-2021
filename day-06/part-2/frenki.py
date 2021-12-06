from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    d = {
      "0": 0,
      "1": 0,
      "2": 0,
      "3": 0,
      "4": 0,
      "5": 0,
      "6": 0,
      "7": 0,
      "8": 0
    }
    for i in s.split(","):
      d[i] += 1

    return d["0"] * 6703087164 + d["1"] * 6206821033 + d["2"] * 5617089148 + d["3"] * 5217223242 + d["4"] * 4726100874 + d["5"] * 4368232009 + d["6"] * 3989468462 + d["7"] * 3649885552 + d["8"] * 3369186778