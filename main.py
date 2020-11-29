from tkinter import *
from copy import *

#  --\\\\\\\\\\\\\\\\\\\\\\\\\\------\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\---------------------\\
#  --//////////////////////////------/////////////////////////////////////---------------------//

# Нужно сделать
# TODO: главное меню (выбор скорости, начать игру)
# TODO: game over окно (выбор скорости, обновить рейтинг, начать заново)
# TODO: рейтинг (в game over и в самой игре)
# TODO: автоматическое сохранение рейтинга (через файлик)
# TODO: передвижение змеи
# TODO: game over при пожирании своего тела
# TODO: рандомная генерация еды
# TODO: рандомная генерация еды при старте игры
#
# Просто идеи
# TODO: (тип игры) уровни
# TODO: пауза, сохранить в файл, открыть файл и продолжить игру
# TODO: клетка тела змеи меньше на n%
# TODO: (тип игры) при пожирании себя, змейка продолжает играть без откусанного тела (откусанное тело исчезает)

#  --\\\\\\\\\\\\\\\\\\\\\\\\\\------\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\---------------------\\
#  --//////////////////////////------/////////////////////////////////////---------------------//


class Application(Frame):
    move_bool = False

    def __init__(self, title='Snake', width_render=600, height_render=600, x_pixel_amount=10, y_pixel_amount=10,
                 primary_color='#31DAFF', secondary_color='#000d12', speed=500):
        self.__window = Tk()
        self.__window.title(title)
        self.__speed = speed
        super().__init__(self.__window)

        self.__render = Render(self.__window, width_render, height_render, x_pixel_amount, y_pixel_amount,
                               primary_color, secondary_color)

    def run(self):
        self.move_bool = not self.move_bool

        if not self.move_bool:
            self.__render.move_snake()

        self.__render.run()
        self.after(int(self.__speed / 2), self.run)


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass


class Food(Singleton):
    __clear = True

    def __init__(self, field):
        self.__field = deepcopy(field)
        self.__field[2][3] = True

    def coordinates(self):
        self.__clear = not self.__clear

        return self.__field if not self.__clear else []


class Snake(Singleton):
    def __init__(self, field):
        self.__field = deepcopy(field)
        self.__field[5][5] = True
        self.__field[5][6] = True
        self.__field[5][7] = True

    def coordinates(self):
        return self.__field

    def move(self):
        print(123)

        return True  # TODO: если истина, то жив


class Field(Singleton):
    def __init__(self, x_pixel_amount, y_pixel_amount):
        self.__x_pixel_amount = x_pixel_amount
        self.__y_pixel_amount = y_pixel_amount
        self.__field = [[False for _ in range(self.__y_pixel_amount)] for _ in range(self.__x_pixel_amount)]
        self.__food = Food(self.__field)
        self.__snake = Snake(self.__field)

    def field(self):
        return self.__field

    def food_coordinates(self):
        return self.__food.coordinates()

    def snake_coordinates(self):
        return self.__snake.coordinates()

    def move_snake(self):
        return self.__snake.move()

    def x_pixel_amount(self):
        return self.__x_pixel_amount

    def y_pixel_amount(self):
        return self.__y_pixel_amount


class Render(Singleton):
    def __init__(self, window, width, height, x_pixel_amount, y_pixel_amount, primary_color, secondary_color):
        self.__field = Field(x_pixel_amount, y_pixel_amount)
        self.__width = width
        self.__height = height
        self.__primary_color = primary_color
        self.__secondary_color = secondary_color
        self.__render = Canvas(window, width=width, height=height, bg=secondary_color)
        self.__render.focus_set()
        self.__render.pack()

    def run(self):
        self.__render_bg()
        self.__render_field()
        self.__render_food()
        self.__render_snake()

    def move_snake(self):
        return self.__field.move_snake()

    def __render_field(self):
        for width_num, width_item in enumerate(self.__field.field()):
            y = width_num * (self.__width / self.__field.y_pixel_amount())

            self.__render.create_line((0, y, self.__height, y), fill=self.__primary_color)

            for height_num, height_item in enumerate(width_item):
                x = height_num * (self.__height / self.__field.x_pixel_amount())

                self.__render.create_line((x, 0, x, self.__width), fill=self.__primary_color)

    def __render_bg(self):
        self.__render.create_rectangle(0, 0, self.__width, self.__height, fill=self.__secondary_color)

    def __render_food(self):
        self.__render_pixel(self.__field.food_coordinates())

    def __render_snake(self):
        self.__render_pixel(self.__field.snake_coordinates())

    def __x_size(self):
        return self.__width / self.__field.x_pixel_amount()

    def __y_size(self):
        return self.__height / self.__field.y_pixel_amount()

    def __pixel(self, x_num, y_num, padding=3):
        x1 = x_num * self.__x_size()
        y1 = y_num * self.__y_size()
        x2 = x1 + self.__x_size()
        y2 = y1 + self.__y_size()

        self.__render.create_rectangle(x1 + padding, y1 + padding, x2 - padding, y2 - padding,
                                       fill=self.__primary_color)

    def __render_pixel(self, coordinates, padding=3):
        for x_num, width_item in enumerate(coordinates):
            for y_num, height_item in enumerate(width_item):
                if height_item:
                    self.__pixel(x_num, y_num, padding)


app = Application()
app.run()
app.mainloop()
