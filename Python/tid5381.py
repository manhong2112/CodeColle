# -*- coding: big5 -*-
def ex1(text):
    i = {}
    for j in text:
        if j in i:
            i[j] += 1
        else:
            i[j] = 1
    return sorted(i.items(), key=lambda i: i[1], reverse=True)


print(ex1("History is his story."))


def ex2():
    from random import randint
    from sys import exit

    class Game:
        thrownNumber = 0
        gameRound = 0

        def start_game(self):
            self.gameRound += 1
            print("New Game start, Round", self.gameRound)
            self.thrownNumber = randint(3, 18)

        def end_game(self, *players):
            for i in players:
                player_score = 0
                player_score += i.bet.get("big", 0) * \
                    2 if self.thrownNumber >= 11 else 0
                player_score += i.bet.get("small", 0) * \
                    2 if self.thrownNumber < 11 else 0
                player_score += i.bet.get(str(self.thrownNumber), 0) * 10
                i.score += player_score
                i.bet = {}

    class Player:

        def __init__(self, player_id, score=100):
            self.player_id = player_id
            self.score = score
            self.bet = {}

        def add_bet(self, bet_type, bet_score):
            if self.score - bet_score < 0:
                raise ValueError()
            self.bet[bet_type] = self.bet.get(bet_type, 0) + bet_score
            self.score -= bet_score

    class Computer(Player):

        def __init__(self, player_id, score=100):
            super().__init__(player_id, score)

        def add_bet(self):
            for i in range(randint(1, 5)):
                try:
                    bet_score = randint(1, int(self.score / randint(1, 5)) + 1)
                    if randint(0, 1):
                        super().add_bet("big" if randint(0, 1) else "small", bet_score)
                    else:
                        super().add_bet(str(randint(3, 18)), bet_score)
                    pass
                except ValueError:
                    break

    comp = Computer("Computer")
    player = Player(input("Input Your Name: \n> "))
    game = Game()

    # game main body
    while True:
        game.start_game()
        # print(game.thrownNumber)

        # read input
        print("Input 'quit' to end game, input 'end' or leave blank to end input, input as '<type/number> <bet>' to bet")
        while True:
            tmp = input("> ")
            if tmp == "end" or tmp == "":
                break
            if tmp == "quit":
                exit(0)
            tmp = tmp.split(" ")
            try:
                player.add_bet(tmp[0], int(tmp[1]))
            except ValueError:
                print("Over your existing score")
            except IndexError:
                print("Wrong input, try again")

        comp.add_bet()
        print(comp.player_id, " bet ", comp.bet, sep="")
        print(player.player_id, " bet ", player.bet, sep="")

        game.end_game(player, comp)
        print("Number is", game.thrownNumber)

        print(comp.player_id, "'s score: ", comp.score, sep="")
        print(player.player_id, "'s score: ", player.score, sep="")

        print("=" * 24, sep="")


ex2()
