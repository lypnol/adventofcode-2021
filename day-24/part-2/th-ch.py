from tool.runners.python import SubmissionPy

from collections import deque


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Program is made up of 14 blocks starting with an input and having parameters
        blocks = []
        for block in s.split("inp w")[1:]:
            instructions = block.splitlines()
            # p1 is 1 or 26
            p1 = int(instructions[4].replace("div z ", ""))
            # p2 is >= 10 or < 0
            p2 = int(instructions[5].replace("add x ", ""))
            # p3 is > 0 and <= 16
            p3 = int(instructions[15].replace("add y ", ""))
            blocks.append((p1, p2, p3))
            #### For each block, one input (inp) then z computation will be:
            # if (z % 26 + p2) == inp:
            #     z = z // p1
            # else:
            #     z = (z // p1) * 26 + inp + p3
            #############################
            # If p2 > 0: p2 >= 10 so condition is false (1 <= inp <= 9)
            #   And if p2 > 0 then p1 = 1 all the time
            #   So z = 26 * z + inp + p3
            #   p3 > 0 so z is strictly growing
            #       => need the condition to be true to lower the value towards 0
            # else: (p2 <= 0 and so p1 == 26)
            #   The condition (26 * z + prev_inp + prev_p3) % 26 + p2 == inp need to be true to lower z
            #   Condition can be re-written as (prev_inp + prev_p3) % 26 + p2 == inp
            #   0 < prev_p3 <= 16 and 1 <= prev_inp <= 9 so we can remove the modulo:
            #   Condition is: prev_inp + (prev_p3 + p2) == inp
            #   So delta between inp and prev_inp is prev_p3 + p2

        constraints = {}
        p2_greater_than_0 = deque()
        for inp, (p1, p2, p3) in enumerate(blocks):
            if p2 > 0:
                p2_greater_than_0.appendleft((inp, p3))
            else:
                prev_inp, prev_p3 = p2_greater_than_0.popleft()
                constraints[inp] = (prev_inp, prev_p3 + p2)

        # There are 7 blocks with p2 > 0 and 7 with p2 <= 0 so the stack `p2_greater_than_0` will be empty
        # And we will have 7 constraints
        values = [None] * 14
        for inp, (prev_inp, delta) in constraints.items():
            # We always have prev_inp before inp
            # To get the smallest model number, we need prev_inp as small as possible
            # inp will be (prev_inp + delta) which must be in [1, 9] and 1 <= prev_inp <= 9
            # So 1 <= prev_inp + delta <= 9
            #    1 - delta <= prev_inp <= 9 - delta, with 1 <= prev_inp <= 9
            #    So smallest possible value for prev_inp is max(1 - delta, 1)
            #    And then inp = prev_inp + delta
            #             inp = max(1 - delta, 1) + delta
            #             inp = max(1, 1 + delta)
            ########
            values[prev_inp] = max(1 - delta, 1)
            values[inp] = max(1, 1 + delta)

        return "".join(map(str, values))
