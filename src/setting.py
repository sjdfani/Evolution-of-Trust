from . import constants
from .individual import PlayType


class PayOffs:
    __cooperate_cooperate = None
    __cooperate_cheat = None
    __cheat_cooperate = None
    __cheat_cheat = None

    def __init__(self) -> None:
        self.set_default_value()

    def set_default_value(self):
        self.__cooperate_cooperate = (
            constants.CONST_DEFAULT_COOPERATE_COOPERATE,
            constants.CONST_DEFAULT_COOPERATE_COOPERATE
        )
        self.__cooperate_cheat = (
            constants.CONST_DEFAULT_COOPERATE_CHEAT,
            constants.CONST_DEFAULT_CHEAT_COOPERATE
        )
        self.__cheat_cooperate = (
            constants.CONST_DEFAULT_CHEAT_COOPERATE,
            constants.CONST_DEFAULT_COOPERATE_CHEAT
        )
        self.__cheat_cheat = (
            constants.CONST_DEFAULT_CHEAT_CHEAT,
            constants.CONST_DEFAULT_CHEAT_CHEAT
        )

    def set_payoffs(self, cop_cop_value: float, cop_cheat_value: float, cheat_cop_value: float, cheat_cheat_value: float):
        self.__cooperate_cooperate = (cop_cop_value, cop_cop_value)
        self.__cooperate_cheat = (cop_cheat_value, cheat_cop_value)
        self.__cheat_cooperate = (cheat_cop_value, cop_cheat_value)
        self.__cheat_cheat = (cheat_cheat_value, cheat_cheat_value)

    def check_and_get_score(self, player1: int, player2: int):
        if player1 == PlayType.COOPERATE and player2 == PlayType.COOPERATE:
            return self.__cooperate_cooperate
        elif player1 == PlayType.COOPERATE and player2 == PlayType.CHEAT:
            return self.__cooperate_cheat
        elif player1 == PlayType.CHEAT and player2 == PlayType.COOPERATE:
            return self.__cheat_cooperate
        elif player1 == PlayType.CHEAT and player2 == PlayType.CHEAT:
            return self.__cheat_cheat

    def get_str_types(self, player1: int, score_player_1: int, player2: int, score_player_2: int):
        if player1 == PlayType.COOPERATE and player2 == PlayType.COOPERATE:
            return f"Cooperate ({score_player_1}) & Cooperate ({score_player_2})"
        elif player1 == PlayType.COOPERATE and player2 == PlayType.CHEAT:
            return f"Cooperate ({score_player_1}) & Cheat ({score_player_2})"
        elif player1 == PlayType.CHEAT and player2 == PlayType.COOPERATE:
            return f"Cheat ({score_player_1}) & Cooperate ({score_player_2})"
        elif player1 == PlayType.CHEAT and player2 == PlayType.CHEAT:
            return f"Cheat ({score_player_1}) & Cheat ({score_player_2})"

    def get_cop_cop(self):
        return self.__cooperate_cooperate

    def get_cop_cheat(self):
        return self.__cooperate_cheat

    def get_cheat_cop(self):
        return self.__cheat_cooperate

    def get_cheat_cheat(self):
        return self.__cheat_cheat


class Rule:
    __rounds = None
    __remove_tail_players = None
    __population_size = None

    def __init__(self) -> None:
        self.set_default_value()

    def set_default_value(self):
        self.__rounds = constants.CONST_DEFAULT_ROUNDS
        self.__remove_tail_players = constants.CONST_DEFAULT_COUNT_REPLACE_WEAKEST
        self.__population_size = constants.CONST_DEFAULT_POPULATION

    def set_rule(self, rounds: float, remove_tail_players: float, population_size: float):
        self.__rounds = rounds
        self.__remove_tail_players = remove_tail_players
        self.__population_size = population_size

    def get_rounds(self):
        return self.__rounds

    def get_remove_tail_players(self):
        return self.__remove_tail_players

    def get_population_size(self):
        return self.__population_size
