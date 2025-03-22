import turtle

#إعداد الشاشة
sc = turtle.Screen()
sc.setup(600, 600)
sc.bgcolor('black')

# إنشاء الكائن (pen) الذي سيرسم الأشكال
pen = turtle.Turtle()
pen.width(10)
pen.speed(7)
pen.right(90)

# تعريف دالة لرسم نصف دائرة بلون ونصف قطر ديناميكي
def semi_circle(col, rad, val):
    pen.color(col)
    pen.circle(rad, -180)
    pen.up()
    pen.setpos(val, 0)
    pen.down()
    pen.right(180)

# تحديد الألوان لكل نصف دائرة
col = ['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']

for i in range(7):
    semi_circle(col[i], 10*(i + 8), -10*(i + 1))

pen.hideturtle()
turtle.done()
