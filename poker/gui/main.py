import random

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QFrame, QMessageBox, QLabel, QAction
from PyQt5.QtGui import QIcon

from gui import utils, const
from game import engine, helpers, const as eng_const


class MainWnd(QMainWindow):

    def __init__(self, app):
        super().__init__()

        self.options = {}
        self.players = []
        self.bet = None
        self.game = None

        self.app = app
        self.setWindowIcon(QIcon(const.MAIN_ICON))
        self.setWindowTitle(const.MAIN_WINDOW_TITLE)
        self.init_menu_actions()

        sb_scales = (1, 2, 0)
        self.status_labels = []
        for i in range(3):
            self.status_labels.append(QLabel())
            self.statusBar().addWidget(self.status_labels[i], sb_scales[i])

        self.area = QFrame(self)
        self.area.setFocusPolicy(Qt.StrongFocus)
        self.setCentralWidget(self.area)

        self.resize(1400, 960)
        self.center()
        self.show()

    def init_menu_actions(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        # toolbar = self.addToolBar('Выход')
        start_actn = QAction('Играть', self)
        # start_actn.setShortcut('Esc')
        start_actn.setStatusTip('Начать новую игру')
        start_actn.triggered.connect(self.start_game)
        file_menu.addAction(start_actn)

        # exit_actn = QAction(QIcon('exit24.png'), 'Exit', self)
        exit_actn = QAction('Выход', self)
        exit_actn.setShortcut('Esc')
        exit_actn.setStatusTip('Выход из игры')
        exit_actn.triggered.connect(self.close)
        file_menu.addAction(exit_actn)
        # toolbar.addAction(exit_actn)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, 10)  # (screen.height() - size.height()) / 3)

    def closeEvent(self, event):
        print('< Exit >')
        super(MainWnd, self).closeEvent(event)

    def show_help(self):
        QMessageBox.information(self.parent(), 'Подсказка',
                                '\n'.join(('Клавиши управления игрой\n',) + const.HELP_KEYS), QMessageBox.Ok)

    def set_status_messages(self, messages):
        """
        Записать сообщение в статусбар

        :param messages: list, tuple: массив сообщений. Сообщения распределяются по индексам:
            0 - в первую панель статусбара (слева - направо), 1 - во вторую и т.д.
            Длина списка сообщений не должна превышать кол-во панелей статусбара. Все, что больше, будет игнорироваться
        """

        for i in range(len(messages)):
            if i < len(self.status_labels):
                self.status_labels[i].setText(messages[i])

    def set_status_message(self, message, index=0):
        """
        Записать сообщение в статусбар

        :param message: str: Строка сообщения.
        :param index: int: Индекс панели статусбара, где надо вывести сообщение
        """

        if 0 < index < len(self.status_labels):
            self.status_labels[index].setText(message)

    def clear_status_messages(self):
        self.set_status_messages(('', '', ''))

    def set_default_options(self):
        self.options['game_sum_by_diff'] = True
        self.options['dark_allowed'] = False
        self.options['third_pass_limit'] = False
        self.options['fail_subtract_all'] = False
        self.options['no_joker'] = False
        self.options['joker_give_at_par'] = False
        self.options['joker_demand_peak'] = True
        self.options['pass_factor'] = 5
        self.options['gold_mizer_factor'] = 15
        self.options['dark_notrump_factor'] = 20
        self.options['brow_factor'] = 50
        self.options['dark_mult'] = 2
        self.options['gold_mizer_on_null'] = True
        self.options['on_all_order'] = True
        self.options['take_block_bonus'] = True

    def start_game(self):
        """ Старт игры - инициализация игры и показ игрового поля """

        # Настройка договоренностей игры, игроков и т.п.
        # todo: Пока что накидываем все опции дефолтно, без возможности выбора. Потом сделаю форму
        robots = [r for r in const.ROBOTS]
        humans = [h for h in const.HUMANS]
        self.players = []
        self.bet = 10
        self.set_default_options()

        for i in range(random.choice([3, 4])):
            if i == 0:
                self.players.append(helpers.Player())
                self.players[i].id = i
                self.players[i].is_robot = False
                self.players[i].name = f'{humans.pop(random.randrange(0, len(humans)))}'
            else:
                self.players.append(helpers.Player())
                self.players[i].id = i
                self.players[i].is_robot = True
                self.players[i].name = f'{robots.pop(random.randrange(0, len(robots)))}'
                self.players[i].risk_level = random.randint(0, 2)

        self.options['deal_types'] = [n for n in range(len(eng_const.DEAL_NAMES) - 1)]

        self.game = engine.Engine(self.players, self.bet, allow_no_human=False, **self.options)
        self.game.start()

        # И поехала игра
        if self.game.started():
            self.init_game_table()

    def stop_game(self):
        """ Скрыть игровое поле """

    def init_game_table(self):
        """ Показ игрового поля, отображение на нем игроков """
