import os
import time
from . import individual, setting, constants
import pandas as pd
import matplotlib.pyplot as plt


class Game:
    payoffs = None
    rules = None
    characters = None
    print_log = None

    def __init__(self) -> None:
        self.payoffs = setting.PayOffs()
        self.rules = setting.Rule()
        self.print_log = constants.PRINT_LOG
        self.characters = (
            individual.Cooperator(),
            individual.Copycat(),
            individual.Cheater(),
            individual.Grudger(),
            individual.Detective(),
        )
        if constants.IS_RANDOM_NESS:
            self.characters += (
                individual.CopyKitten(), individual.Simpleton(), individual.Random()
            )

    def set_payOffs(self):
        # cop_cop_value = int(input("Enter cooperate vs cooperate value: "))
        # cop_cheat_value = int(input("Enter cooperate vs cheat value: "))
        # cheat_cop_value = int(input("Enter cheat vs cooperate value: "))
        # cheat_cheat_value = int(input("Enter cheat vs cheat value: "))
        # self.payoffs.set_payoffs(
        #     cop_cop_value, cop_cheat_value, cheat_cop_value, cheat_cheat_value)

        values = [
            float(input(f"Enter {pair[0]} vs {pair[1]} value: "))
            for pair in [
                ("cooperate", "cooperate"),
                ("cooperate", "cheat"),
                ("cheat", "cooperate"),
                ("cheat", "cheat"),
            ]
        ]
        self.payoffs.set_payoffs(*values)

    def reset_payOffs(self):
        self.payoffs.set_default_value()

    def set_rules(self):
        # rounds = int(input("Enter rounds: "))
        # remove_tail_players = int(
        #     input("Enter count of remove tail players: "))
        # population_size = int(input("Enter population size: "))
        # self.rules.set_rule(rounds, remove_tail_players, population_size)

        self.rules.set_rule(
            int(input("Enter rounds: ")),
            int(input("Enter count of remove tail players: ")),
            int(input("Enter population size: "))
        )

    def reset_rules(self):
        self.rules.set_default_value()

    def select_character(self, count: int):
        population = list()
        for _ in range(count):
            print(f"Selection {_+1}:\n")
            for i, individual in enumerate(self.characters):
                print(f"{i+1}. {individual}")
            option = int(input("Enter a character: "))

            while option not in range(1, len(self.characters)+1):
                print("Error, Please select the correct option...")
                option = int(input("Enter a character: "))

            population.append(self.characters[option-1])
            print("\n")

        return population

    def play_two_character(self, player_1, player_2):
        response_player_1 = player_1.play()
        response_player_2 = player_2.play()

        # Player 1
        if (
            isinstance(player_1, individual.Copycat) or
            isinstance(player_1, individual.Simpleton)
        ):
            player_1.set_last_round_move(response_player_2)
        elif (
            isinstance(player_1, individual.Grudger)
        ):
            player_1.update_is_cheat(response_player_2)
        elif (
            isinstance(player_1, individual.Detective)
        ):
            player_1.set_last_round_move(response_player_2)
            player_1.update_is_cheat(response_player_2)
        elif (
            isinstance(player_1, individual.CopyKitten)
        ):
            player_1.update_cheat_count(response_player_2)

        # Player 2
        if (
            isinstance(player_2, individual.Copycat) or
            isinstance(player_2, individual.Simpleton)
        ):
            player_2.set_last_round_move(response_player_1)
        elif (
            isinstance(player_2, individual.Grudger)
        ):
            player_2.update_is_cheat(response_player_1)
        elif (
            isinstance(player_2, individual.Detective)
        ):
            player_2.set_last_round_move(response_player_1)
            player_2.update_is_cheat(response_player_1)
        elif (
            isinstance(player_2, individual.CopyKitten)
        ):
            player_2.update_cheat_count(response_player_1)

        result_player_1, result_player_2 = self.payoffs.check_and_get_score(
            response_player_1, response_player_2)
        player_1.change_score(result_player_1)
        player_2.change_score(result_player_2)

        if self.print_log:
            print(self.payoffs.get_str_types(
                response_player_1, player_1.get_score(),
                response_player_2, player_2.get_score()
            ))

    def one_vs_one(self):
        os.system("clear")
        population = self.select_character(2)
        os.system("clear")

        print(f"{population[0]} vs {population[1]}\n")

        data = [
            {
                population[0].__str__(): population[0].get_score(),
                population[1].__str__(): population[1].get_score(),
            },
        ]
        for i in range(self.rules.get_rounds()):
            print(f"Round {i+1}")
            self.play_two_character(population[0], population[1])
            data.append(
                {
                    population[0].__str__(): population[0].get_score(),
                    population[1].__str__(): population[1].get_score(),
                }
            )
        data = {
            "names": [population[0].__str__(), population[1].__str__()],
            "data": data
        }
        return data

    def get_manual_population(self):
        os.system("clear")
        available_size = self.rules.get_population_size()

        object_population = {char: 0 for char in self.characters}

        for i in range(len(self.characters)):
            print(f"Available Population Size: {available_size}")
            count = int(input(f"Enter {self.characters[i]} size: "))
            if available_size - count < 0 or (count < 0 and available_size != 0):
                print(
                    f"You entered more than valid size, Please try again after {constants.CONST_SLEEP_TIME} seconds...")
                time.sleep(constants.CONST_SLEEP_TIME)
                self.get_manual_population()
            else:
                available_size -= count
                object_population[self.characters[i]] = count

        if available_size != 0:
            print(
                f"You should spend all available size, Please try again after {constants.CONST_SLEEP_TIME} seconds...")
            time.sleep(constants.CONST_SLEEP_TIME)
            self.get_manual_population()

        data = []
        for key, value in object_population.items():
            data.extend([key for _ in range(value)])

        return data

    def get_automatic_population(self):
        os.system("clear")
        population_size = self.rules.get_population_size()

        population_per_object = population_size // len(self.characters)
        remaining_population = population_size % len(self.characters)

        object_population = {}
        for i in range(len(self.characters)):
            if i < remaining_population:
                object_population[
                    self.characters[i]] = population_per_object + 1
            else:
                object_population[self.characters[i]] = population_per_object

        data = []
        for key, value in object_population.items():
            data.extend([key for _ in range(value)])

        print("Result:\n")
        for key, value in object_population.items():
            print(f"{key} : {value}")

        print("\n")
        while True:
            response = input("Continue... ? ").lower()
            if response in ("y", "yes"):
                break

        return data

    def replace_weakest(self, data: list):
        data.sort(key=lambda x: x.get_score())
        data = data[self.rules.get_remove_tail_players():]

        for item in data[-self.rules.get_remove_tail_players():]:
            if isinstance(item, individual.Cooperator):
                obj = individual.Cooperator()
                obj.score = item.get_score()
            elif isinstance(item, individual.Copycat):
                obj = individual.Copycat()
                obj.score = item.get_score()
            elif isinstance(item, individual.Cheater):
                obj = individual.Cheater()
                obj.score = item.get_score()
            elif isinstance(item, individual.Grudger):
                obj = individual.Grudger()
                obj.score = item.get_score()
            elif isinstance(item, individual.Detective):
                obj = individual.Detective()
                obj.score = item.get_score()
            elif isinstance(item, individual.CopyKitten):
                obj = individual.CopyKitten()
                obj.score = item.get_score()
            elif isinstance(item, individual.Simpleton):
                obj = individual.Simpleton()
                obj.score = item.get_score()
            elif isinstance(item, individual.Random):
                obj = individual.Random()
                obj.score = item.get_score()
            data.append(obj)

        return data

    def multiple(self, automatic: bool):
        population, data_score, data_count = [], [], []
        temp_score, temp_count = {}, {}

        os.system("clear")
        if not automatic:
            population = self.get_manual_population()
        else:
            population = self.get_automatic_population()
        os.system("clear")

        for i in range(len(population)):
            if (population[i].__str__(), 0) not in temp_score.keys():
                temp_score[
                    (population[i].__str__(), 0)
                ] = population[i].get_score()
            else:
                temp_score[
                    (population[i].__str__(), 0)
                ] += population[i].get_score()

            if (population[i].__str__(), 0) not in temp_count.keys():
                temp_count[(population[i].__str__(), 0)] = 1
            else:
                temp_count[(population[i].__str__(), 0)] += 1

        data_score.append(temp_score)
        data_count.append(temp_count)

        temp_count, temp_score = {}, {}
        for r in range(self.rules.get_rounds()):
            if self.print_log:
                print(f"*** Round {r+1} ***")
            for i in range(len(population)):
                for j in range(len(population)):
                    if i != j:
                        if self.print_log:
                            print(f"\n{population[i]} vs {population[j]}")
                        self.play_two_character(population[i], population[j])

            if self.print_log:
                print("\n\n\n")
            for m in range(len(population)):
                if (population[m].__str__(), r+1) not in temp_score.keys():
                    temp_score[
                        (population[m].__str__(), r+1)] = population[m].get_score()
                else:
                    temp_score[
                        (population[m].__str__(), r+1)] += population[m].get_score()

                if (population[m].__str__(), r+1) not in temp_count.keys():
                    temp_count[(population[m].__str__(), r+1)] = 1
                else:
                    temp_count[(population[m].__str__(), r+1)] += 1

            data_score.append(temp_score)
            data_count.append(temp_count)
            temp_score, temp_count = {}, {}

            population = self.replace_weakest(population)

        print("Count of population in different rounds:")
        for item in data_count:
            print(item)

        print("\nScore of population in different rounds:")
        for item in data_score:
            print(item)

        return {
            "score": data_score,
            "count": data_count,
        }

    def plot_one_by_one_result(self, data: dict):
        df = pd.DataFrame(data["data"])
        plt.plot(df)
        plt.legend(data["names"])
        plt.grid()
        plt.show()

    def plot_multiple_count(self, data_count: list):
        formatted_data = {}
        for item in data_count:
            for key, value in item.items():
                obj_name, round_num = key
                if round_num not in formatted_data:
                    formatted_data[round_num] = {}
                if obj_name in formatted_data[round_num]:
                    formatted_data[round_num][obj_name] += value
                else:
                    formatted_data[round_num][obj_name] = value

        df = pd.DataFrame.from_dict(formatted_data, orient='index')
        df.sort_index(inplace=True)
        df.fillna(0, inplace=True)

        plt.figure(figsize=(10, 6))
        plt.title("Count Plot")
        plt.plot(df)
        plt.legend(
            df.columns.tolist(),
            loc='lower left',
            fontsize='small',
        )
        plt.xticks(range(self.rules.get_rounds()+1))
        plt.grid()
        plt.show()

    def plot_multiple_score(self, data_score: list):
        formatted_data = {}
        for item in data_score:
            for key, value in item.items():
                obj_name, round_num = key
                if round_num not in formatted_data:
                    formatted_data[round_num] = {}
                formatted_data[round_num][obj_name] = value

        df = pd.DataFrame.from_dict(formatted_data, orient='index')
        df.sort_index(inplace=True)
        df.fillna(0, inplace=True)

        plt.figure(figsize=(10, 6))
        plt.title("Score Plot")
        plt.plot(df)
        plt.legend(
            df.columns.tolist(),
            loc='upper left',
            fontsize='small',
        )
        plt.xticks(range(df.index.min(), df.index.max() + 1))
        # plt.yticks(range(int(df.min().min()), int(df.max().max()), 500))
        plt.yticks(range(int(df.min().min()), int(df.max().max()), 500))
        plt.grid()
        plt.show()

    def plot_multiple_result(self, data: dict):
        self.plot_multiple_count(data["count"])
        self.plot_multiple_score(data["score"])
