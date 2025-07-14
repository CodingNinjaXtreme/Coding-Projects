import turtle
import time

# --- GLOBAL SETUP ---
screen = turtle.Screen()
screen.title("Breakout")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# --- GLOBAL MOVEMENT STATE ---
moving_left = False
moving_right = False
paddle_timer_started = False  # ensures move_paddle runs only once

# --- PADDLE MOVEMENT LOOP ---
def move_paddle():
    if moving_left and paddle.xcor() > -350:
        paddle.setx(paddle.xcor() - 10)
    if moving_right and paddle.xcor() < 350:
        paddle.setx(paddle.xcor() + 10)
    screen.ontimer(move_paddle, 16)

# --- KEY HANDLERS ---
def go_left():
    global moving_left
    moving_left = True

def stop_left():
    global moving_left
    moving_left = False

def go_right():
    global moving_right
    moving_right = True

def stop_right():
    global moving_right
    moving_right = False

# --- START GAME ---
def start_game():
    global paddle, moving_left, moving_right, paddle_timer_started

    # Reset key movement states
    moving_left = False
    moving_right = False

    screen.clear()
    screen.bgcolor("black")
    screen.title("Breakout")
    screen.setup(width=800, height=600)
    screen.tracer(0)

    # Paddle
    paddle = turtle.Turtle()
    paddle.shape("square")
    paddle.color("white")
    paddle.shapesize(stretch_wid=1, stretch_len=5)
    paddle.penup()
    paddle.goto(0, -250)

    # Ball
    ball = turtle.Turtle()
    ball.shape("circle")
    ball.color("red")
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 4
    ball.dy = 4

    # Bricks
    bricks = []
    colors = ["red", "orange", "yellow", "green", "blue"]
    y_pos = 250
    for color in colors:
        for x in range(-350, 400, 70):
            brick = turtle.Turtle()
            brick.shape("square")
            brick.color(color)
            brick.shapesize(stretch_wid=1, stretch_len=3)
            brick.penup()
            brick.goto(x, y_pos)
            bricks.append(brick)
        y_pos -= 30

    # Score display
    score = 0
    score_display = turtle.Turtle()
    score_display.color("white")
    score_display.penup()
    score_display.hideturtle()
    score_display.goto(0, 260)
    score_display.write("Score: 0", align="center", font=("Courier", 18, "bold"))

    # Key bindings
    screen.listen()
    screen.onkeypress(go_left, "Left")
    screen.onkeyrelease(stop_left, "Left")
    screen.onkeypress(go_right, "Right")
    screen.onkeyrelease(stop_right, "Right")

    screen.onkeypress(start_game, "r")  # restart key always active

    # Start paddle movement loop only once
    if not paddle_timer_started:
        move_paddle()
        paddle_timer_started = True

    # --- MAIN GAME LOOP ---
    game_running = True
    while game_running:
        screen.update()
        time.sleep(0.01)

        # Ball movement
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Wall collisions
        if ball.xcor() > 390 or ball.xcor() < -390:
            ball.dx *= -1
        if ball.ycor() > 290:
            ball.dy *= -1

        # Paddle collision
        if ball.ycor() < -230 and paddle.xcor() - 60 < ball.xcor() < paddle.xcor() + 60:
            ball.sety(-230)
            ball.dy *= -1

        # Bottom out
        if ball.ycor() < -290:
            game_running = False
            score_display.clear()
            score_display.write("GAME OVER - Press R to Restart", align="center", font=("Courier", 18, "bold"))

        # Brick collision
        for brick in bricks:
            if brick.distance(ball) < 40:
                ball.dy *= -1
                brick.goto(1000, 1000)  # remove offscreen
                bricks.remove(brick)
                score += 10
                score_display.clear()
                score_display.write(f"Score: {score}", align="center", font=("Courier", 18, "bold"))

        # Win condition
        if not bricks:
            game_running = False
            score_display.clear()
            score_display.write("YOU WIN! - Press R to Restart", align="center", font=("Courier", 18, "bold"))

# --- START SCREEN ---
intro = turtle.Turtle()
intro.hideturtle()
intro.color("white")
intro.penup()
intro.goto(0, 0)
intro.write("Press SPACE to Start", align="center", font=("Courier", 24, "bold"))

# --- Start game on SPACE ---
screen.listen()
screen.onkeypress(start_game, "space")

screen.mainloop()
