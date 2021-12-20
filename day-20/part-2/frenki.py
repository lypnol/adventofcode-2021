from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    data = s.splitlines()
    algorithm = data[0]
    image = data[2:]
    height = len(image)
    width = len(image[0])

    for i in range(height):
      image[i] = ".." + image[i] + ".."

    image = ["."*(width + 4)] * 2 + image + ["."*(width + 4)] * 2

    def compute(i,j):
      raw = image[i-1][j-1:j+2] + image[i][j-1:j+2] + image[i+1][j-1:j+2]
      computed = ""
      for k in raw:
        if k == "#":
          computed += "1"
        else:
          computed += "0"

      return algorithm[int(computed, 2)]

    for counter in range(49):
      if counter % 2 == 1 or algorithm[0] == ".":
        temp = ["." * (width + 2 * counter + 6)] * 2
      else:
        temp = ["#" * (width + 2 * counter + 6)] * 2

      for i in range(1, height + 3 + 2 * counter):
        if counter % 2 == 1 or algorithm[0] == ".":
          line = ".."
        else:
          line = "##"

        for j in range(1, width + 3 + 2 * counter):
          line += compute(i,j)

        if counter % 2 == 1 or algorithm[0] == ".":
          line += ".."
        else:
          line += "##"

        temp.append(line)

      if counter % 2 == 1 or algorithm[0] == ".":
        temp += ["." * (width + 2 * counter + 6)] * 2
      else:
        temp += ["#" * (width + 2 * counter + 6)] * 2

      image = temp

    result = 0
    for i in range(1, height + 101):
      for j in range(1, width + 101):
        if compute(i,j) == "#":
          result += 1
    return result