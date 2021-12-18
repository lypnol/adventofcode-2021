from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):
    def find_vx0s(self, x1, x2):
        result = set()
        for vx0 in range(1, x2+1):
            x = 0
            vx = vx0
            for _ in range(vx0+1):
                if x > x2:
                    break
                if x1 <= x:
                    result.add(vx0)
                    break
                x += vx
                if vx > 0:
                    vx -= 1
                elif vx < 0:
                    vx += 1
        return result

    def reaches_target(self, vx0, vy0, x1, x2, y1, y2):
        vx = vx0
        vy = vy0
        x, y = (0,0)

        while y >= y1:
            if x1 <= x <= x2 and y1 <= y <= y2:
                return True
            x += vx
            y += vy
            vy -= 1
            if vx > 0:
                vx -= 1
            elif vx < 0:
                vx += 1

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        # target area: x=96..125, y=-144..-98
        # target area: x=20..30, y=-10..-5

        x1,x2 = (96,125)
        y1,y2 = (-144,-98)
        # x1,x2 = (20,30)
        # y1,y2 = (-10,-5)

        vx0s = self.find_vx0s(x1,x2)
        vy0 = 1
        result = 0
        for vy0 in range(-300,600):
            c =  sum(1 for vx0 in vx0s if self.reaches_target(vx0,vy0,x1,x2,y1,y2))
            result += c
        return result

def test_div():
    """
    Run `python -m pytest ./day-17/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
