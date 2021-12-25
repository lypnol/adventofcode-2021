from tool.runners.python import SubmissionPy


def roll_dice(last_value):
    if last_value >= 100:
        return 1
    return last_value + 1


def move_to_position(start_position, move):
    position = start_position + move
    while position > 10:
        position -= 10
    return position


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        players = []
        # Your code goes here
        for line in s.splitlines():
            line = line.replace("Player ", "")
            player, start_position = line.split(" starting position: ")
            players.append({
                "score": 0,
                "position": int(start_position),
                "name": player,
            })

        current_player_index = 0
        dice = 0
        is_won = False
        nb_times_die_rolled = 0

        while not is_won:
            move = 0
            for _ in range(3):
                move += roll_dice(dice)
                dice += 1
                nb_times_die_rolled += 1
                if dice > 100:
                    dice = 1
            players[current_player_index]["position"] = move_to_position(
                players[current_player_index]["position"], move)
            players[current_player_index]["score"] += players[
                current_player_index]["position"]

            if players[current_player_index]["score"] >= 1000:
                is_won = True

            current_player_index = (current_player_index + 1) % len(players)

        loser_score = players[current_player_index]["score"]

        return loser_score * nb_times_die_rolled


def test_th_ch():
    """
    Run `python -m pytest ./day-21/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
Player 1 starting position: 4
Player 2 starting position: 8
""".strip()) == 739785)
