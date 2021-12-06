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

    return d["0"] * 1421 +d["1"] * 1401 + d["2"] * 1191 + d["3"] * 1154 + d["4"] * 1034 + d["5"] * 950 + d["6"] * 905 + d["7"] * 779 + d["8"] * 768