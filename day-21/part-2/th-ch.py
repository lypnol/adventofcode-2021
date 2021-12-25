from tool.runners.python import SubmissionPy

from functools import lru_cache


@lru_cache(maxsize=None)
def move_to_position(start_position, move):
    position = start_position + move
    while position > 10:
        position -= 10
    return position


@lru_cache(maxsize=None)
def play_game(player1, player2, player1_is_playing=True):
    score1, pos1 = player1
    score2, pos2 = player2

    if score1 >= 21:
        return 1, 0

    if score2 >= 21:
        return 0, 1

    nb_wins1, nb_wins2 = 0, 0

    for move1 in [1, 2, 3]:
        for move2 in [1, 2, 3]:
            for move3 in [1, 2, 3]:
                if player1_is_playing:
                    new_pos1 = move_to_position(pos1, move1 + move2 + move3)
                    new_score1 = score1 + new_pos1
                    wins1, wins2 = play_game((new_score1, new_pos1),
                                             (score2, pos2), False)
                else:
                    new_pos2 = move_to_position(pos2, move1 + move2 + move3)
                    new_score2 = score2 + new_pos2
                    wins1, wins2 = play_game((score1, pos1),
                                             (new_score2, new_pos2), True)

                nb_wins1 += wins1
                nb_wins2 += wins2

    return nb_wins1, nb_wins2


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
            _, start_position = line.split(" starting position: ")
            players.append({
                "position": int(start_position),
            })

        wins1, wins2 = play_game(
            (0, players[0]["position"]),
            (0, players[1]["position"]),
            player1_is_playing=True,
        )
        return max(wins1, wins2)


def test_th_ch():
    """
    Run `python -m pytest ./day-21/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
Player 1 starting position: 4
Player 2 starting position: 8
""".strip()) == 444356092776315)
