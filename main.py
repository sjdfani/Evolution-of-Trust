import os
import time
from src import game, constants


class Trust:
    game = None

    def __init__(self) -> None:
        self.game = game.Game()

    def plot_question(self, data: list, multiple: bool):
        response = input("\nDo you want get plot of result? ")
        if response in ("y", "yes"):
            if multiple:
                self.game.plot_multiple_result(data)
            else:
                self.game.plot_one_by_one_result(data)
        self.menu()

    def show_information(self):
        print("PayOffs:")
        print(f"\tCooperate vs Cooperate: {self.game.payoffs.get_cop_cop()}")
        print(f"\tCooperate vs Cheat: {self.game.payoffs.get_cop_cheat()}")
        print(f"\tCheat vs Cooperate: {self.game.payoffs.get_cheat_cop()}")
        print(f"\tCheat vs Cheat: {self.game.payoffs.get_cheat_cheat()}")
        print("Rules:")
        print(f"\tRounds: {self.game.rules.get_rounds()}")
        print(
            f"\tRemove Tail Players: {self.game.rules.get_remove_tail_players()}")
        print(f"\tPopulation Size: {self.game.rules.get_population_size()}")

    def multiple_menu(self):
        os.system("clear")
        print("Count of Individuals:")
        print("1. Manual")
        print("2. Automatic")
        option = int(input("\nEnter an option: "))
        if option == 1:
            return False
        elif option == 2:
            return True
        else:
            print(
                f"Invalid option, please try again after {constants.CONST_SLEEP_TIME} seconds...")
            time.sleep(constants.CONST_SLEEP_TIME)
            self.multiple_menu()

    def menu(self):
        os.system("clear")
        print("***** Welcome to Trust Game *****\n\n")
        print("Information:")
        print("-"*constants.CONST_SPACE)
        self.show_information()
        print("-"*constants.CONST_SPACE)
        print("\nMenu: ")
        print("-"*constants.CONST_SPACE)
        print("PayOffs:")
        print("\t1. Set New Values")
        print("\t2. Reset Default Values")
        print("Rules:")
        print("\t3. Set New Values")
        print("\t4. Reset Default Values")
        print("Tournament:")
        print("\t5. Play 1vs1")
        print("\t6. Play Multiplayer")
        print("Options:")
        print("\t9. Exit")
        print("-"*constants.CONST_SPACE)
        option = input("\nPlease select an option: ")

        if option == "1":
            self.game.set_payOffs()
            self.menu()
        elif option == "2":
            self.game.reset_payOffs()
            self.menu()
        elif option == "3":
            self.game.set_rules()
            self.menu()
        elif option == "4":
            self.game.reset_rules()
            self.menu()
        elif option == "5":
            data = self.game.one_vs_one()
            self.plot_question(data, False)
        elif option == "6":
            automatic = self.multiple_menu()
            data = self.game.multiple(automatic=automatic)
            self.plot_question(data, True)
        elif option == "9":
            exit()
        else:
            print(
                f"Invalid option, please try again after {constants.CONST_SLEEP_TIME} seconds...")
            time.sleep(constants.CONST_SLEEP_TIME)
            self.menu()


def main():
    obj = Trust()
    obj.menu()


if __name__ == "__main__":
    main()
