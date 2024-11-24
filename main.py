import random


class Player:
    """Base Player class for all types of players."""
    moves = ['rock', 'paper', 'scissors']

    def move(self):
        """Default move for Player: always 'rock'."""
        return 'rock'

    def learn(self, my_move, their_move):
        """Empty learn method for non-learning players."""
        pass


class RandomPlayer(Player):
    """Player that randomly selects a move each round."""
    def move(self):
        return random.choice(self.moves)


class ReflectPlayer(Player):
    """Player that mimics the opponent's previous move."""
    def __init__(self):
        super().__init__()
        self.their_move = None

    def move(self):
        return self.their_move if self.their_move else random.choice(
            self.moves)

    def learn(self, my_move, their_move):
        self.their_move = their_move


class CyclePlayer(Player):
    """Player that cycles through moves in a fixed order."""
    def __init__(self):
        super().__init__()
        self.my_move = None

    def move(self):
        if self.my_move is None:
            self.my_move = 'rock'
        else:
            current_index = self.moves.index(self.my_move)
            self.my_move = self.moves[(current_index + 1) % len(self.moves)]
        return self.my_move

    def learn(self, my_move, their_move):
        self.my_move = my_move


class HumanPlayer(Player):
    """Player controlled by human input."""
    def move(self):
        while True:
            move = input("Choose 'rock', 'paper', or 'scissors': ").lower()
            if move in self.moves:
                return move
            elif move == 'exit':
                exit("Game exited by user.")
            else:
                print("Invalid move. Enter 'rock', 'paper', or 'scissors'.")


class RockPlayer(Player):
    """Player that always plays 'rock'."""
    def move(self):
        return 'rock'


class Game:
    """Main game class to manage rounds and scores."""
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.score_p1 = 0
        self.score_p2 = 0

    def beats(self, one, two):
        return ((one == 'rock' and two == 'scissors') or
                (one == 'scissors' and two == 'paper') or
                (one == 'paper' and two == 'rock'))

    def get_number_of_rounds(self):
        while True:
            rounds = input("How many rounds would you like to play? : ")
            if rounds.isdigit():
                return int(rounds)
            elif rounds.lower() == 'exit':
                exit("Game exited by user.")
            else:
                print("Invalid input. Please enter a number.")

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"\nPlayer One plays: {move1}")
        print(f"Player Two plays: {move2}")

        if self.beats(move1, move2):
            self.score_p1 += 1
            print("** Player One wins this round! **")
        elif self.beats(move2, move1):
            self.score_p2 += 1
            print("** Player Two wins this round! **")
        else:
            print("** This round is a tie! **")

        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

        print(f"Score after this round: Player One - {self.score_p1}, "
              f"Player Two - {self.score_p2}")

    def play_game(self):
        print(">>>> Game start! <<<<\n(Type 'exit' at any prompt to quit.)")
        rounds = self.get_number_of_rounds()

        for round_num in range(1, rounds + 1):
            print(f"\nRound {round_num} of {rounds}")
            self.play_round()

        print("\n>>>> Game Over! <<<<")
        print(f"Final Score: Player One - {self.score_p1}, "
              f"Player Two - {self.score_p2}")

        if self.score_p1 > self.score_p2:
            print("**** Player One is the overall winner! ****")
        elif self.score_p2 > self.score_p1:
            print("**** Player Two is the overall winner! ****")
        else:
            print("**** The game ended in a tie! ****")


if __name__ == '__main__':
    opponents = [RandomPlayer(), ReflectPlayer(), CyclePlayer(), RockPlayer()]
    game = Game(HumanPlayer(), random.choice(opponents))
    game.play_game()
