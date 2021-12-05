from tool.runners.python import SubmissionPy


class ManutSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        f = s.split('\n')
        count = dict()
        res = 0
        for line in f:
            line = line.split(' ')
            if len(line) == 1:
                continue
            first_pos = line[0].split(',')
            second_pos = line[2].split(',')
            # print(first_pos)
            # print(second_pos)
            if (first_pos[0] == second_pos[0]):
                max_pos = max(int(first_pos[1]), int(second_pos[1]))
                min_pos = min(int(first_pos[1]), int(second_pos[1]))
                for i in range(min_pos, max_pos+1):
                    key = str(first_pos[0]) +","+ str(i)
                    # print(key)
                    if count.get(key, "0") == 1:
                        res += 1
                    count[key] = count.get(key, 0) + 1
            elif (first_pos[1] == second_pos[1]):
                max_pos = max(int(first_pos[0]), int(second_pos[0]))
                min_pos = min(int(first_pos[0]), int(second_pos[0]))
                for i in range(min_pos, max_pos+1):
                    key = str(i) +','+ str(first_pos[1])
                    # print(key)
                    if count.get(key, "0") == 1:
                        res += 1
                    count[key] = count.get(key, 0) + 1
            # print(count)
        return res


def test_manut():
    """
    Run `python -m pytest ./day-05/part-1/manut.py` to test the submission.
    """
    assert (
        ManutSubmission().run(
            """
""".strip()
        )
        == None
    )
