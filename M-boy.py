import random

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, length, bow, direction):
        self.length = length
        self.bow = bow
        self.direction = direction
        self.lives = length
    
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            if self.direction == "vertical":
                dot = Dot(self.bow.x, self.bow.y + i)
            else:
                dot = Dot(self.bow.x + i, self.bow.y)
            ship_dots.append(dot)
        return ship_dots

class Board:
    def __init__(self, size):
        self.size = size
        self.field = [["O"] * size for _ in range(size)]
        self.ships = []
        self.hidden = True
        self.ships_left = 0
    
    def add_ship(self, ship):
        for dot in ship.dots():
            if self.out(dot) or dot in self.ships:
                raise BoardOutException()
        for dot in ship.dots():
            self.field[dot.x][dot.y] = "■"
            self.ships.append(dot)
            self.contour(dot)
        self.ships_left += 1
    
    def contour(self, dot):
        contour_dots = [Dot(dot.x-1, dot.y-1), Dot(dot.x-1, dot.y), Dot(dot.x-1, dot.y+1),
                        Dot(dot.x, dot.y-1), Dot(dot.x, dot.y+1),
                        Dot(dot.x+1, dot.y-1), Dot(dot.x+1, dot.y), Dot(dot.x+1, dot.y+1)]
        for contour_dot in contour_dots:
            if not self.out(contour_dot) and contour_dot not in self.ships:
                self.field[contour_dot.x][contour_dot.y] = "."
    
    def out(self, dot):
        return not (0 <= dot.x < self.size and 0 <= dot.y < self.size)
    
    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()
        if dot in self.ships:
            self.field[dot.x][dot.y] = "X"
            self.ships.remove(dot)
            self.ships_left -= 1
            print("Попадание!")
            if self.ships_left == 0:
                raise GameOverException("Вы победили!")
        else:
            self.field[dot.x][dot.y] = "."
            print("Мимо!")
    
    def __str__(self):
        board_str = ""
        for row in self.field:
            board_str += " ".join(row) + "\n"
        return board_str

class BoardOutException(Exception):
    pass

class GameOverException(Exception):
    pass

class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board
    
    def move(self):
        raise NotImplementedError()

class User(Player):
    def move(self):
        while True:
            try:
                x = int(input("Введите номер строки: "))
                y = int(input("Введите номер столбца: "))
                dot = Dot(x, y)
                self.enemy_board.shot(dot)
                break
            except ValueError:
                print("Введите целое число!")
            except BoardOutException:
                print("Координаты выходят за пределы поля!")
            except Exception as e:
                print(e)

class AI(Player):
    def move(self):
        while True:
            x = random.randint(0, self.board.size-1)
            y = random.randint(0, self.board.size-1)
            dot = Dot(x, y)
            try:
                self.enemy_board.shot(dot)
                break
            except BoardOutException:
                continue
            except Exception as e:
                print(e)

class Game:
    def __init__(self, size=6):
        self.size = size
        self.user_board = Board(size)
        self.ai_board = Board(size)
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)
    
    def random_board(self, board):
        ships = [3, 2, 2, 1, 1, 1, 1]
        for ship_length in ships:
            while True:
                direction = random.choice(["vertical", "horizontal"])
                x = random.randint(0, self.size-1)
                y = random.randint(0, self.size-1)
                ship_bow = Dot(x, y)
                ship = Ship(ship_length, ship_bow, direction)
                try:
                    board.add_ship(ship)
                    break
                except BoardOutException:
                    continue
    
    def greet(self):
        print("Добро пожаловать в игру 'Морской бой'!")
        print("Формат ввода координат: номер строки, номер столбца.")
    
    def loop(self):
        while True:
            print("Ваша доска:")
            print(self.user_board)
            print("Доска противника:")
            print(self.ai_board)
            try:
                if self.user.move():
                    continue
                if self.ai.move():
                    continue
            except GameOverException as e:
                print(e)
                break
    
    def start(self):
        self.greet()
        self.random_board(self.user_board)
        self.random_board(self.ai_board)
        self.loop()

game = Game()
game.start()