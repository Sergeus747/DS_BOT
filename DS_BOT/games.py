import copy
import random                                               # радномайзер
from random import choice                                   # Выбор из списка


class RollGame():                                           # Класс парной игры в кости
    Is_playing = False                                      # Идет ли игра
    players = ["",""]                                       # Имена игроков
    points = [0,0]                                          # Очки игроков
    Whose_throw = 0                                         # Кто бросает


    def reset(self):                                        # Сброс игры в начальное состояние
        self.Is_playing = False
        self.points = [0,0]
        self.Whose_throw = 0
        return 'Парные кости сброшены'


class BlackJackGame():                                      # Класс игры в BLACKJACK

    Cards_p= {
        '2_Clubs': 2,       '2_Worms': 2,       '2_Peaks': 2,       '2_Diamonds': 2,
        '3_Clubs': 3,       '3_Worms': 3,       '3_Peaks': 3,       '3_Diamonds': 3,
        '4_Clubs': 4,       '4_Worms': 4,       '4_Peaks': 4,       '4_Diamonds': 4,
        '5_Clubs': 5,       '5_Worms': 5,       '5_Peaks': 5,       '5_Diamonds': 5,
        '6_Clubs': 6,       '6_Worms': 6,       '6_Peaks': 6,       '6_Diamonds': 6,
        '7_Clubs': 7,       '7_Worms': 7,       '7_Peaks': 7,       '7_Diamonds': 7,
        '8_Clubs': 8,       '8_Worms': 8,       '8_Peaks': 8,       '8_Diamonds': 8,
        '9_Clubs': 9,       '9_Worms': 9,       '9_Peaks': 9,       '9_Diamonds': 9,
        '10_Clubs': 10,     '10_Worms': 10,     '10_Peaks': 10,     '10_Diamonds': 10,
        'Jack_Clubs': 10,   'Jack_Worms': 10,   'Jack_Peaks': 10,   'Jack_Diamonds': 10,
        'Lady_Clubs': 10,   'Lady_Worms': 10,   'Lady_Peaks': 10,   'Lady_Diamonds': 10,
        'King_Clubs': 10,   'King_Worms': 10,   'King_Peaks': 10,   'King_Diamonds': 10,
        'ACE_Clubs': 11,    'ACE_Worms': 11,    'ACE_Peaks': 11,    'ACE_Diamonds': 11
    }

    Cards= {
        '2_Clubs': 'Cards/2_Clubs.png',         '2_Worms': 'Cards/2_Worms.png',         '2_Peaks': 'Cards/2_Peaks.png',         '2_Diamonds': 'Cards/2_Diamonds.png',
        '3_Clubs': 'Cards/3_Clubs.png',         '3_Worms': 'Cards/3_Worms.png',         '3_Peaks': 'Cards/3_Peaks.png',         '3_Diamonds': 'Cards/3_Diamonds.png',
        '4_Clubs': 'Cards/4_Clubs.png',         '4_Worms': 'Cards/4_Worms.png',         '4_Peaks': 'Cards/4_Peaks.png',         '4_Diamonds': 'Cards/4_Diamonds.png',
        '5_Clubs': 'Cards/5_Clubs.png',         '5_Worms': 'Cards/5_Worms.png',         '5_Peaks': 'Cards/5_Peaks.png',         '5_Diamonds': 'Cards/5_Diamonds.png',
        '6_Clubs': 'Cards/6_Clubs.png',         '6_Worms': 'Cards/6_Worms.png',         '6_Peaks': 'Cards/6_Peaks.png',         '6_Diamonds': 'Cards/6_Diamonds.png',
        '7_Clubs': 'Cards/7_Clubs.png',         '7_Worms': 'Cards/7_Worms.png',         '7_Peaks': 'Cards/7_Peaks.png',         '7_Diamonds': 'Cards/7_Diamonds.png',
        '8_Clubs': 'Cards/8_Clubs.png',         '8_Worms': 'Cards/8_Worms.png',         '8_Peaks': 'Cards/8_Peaks.png',         '8_Diamonds': 'Cards/8_Diamonds.png',
        '9_Clubs': 'Cards/9_Clubs.png',         '9_Worms': 'Cards/9_Worms.png',         '9_Peaks': 'Cards/9_Peaks.png',         '9_Diamonds': 'Cards/9_Diamonds.png',
        '10_Clubs': 'Cards/10_Clubs.png',       '10_Worms': 'Cards/10_Worms.png',       '10_Peaks': 'Cards/10_Peaks.png',       '10_Diamonds': 'Cards/10_Diamonds.png',
        'Jack_Clubs': 'Cards/Jack_Clubs.png',   'Jack_Worms': 'Cards/Jack_Worms.png',   'Jack_Peaks': 'Cards/Jack_Peaks.png',   'Jack_Diamonds': 'Cards/Jack_Diamonds.png',
        'Lady_Clubs': 'Cards/Lady_Clubs.png',   'Lady_Worms': 'Cards/Lady_Worms.png',   'Lady_Peaks': 'Cards/Lady_Peaks.png',   'Lady_Diamonds': 'Cards/Lady_Diamonds.png',
        'King_Clubs': 'Cards/King_Clubs.png',   'King_Worms': 'Cards/King_Worms.png',   'King_Peaks': 'Cards/King_Peaks.png',   'King_Diamonds': 'Cards/King_Diamonds.png',
        'ACE_Clubs': 'Cards/ACE_Clubs.png',     'ACE_Worms': 'Cards/ACE_Worms.png',     'ACE_Peaks': 'Cards/ACE_Peaks.png',     'ACE_Diamonds': 'Cards/ACE_Diamonds.png',
        'Shirt': 'Cards/Shirt.png'
    }

    Is_playing = False                                      # Идет ли игра
    player = [""]                                           # Кто играет
    bot_keys = []
    player_keys = []   
    bot_points = 0
    player_points = [0]                                     # Очки игроков
    bet = 0                                                 # Ставка


    def reset(self):                                        # Сброс игры в начальное состояние
        self.Is_playing = False
        self.player = [""]  
        self.bot_keys = []
        self.player_keys = []
        self.bot_points = 0 
        self.player_points = [0]
        self.bet = 0 
        return "BLACKJACK сброшен"


    def hand_starter_deck(self, name, count):               # Раздача страктовой колоды
        self.player = name
        self.Is_playing = True
        self.bet = int(count)
        decks = []                                          # Массив колод

        for i in range(6):                                  # Заполнение колод
            decks.append(self.get_deck())

        for i in range(2):                                  # Бот набирает стартовые карты
            deck = random.randint(0, 5)                     # Выбор колоды

            card = choice(list(decks[deck].keys()))
            del decks[deck][card]
            
            self.bot_take_card(card)                        # Бот берет карту
        # print (self.bot_keys)

        
        for i in range(2):                                  # Игрок набирает стартовые карты
            deck = random.randint(0, 5)                     # Выбор колоды

            card = choice(list(decks[deck].keys()))
            del decks[deck][card]

            self.player_take_card(card)                     # Игрок берет карту
        # print (self.player_keys)


    def get_deck(self):
        return copy.copy(self.Cards_p)


    def check_bot_blackjack(self):
        if self.bot_points == 21:
            return True
        else:
            return False


    def check_player_blackjack(self, number):
        if self.player_points[number] == 21:
            return True
        else:
            return False


    def bot_take_card(self, card):                          # бот берет карту
        self.bot_keys.append(card)
        if self.Cards_p[card] == 11 and self.bot_points > 10:
            self.bot_points += 1
        else:
            self.bot_points += self.Cards_p[card]
        return "бот взял карту"


    def player_take_card(self, card):                       # игрок берет карту
        self.player_keys.append(card)
        if self.Cards_p[card] == 11 and self.player_points[0] > 10:
            self.player_points[0] += 1
        else:
            self.player_points[0] += self.Cards_p[card]
        return "игрок взял карту"


    def bot_show_card(self, number):
        return copy.copy(self.Cards[self.bot_keys[number]])
    

    def player_show_card(self, number):
        return copy.copy(self.Cards[self.player_keys[number]])


    def show_player_points(self, number):
        return copy.copy(self.player_points[number])


    def show_bot_points(self):
        return copy.copy(self.bot_points)


    def show_shirt(self):
        return copy.copy(self.Cards['Shirt'])
    