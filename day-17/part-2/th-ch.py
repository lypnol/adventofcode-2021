from tool.runners.python import SubmissionPy


class Target:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def has_missed(self, x, y, v_x, v_y):
        return x > self.x_max or (y < self.y_min and v_y <= 0)

    def is_in(self, x, y):
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max


class ThChSubmission(SubmissionPy):
    def launch(self, v_x, v_y, target):
        x, y = v_x, v_y
        while not target.is_in(x, y):
            v_x = v_x - 1 if v_x > 0 else (v_x + 1 if v_x < 0 else 0)
            v_y -= 1
            x += v_x
            y += v_y
            if target.has_missed(x, y, v_x, v_y):
                return False, x, y

        return True, x, y

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        x_coords, y_coords = s.replace("target area: ", "").split(", ")
        x_min, x_max = x_coords.replace("x=", "").split("..")
        y_min, y_max = y_coords.replace("y=", "").split("..")
        x_min, x_max, y_min, y_max = int(x_min), int(x_max), int(y_min), int(y_max)
        target = Target(x_min, x_max, y_min, y_max)

        v_x = 0
        nb_initial_velocities_ok = 0
        while True:
            if (v_x + 1) * (v_x) // 2 < x_min + 1:
                v_x += 1
                continue  # cannot reach the target

            v_y = y_min
            while True:
                in_target, x, y = self.launch(v_x, v_y, target)

                if not in_target:
                    if x < x_min:
                        v_y += 1
                        continue
                    elif v_y > abs(y_max) or x > x_max:
                        break
                else:
                    nb_initial_velocities_ok += 1
                v_y += 1

            v_x += 1
            if v_x > x_max:
                break

        return nb_initial_velocities_ok


def test_th_ch():
    """
    Run `python -m pytest ./day-17/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
target area: x=20..30, y=-10..-5
""".strip()
        )
        == 112
    )
