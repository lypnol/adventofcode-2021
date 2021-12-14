from tool.runners.python import SubmissionPy

from collections import Counter

class DivSubmission(SubmissionPy):
    STEPS = 10
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        blocks = s.split("\n\n")
        template = blocks[0]

        rules = blocks[1].split("\n")
        insertions = dict()
        for rule in rules:
            left, right = rule.split(" -> ")
            x,y = list(left)
            insertions[(x,y)] = right

        for _ in range(self.STEPS):
            new_template = ""
            for a,b in zip(template, template[1:]):
                new_template += a
                if (a,b) in insertions:
                    new_template += insertions[(a,b)]
            new_template += template[-1]
            template = new_template

        counter = Counter(new_template)
        return max(counter.values()) - min(counter.values())




def test_div():
    """
    Run `python -m pytest ./day-14/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
