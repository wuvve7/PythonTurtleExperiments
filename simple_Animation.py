import turtle
from random import randint
import time

# وظيفة لكتابة اسم اللاعب بشكل مرئي
def write_player_name(player, name):
    player.penup()
    player.goto(-160, player.ycor() + 20)  # ضبط الموقع ليكون فوق اللاعب
    player.write(name, align="center", font=("Arial", 12, "normal"))
    player.goto(-160, player.ycor() - 20)  # العودة للموقع الأصلي بعد الكتابة

# وظيفة لبدء السباق
def race(players, finish_line):
    race_over = False
    while not race_over:
        for player in players:
            player.forward(randint(1, 5))  # تحرك كل لاعب خطوة عشوائية
            if player.xcor() > finish_line:  # تحقق من فوز اللاعب
                race_over = True
                winner = player
                break
    return winner

# إعداد نافذة الترتيل
screen = turtle.Screen()
screen.bgcolor("white")

# إعداد المسار
track = turtle.Turtle()
track.hideturtle()
track.penup()
track.goto(-160, 150)
track.pendown()

# رسم المسار
for step in range(15):
    track.write(step, align='center')
    track.right(90)
    for num in range(8):
        track.penup()
        track.forward(10)
        track.pendown()
        track.forward(10)

    track.penup()
    track.backward(160)
    track.left(90)
    track.forward(20)

# إعداد اللاعبين
players = []

# إضافة اللاعبين
colors = ['red', 'blue', 'green', 'orange']
names = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
for i in range(4):
    player = turtle.Turtle()
    player.shape('turtle')
    player.color(colors[i])
    player.penup()
    player.goto(-160, 100 - (i * 30))  # تحديد المواقع بشكل مناسب لكل لاعب
    players.append(player)
    write_player_name(player, names[i])  # كتابة اسم اللاعب

# إضافة خط النهاية
finish_line = 140

# إعداد المؤقت
start_time = time.time()

# بداية السباق
print("Race Started!")
winner = race(players, finish_line)

# طباعة الفائز
end_time = time.time()
race_duration = round(end_time - start_time, 2)

# إظهار الفائز ومدة السباق
winner_name = winner.color()[0].capitalize()
print(f"{winner_name} wins the race!")
print(f"Race Duration: {race_duration} seconds")

# إخفاء السلاحف بعد السباق
for player in players:
    player.hideturtle()

# إنهاء الرسومات
turtle.done()
