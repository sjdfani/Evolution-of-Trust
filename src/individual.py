import random


class PlayType:
    COOPERATE = 1
    CHEAT = 0

    def get_opposite_of(value):
        if value == PlayType.COOPERATE:
            return PlayType.CHEAT
        elif value == PlayType.CHEAT:
            return PlayType.COOPERATE


class Character:
    __score = 20

    def change_score(self, value: int):
        self.__score += value

    def get_score(self):
        return self.__score


class Cooperator(Character):
    """
    Always Cooperate.
    """

    def __str__(self) -> str:
        return "Cooperator"

    def play(self):
        return PlayType.COOPERATE


class Copycat(Character):
    """
    Starts with Cooperate.
    Afterwards, it just copy whatever you did in the last.
    """
    opponent_last_move = None

    def __str__(self) -> str:
        return "Copycat"

    def set_last_round_move(self, opponent_move: PlayType):
        self.opponent_last_move = opponent_move

    def play(self):
        if self.opponent_last_move is None:
            return PlayType.COOPERATE
        else:
            return self.opponent_last_move


class Cheater(Character):
    """
    Always cheat.
    """

    def __str__(self) -> str:
        return "Cheater"

    def play(self):
        return PlayType.CHEAT


class Grudger(Character):
    """
    Starts with Cooperate, and keeps cooperating until you cheat it even once.
    Afterwards, it always plays Cheat.
    """
    is_cheat = False
    is_first_time = True

    def __str__(self) -> str:
        return "Grudger"

    def update_is_cheat(self, opponent_move: PlayType):
        if opponent_move == PlayType.CHEAT:
            self.is_cheat = True

    def play(self):
        if self.is_first_time:
            self.is_first_time = False
            return PlayType.COOPERATE
        else:
            if self.is_cheat:
                return PlayType.CHEAT
            else:
                return PlayType.COOPERATE


class Detective(Character):
    """
    Starts with: Cooperate, Cheat, Cooperate, Cooperate.
    Afterwards, if you ever retaliate with a Cheat, it plays like a Copycat.
    Otherwise, it plays like an Always Cheat.
    """
    opponent_last_move = None
    index = 0
    is_cheat = False
    move_list = (
        PlayType.COOPERATE, PlayType.CHEAT,
        PlayType.COOPERATE, PlayType.COOPERATE,
    )

    def __str__(self) -> str:
        return "Detective"

    def increment_index(self):
        self.index += 1

    def update_is_cheat(self, opponent_move: PlayType):
        if opponent_move == PlayType.CHEAT:
            self.is_cheat = True

    def set_last_round_move(self, opponent_move: PlayType):
        self.opponent_last_move = opponent_move
        self.update_is_cheat(opponent_move)

    def play(self):
        if len(self.move_list) - self.index > 0:
            move = self.move_list[self.index]
            self.increment_index()
            return move
        else:
            if self.is_cheat:
                return self.opponent_last_move
            else:
                return PlayType.CHEAT


class CopyKitten(Character):
    """
    Starts with Cooperate.
    Only retaliates with a Cheat if you cheated it TWICE in a row.
    """
    cheat_count = 0

    def __str__(self) -> str:
        return "CopyKitten"

    def update_cheat_count(self, opponent_move: PlayType):
        if opponent_move == PlayType.CHEAT:
            self.cheat_count += 1

    def play(self):
        if self.cheat_count == 0 or self.cheat_count == 1:
            return PlayType.COOPERATE
        elif self.cheat_count == 2:
            self.cheat_count = 0
            return PlayType.CHEAT


class Simpleton(Character):
    """
    Starts with Cooperate.
    Then, if you cooperated in last round, it repeats its last move.
    But if you cheated in last round, it switches its last move.
    """
    opponent_last_move = None

    def __str__(self) -> str:
        return "Simpleton"

    def set_last_round_move(self, opponent_move: PlayType):
        self.opponent_last_move = opponent_move

    def play(self):
        if self.opponent_last_move is None:
            return PlayType.COOPERATE
        elif self.opponent_last_move == PlayType.COOPERATE:
            return self.opponent_last_move
        elif self.opponent_last_move == PlayType.CHEAT:
            return PlayType.get_opposite_of(self.opponent_last_move)


class Random(Character):
    """
    Randomly cheats or cooperates with 50-50 chance.
    """

    def __str__(self) -> str:
        return "Random"

    def play(self):
        number = random.randint(0, 1)
        return PlayType.COOPERATE if number == 1 else PlayType.CHEAT
