import time
import SudokuSolver
import sys
import turtle

print(f"start: {time.ctime()}")

screen = turtle.Screen()
screen.setup(width=800, height=800)
screen.bgcolor("lightgray")

FONT1 = ("Arial", 8, "normal")
FONT2 = ("Arial", 16, "bold")

empty_sign = '-'

print(f"init start: {time.ctime()}")

#allTurtles = [turtle.Turtle(shape="blank") for _ in range(82)]
boardOfTurtles = [[turtle.Turtle(shape="blank", visible=False) for _ in range(9)] for _ in range(9)]

infoTurtle = turtle.Turtle(shape="blank")
infoTurtle.penup()
infoTurtle.goto(-300,-300)

print(f"init done: {time.ctime()}")

def transform_coordinates(i: int, j: int):
    k = 60
    dx = -(9*k)//2
    dy = -(9*k)//2
    return (i*k + dx, (9-j)*k + dy)

print(f"setup start: {time.ctime()}")
# initial setup
turtle.speed(0)
turtle.penup()
for i in range(9):
    for j in range(9):
        (x,y) = transform_coordinates(i, j)
        t = boardOfTurtles[j][i]
        t.penup()
        t.speed(0)
        t.goto(x, y)

print(f"setup done: {time.ctime()}")

def draw_net():
    netx = 540
    nety = 190
    netPen = turtle.Turtle("blank")
    netPen.speed(0)
    #
    netPen.penup()
    netPen.goto(-300, -60)
    netPen.pendown()
    netPen.forward(netx)
    #
    netPen.penup()
    netPen.goto(-300, 130)
    netPen.pendown()
    netPen.forward(netx)
    #
    netPen.penup()
    netPen.goto(-125, -250)
    netPen.pendown()
    netPen.left(90)
    netPen.forward(netx)
    #
    netPen.penup()
    netPen.goto(55, -250)
    netPen.pendown()
    netPen.forward(netx)


def text_at_xy(x, y, text, f):
    turtle.penup()
    turtle.goto(x, y)
    turtle.write(text, font=f)


mode = 2

def UpdateBoard(cell: SudokuSolver.Cell, reason: str=''):
    if cell:
        val = str(cell.value) if cell.is_solved() else empty_sign
        cand = cell.str_candidates(' ')
        if len(cand) > 10:
            cand = cand[:10] + '\n' + cand[10:]
        t = boardOfTurtles[cell.i][cell.j]
        if mode == 1:
            t.clear()
            t.write(val, font=FONT2)
            pos = t.pos()
            t.penup()
            t.goto(pos[0] - 3*len(cell.candidates), pos[1] - 20)
            t.write(cand)
            t.goto(pos)
        else:
            t.clear()
            if cell.is_solved():
                t.write(val, font=FONT2)
            else:
                pos = t.pos()
                t.penup()
                t.goto(pos[0] - 3*len(cell.candidates), pos[1] - 10)
                t.write(cand, font=FONT1)
                t.goto(pos)
    #
    if reason:
        infoTurtle.clear()
        infoTurtle.write(f"{reason}")

draw_net()

print(f"start load: {time.ctime()}")

ss = SudokuSolver.SudokuSolver(UpdateBoard)

if len(sys.argv) > 1:
    f = open(sys.argv[1], "r")
else:
    f = open('sudoku1.txt', "r")

ss.load(f)
f.close()

print(f"end load: {time.ctime()}")

print(f"start solve: {time.ctime()}")
ss.solve()
print(f"end solve: {time.ctime()}")

#ShowBoard(ss.board)

screen.exitonclick()