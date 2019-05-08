""" Вспомогательные классы, инкапсулирующие атрибуты логических единиц """

from game import const


class GameException(Exception):
    pass


class Deal(object):

    def __init__(self, player:Player, type_:int, cards:int):
        self.player = player    # первый ходящий в партии (НЕ РАЗДАЮЩИЙ! т.к. смысла его хранить нет - он нужен только для вычисления ходящего)
        self.type_ = type_      # тип раздачи
        self.cards = cards      # количество карт, раздаваемых одному игроку

class Card(object):

    def __init__(self, lear:int, value:int, is_joker=False):
        self._lear = lear           # масть
        self._value = value         # достоинство, номинал
        self._is_joker = is_joker   # Джокер или нет (value == 7 and lear == const.LEAR_SPADES)

    @property
    def value(self):
        return self._value

    @property
    def lear(self):
        return self._lear

    @property
    def joker(self):
        return self._is_joker

    def __str__(self):
        if self.joker:
            return f'Joker ({const.CARD_NAMES[self._value]} {const.LEAR_SYMBOLS[self._lear]})'
        else:
            return f'{const.CARD_NAMES[self._value]} {const.LEAR_SYMBOLS[self._lear]}'


class Player(object):

    id = None
    login = None
    password = None
    name = None
    is_robot = None
    risk_level = None
    level = None
    money = 0

    # статистика
    total_money = 0         # сумма всех выигрышей
    total_games = 0         # +1 в начале игры
    completed_games = 0     # +1 при завершении игры (доведения игры до конца)
    interrupted_games = 0   # +1 при прерывании игры
    winned_games = 0        # +1 при выигрыше (набрал больше всех)
    failed_games = 0        # +1 при проигрыше (если ушел в минус)
    neutral_games = 0       # +1 при если не выиграл и не проиграл (набрал не больше всех, но в плюсе)

    # игровые переменные
    order = -1              # заказ в текущей партии
    take = 0                # взято в текущей партии
    scores = 0              # очки в текущей партии
    total_scores = 0        # общий счет в текущей игре на текущий момент
    cards = []              # карты на руках
    order_cards = []        # карты, на которые сделан заказ (заполняется только у ИИ)
    pass_counter = 0        # счетчик пасов, заказанных подряд

    def __init__(self, params=None):
        if params:
            self.from_dict(params)

    def from_dict(self, params):
        self.id = params['id']
        self.login = params['login']
        self.password = params['password']
        self.name = params['name']
        self.is_robot = params['is_robot']
        self.risk_level = params['risk_level']
        self.level = params['level']
        self.total_money = params['total_money']
        self.total_games = params['total']
        self.completed_games = params['completed']
        self.interrupted_games = params['interrupted']
        self.winned_games = params['winned']
        self.failed_games = params['failed']

    def as_dict(self):
        return {k: self.__dict__[k] for k in self.__dict__ if not k.startswith(self.__class__)}