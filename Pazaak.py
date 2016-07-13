from random import shuffle, choice
from time import sleep
from os import system, name
class Player():
    def __init__(self, hand):
        from random import sample
        self.number = len(players) + 1
        self.cards = []
        self.total = 0
        self.hand = sample(hand, 4)
        self.playing = True
        self.over = False
    def __str__(self):
        return 'Player #' + str(self.number)
    def draw(self, index):
        if self.total <= 20:
            self.over = False
        if self.over == True:
            print(str(self), "has stopped taking turns as they have not gone back below 20.")
            self.playing = False
        else:
            card = deck.pop(index)
            self.cards.append(card)
            self.total += int(card)
    def play(self, value):
        for card in self.hand:
            if card[1:] == value[1:] and (card[0] == '~' or card[0] == value[0]):
                self.hand.remove(card); self.cards.append(value); self.total += int(value)
                return True
        return False
    def table(self):
        return "{} ({} total)".format(' | '.join(self.cards), self.total)
    def showhand(self):
        return 'Empty!' if len(self.hand) == 0 else ' | '.join(self.hand)
    def check(self):
        if self.total == 20:
            self.playing = False
        if len(self.cards) == 9:
            print(str(self), "has stopped taking turns as their play area is full.")
            self.playing = False
            if self.total <= 20:
                return True
        elif self.total > 20:
            self.over = True
        return False
clearCode = 'cls' if name == 'nt' else 'clear'
system(clearCode)
players = []
with open('PazaakDecks.txt') as hands:
    for deck in hands:
        deck = deck.strip('\n').split(',')
        if len(deck) != 10:
            raise Exception("Invalid deck file!")
        for card in deck:
            if not ((card[0] == '+' or card[0] == '~' or card[0] == '-') and card[1:].isdecimal() and int(card[1:]) in range(1, 7)):
                raise Exception("Invalid card: " + card)
        players.append(Player(deck))
deck = ['+' + str(i + 1) for copy in range(4) for i in range(10)]
while True:
    times = input("How many times should the deck be shuffled? ")
    if times.isdecimal() and int(times) >= 0:
        for i in range(int(times)):
            shuffle(deck)
        break
    print("Invalid number.")
for i in range(len(players)):
    shuffle(players)
player = players.pop(0)
system(clearCode)
sleep(0.5); print(str(player), "will be going first followed by:", ', '.join([str(i) for i in players]))
players.append(player)
while True:
    player.draw(0)
    print("Your played cards: " + player.table())
    sleep(0.4)
    if player.check():
        break
    if player.playing:
        sleep(0.4)
        print("Your hand is: " + player.showhand())
        while len(player.hand) > 0:
            value = input("To play a card from your hand enter its value now! ")
            if value != '':
                if len(value) >= 2 and (value[0] == '+' or value[0] == '-'):
                    if player.play(value):
                        print("Card played! "); break
                    else:
                        print("Card not in hand!")
                else:
                    print("Invalid value!")
            else:
                break
        if player.check():
            break
    sleep(0.4)
    if player.playing == True and input('Would you like to stand? (Say "yes" or "stand") ').strip('"').casefold() in ("yes", "stand"):
        player.playing = False
    player = players.pop(0); players.append(player)
    i = 0
    while player.playing == False:
        sleep(1)
        i += 1
        if i == len(players):
            break
        print(str(player) + " will not get a turn because they are out of the game! ")
        player = players.pop(0); players.append(player)
    if i == len(players):
        break
    sleep(1)
    system(clearCode)
    print(str(player) + ', it is now your turn!')
for player in players:
    if player.total <= 20 and len(player.cards) == 9:
        print(str(player), "has won the game by filling their table with a total of less than 20!")
        break
else:#only runs if loop wasn't 'broken' out of
    players.sort(key = lambda x: -x.total if x.total > 20 else x.total)
    for player in players:
        if player.total > 20:
            print(str(player), "is not the winner because their total of", player.total, "is more than 20!")
        else:
            if player.total == players[-1].total:
                if players[-1].total == players[-2].total:
                    print(str(player), "has tied with the highest total of", str(player.total) + "!")
                else:
                    print(str(player), "has won with the highest total of", str(player.total) + "!")
            else:
                print(str(player), "has come close but their total of", player.total, "is lower than the winner's.")
        sleep(3)
