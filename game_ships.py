from random import randint

# класс точек на поле

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел вне доски!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "В эту точку вы уже стреляли!"


class BoardWrongShipException(BoardException):
    pass

# класс корабля на игровом поле

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l


    # свойства корабля

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            curent_x = self.bow.x
            curent_y = self.bow.y

            if self.o == 0:
                curent_x += i

            elif self.o == 1:
                curent_y += i

            ship_dots.append(Coord(curent_x, curent_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

# класс игровой доски

class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["o"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        res +='\n -------------------------'
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "o")
        return res

    def outboard(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def add_ship(self, ship):

        for d in ship.dots:
            if self.outboard(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contourship(ship)

    def contourship(self, ship, verboard=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                curent = Coord(d.x + dx, d.y + dy)
                if not (self.outboard(curent)) and curent not in self.busy:
                    if verboard:
                        self.field[curent.x][curent.y] = "."
                    self.busy.append(curent)

    # выстрелы

    def shot(self, d):
        if self.outboard(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contourship(ship, verboard=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "T"
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

# класс игрока общий

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    #запрос о выстреле
    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

# класс игрока компьютер

class AI(Player):
    def ask(self):
        d = Coord(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d

# класс игрока пользователь

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Coord(x-1, y-1)

# класс игры

class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.board_ship()
        comp = self.board_ship()
        comp.hid = True

        self.ai = AI(comp, pl)
        self.us = User(pl, comp)



    def place_ship(self):
        lenships = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lenships:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Coord(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def board_ship(self):
        board = None
        while board is None:
            board = self.place_ship()
        return board


    def hello(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" Чтобы сделать выстрел,\n введите две координаты: ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Ваша доска")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)

                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Вы выиграли!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.hello()
        self.loop()


g = Game()
g.start()