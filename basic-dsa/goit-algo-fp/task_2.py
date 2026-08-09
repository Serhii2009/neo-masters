import sys
import math
import turtle
import argparse

MAX_LEVEL = 12
BASE_SIZE = 100
RATIO = 1 / math.sqrt(2)


def read_level() -> int:
    parser = argparse.ArgumentParser(description="Draw the Pythagoras tree fractal.")
    parser.add_argument(
        "level",
        nargs="?",
        type=int,
        help=f"recursion level from 0 to {MAX_LEVEL}",
    )
    level = parser.parse_args().level

    while level is None or not 0 <= level <= MAX_LEVEL:
        if level is not None:
            print(f"The recursion level must be between 0 and {MAX_LEVEL}.")

        try:
            level = int(input(f"Enter the recursion level (0-{MAX_LEVEL}): "))
        except ValueError:
            print("Please enter an integer.")
            level = None
        except EOFError:
            print("\nNo recursion level provided.")
            sys.exit(1)

    return level


def move(pen: turtle.Turtle, distance: float) -> None:
    pen.penup()
    pen.forward(distance)
    pen.pendown()


def move_back(pen: turtle.Turtle, distance: float) -> None:
    pen.penup()
    pen.backward(distance)
    pen.pendown()


def draw_square(pen: turtle.Turtle, size: float) -> None:
    for _ in range(4):
        pen.forward(size)
        pen.left(90)


def pythagoras_tree(pen: turtle.Turtle, size: float, level: int) -> None:
    if level == 0:
        return

    pen.pencolor(leaf_color(level))
    draw_square(pen, size)
    child = size * RATIO

    pen.left(90)
    move(pen, size)
    pen.right(90)

    pen.left(45)
    pythagoras_tree(pen, child, level - 1)

    move(pen, child)
    pen.right(90)
    pythagoras_tree(pen, child, level - 1)

    pen.left(90)
    move_back(pen, child)
    pen.right(45)
    pen.left(90)
    move_back(pen, size)
    pen.right(90)


def leaf_color(level: int) -> str:
    if level > MAX_LEVEL - 2:
        return "#6B4423"

    ratio = min(1.0, (MAX_LEVEL - level) / MAX_LEVEL)
    red = round(107 + (60 - 107) * ratio)
    green = round(68 + (170 - 68) * ratio)
    blue = round(35 + (70 - 35) * ratio)
    return f"#{red:02X}{green:02X}{blue:02X}"


def draw_fractal(level: int) -> None:
    screen = turtle.Screen()
    screen.setup(1000, 750)
    screen.title(f"Pythagoras tree - recursion level {level}")
    screen.bgcolor("white")
    screen.tracer(0)

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()
    pen.goto(-BASE_SIZE / 2, -200)
    pen.setheading(0)
    pen.pendown()

    pythagoras_tree(pen, BASE_SIZE, level)

    screen.update()
    screen.exitonclick()


def main() -> None:
    level = read_level()
    squares = 2 ** level - 1
    print(f"Drawing the Pythagoras tree of level {level}, {squares} squares.")
    print("Click on the window to close it.")
    draw_fractal(level)


main()
