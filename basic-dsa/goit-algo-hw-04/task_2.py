import sys
import turtle
import argparse

MAX_LEVEL = 6
SIDE_LENGTH = 450


def read_level() -> int:
    parser = argparse.ArgumentParser(description="Draw the Koch snowflake fractal.")
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


def koch_curve(pen: turtle.Turtle, level: int, length: float) -> None:
    if level == 0:
        pen.forward(length)
        return

    for angle in (60, -120, 60, 0):
        koch_curve(pen, level - 1, length / 3)
        pen.left(angle)


def draw_snowflake(level: int, length: float = SIDE_LENGTH) -> None:
    screen = turtle.Screen()
    screen.title(f"Koch snowflake - recursion level {level}")
    screen.bgcolor("white")
    screen.tracer(0)

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.color("navy")
    pen.penup()
    pen.goto(-length / 2, length / 3)
    pen.pendown()

    for _ in range(3):
        koch_curve(pen, level, length)
        pen.right(120)

    screen.update()
    screen.exitonclick()


def main() -> None:
    level = read_level()
    print(f"Drawing the Koch snowflake of level {level}. Click on the window to close it.")
    draw_snowflake(level)


main()
