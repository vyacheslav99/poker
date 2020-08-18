""" Вспомогательные классы, инкапсулирующие атрибуты логических единиц """

import random
from . import const


class GameException(Exception):
    pass


class Card(object):

    def __init__(self, lear: int, value: int, is_joker=False, joker_action=None, joker_lear=None):
        self._lear = lear                   # масть
        self._value = value                 # достоинство, номинал
        self._is_joker = is_joker           # Джокер или нет (value == 7 and lear == const.LEAR_SPADES)
        self.joker_action = joker_action    # Действие джокером. Реально задается в момент хода
        self.joker_lear = joker_lear        # Масть, запрошенная джокером. Реально задается в момент хода

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


class TableItem(object):

    def __init__(self, order, card: Card):
        self.order = order                  # Очередность хода, т.е. порядковый номер, которым была положена карта.
        self.card = card                    # Карта, которой ходили

    def is_joker(self):
        """ Флаг - джокер это или нет. Просто пробрасывает соответствующую опцию из карты """
        return self.card.joker

    def joker_action(self):
        """ Если джокер - то действие джокером. Просто пробрасывает соответствующую опцию из карты """
        return self.card.joker_action

    def joker_lear(self):
        """ Масть, запрошенная джокером. Просто пробрасывает соответствующую опцию из карты """
        return self.card.joker_lear


class Player(object):

    def __init__(self, params=None):
        self.id = None
        self.login = None
        self.password = None
        self.name = None
        self.is_robot = None
        self.risk_level = None
        # self.level = None

        # статистика
        self.total_money = 0            # сумма всех выигрышей
        self.total_games = 0            # +1 в начале игры
        self.completed_games = 0        # +1 при завершении игры (доведения игры до конца)
        self.interrupted_games = 0      # +1 при прерывании игры
        self.winned_games = 0           # +1 при выигрыше (набрал больше всех)
        self.failed_games = 0           # +1 при проигрыше (если ушел в минус)
        self.neutral_games = 0          # +1 если не выиграл и не проиграл (набрал не больше всех, но в плюсе)
        self.last_money = 0             # сумма последнего выигрыша

        # игровые переменные
        self.order = -1                 # заказ в текущем раунде
        self.take = 0                   # взято в текущем раунде
        self.scores = 0                 # очки в текущем раунде
        self.total_scores = 0           # общий счет в текущей игре на текущий момент
        self.cards = []                 # карты на руках
        self.order_cards = []           # карты, на которые сделан заказ (заполняется только у ИИ)
        self.order_is_dark = False      # текущий заказ был сделан в темную или нет
        self.pass_counter = 0           # счетчик пасов, заказанных подряд
        self.success_counter = 0        # счетчик успешно сыгранных подряд игр

        if params:
            self.from_dict(params)

    def from_dict(self, params):
        self.id = params['id']
        self.login = params['login']
        self.password = params['password']
        self.name = params['name']
        self.is_robot = params['is_robot']
        self.risk_level = params['risk_level']
        # self.level = params['level']
        self.total_money = params['total_money']
        self.total_games = params['total']
        self.completed_games = params['completed']
        self.interrupted_games = params['interrupted']
        self.winned_games = params['winned']
        self.failed_games = params['failed']
        self.last_money = params['last_money']

    def as_dict(self):
        return {k: self.__dict__[k] for k in self.__dict__ if not k.startswith(self.__class__.__name__)}

    def lear_exists(self, lear):
        """ Проверяет, есть ли у игрока карты заданной масти. Джокер не учитывается. Вернет True/False """

        for card in self.cards:
            if not card.joker and card.lear == lear:
                return True

        return False

    def gen_lear_range(self, lear, ascending=False):
        """
        Сформировать список карт игрока заданной масти, отсортированный в указанном порядке (по умолчанию убывание).
        Джокер не включается в список
        """

        return sorted([card for card in self.cards if not card.joker and card.lear == lear],
                      key=lambda x: x.value, reverse=not ascending)

    def max_card(self, lear):
        """ Выдать максимальную карту заданной масти. Джокер не учитывается """
        lr = self.gen_lear_range(lear)
        return lr[0] if lr else None

    def min_card(self, lear):
        """ Выдать минимальную карту заданной масти. Джокер не учитывается """
        lr = self.gen_lear_range(lear, ascending=True)
        return lr[0] if lr else None

    def middle_card(self, lear):
        """ Выдает карту из середины заданной масти (со сдвигом к болшей, если поровну не делиться). Джокер не учитывается """

        lr = self.gen_lear_range(lear)

        if lr:
            if len(lr) > 1:
                return lr[round(len(lr) / 2) - 1]
            else:
                return lr[0]
        else:
            return None

    def cards_sorted(self, ascending=False):
        """ Вернет список карт, отсортированный без учета масти в указанном порядке (по умолчанию убывание) """

        # предварительно перемешаем карты, чтобы масти каждый раз были в разном порядке. Это добавит элемент случайности
        mixed = [c for c in self.cards]
        random.shuffle(mixed)
        return sorted(mixed, key=lambda x: x.value, reverse=not ascending)

    def index_of_card(self, lear=None, value=None, joker=False):
        """ Ищет карту у игрока, возвращает ее индекс. Если joker==True - ищет по флагу joker, игнорируя масть и достоинство """

        for i, c in enumerate(self.cards):
            if (c.lear == lear and c.value == value) or (joker and c.joker):
                return i

        return -1

    def card_exists(self, lear=None, value=None, joker=False, exclude_lear=None):
        """
        Смотрит, есть ли у игрока определенная карта.

        :param lear: Масть. Если не указать - будет искать карту указанного достоинства любой масти
        :param value: Достоинство. Можно опустить только если ищем джокера
        :param joker: флаг, что надо искать джокера: если True - ищет джокера, игнорируя масть и достоинство
        :param exclude_lear: исключая указанную масть
        """

        for c in self.cards:
            if (c.value == value and (c.lear == lear or lear is None) and (
                c.lear != exclude_lear or exclude_lear is None)) or (joker and c.joker):
                return True

        return False

    def add_to_order(self, cards):
        """ Добавить карты из списка к заказу """

        for c in cards:
            self.order_cards.append(c)

    def __str__(self):
        if self.is_robot:
            # s = f'Робот <{const.DIFFICULTY_NAMES[self.level]}, {const.RISK_LVL_NAMES[self.risk_level]}>'
            s = f'Робот <{const.RISK_LVL_NAMES[self.risk_level]}>'
        else:
            s = 'Человек'

        return f'{self.name} ({s})'


class Deal(object):

    def __init__(self, player: Player, type_: int, cards: int):
        self.player = player    # первый ходящий в партии (НЕ РАЗДАЮЩИЙ! т.к. смысла его хранить нет - он нужен только для вычисления ходящего)
        self.type_ = type_      # тип раздачи
        self.cards = cards      # количество карт, раздаваемых одному игроку


def flip_coin(probability, maximum=10):
    """
    Делает выбор ДА или НЕТ с заданной вероятностью в пользу ДА.

    :param probability: вероятность (число от 0 до maximum): сколько шансов из максимума должно быть в пользу ДА.
        Если probability == 0 - будет всегда НЕТ, если probability == maximum - всегда ДА
    :param maximum: Максимальное значение вероятности. Чем оно больше, тем точнее можно задать вероятность
    :return: bool - полученный ответ
    """

    if probability < 0 or probability > maximum:
        probability = round(maximum / 2)

    return random.choice([True for _ in range(probability)] + [False for _ in range(maximum-probability)])