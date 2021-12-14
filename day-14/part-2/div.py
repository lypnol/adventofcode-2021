from tool.runners.python import SubmissionPy

from collections import Counter

class DivSubmission(SubmissionPy):
    STEPS = 40

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

        # dynamic programming!
        # we're going to compute the multiset of elements inserted by each pair rule step by step

        counter_by_pair = dict() # key (pair, n) -> value: multiset of elements inserted by the PAIR after n steps
        for pair, child in insertions.items():
            counter_by_pair[(pair,0)] = Counter([child])

        for step in range(1, self.STEPS):
            for pair in insertions:
                # the pair AC creates the element B
                b = insertions[pair]
                a,c = pair

                # the multiset is made of B
                counter = Counter([b])
                # and the multiset created by the pair AB with one less step
                if (a,b) in insertions:
                    counter += counter_by_pair[((a,b), step-1)]
                # and the multiset created by the pair AC with one less step
                if (b,c) in insertions:
                    counter += counter_by_pair[((b,c), step-1)]
                counter_by_pair[(pair, step)] = counter

        # now we just have to merge the multisets from the pairs in the template
        all_counter = Counter(list(template))
        for pair in zip(template, template[1:]):
            if pair in insertions:
                all_counter += counter_by_pair[(pair, self.STEPS-1)]

        return max(all_counter.values()) - min(all_counter.values())

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
