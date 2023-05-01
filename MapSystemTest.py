import turtle
from PIL import Image

#Creates the background
bg = turtle.Screen()
bg.title('Object Map')
bg.setup(900,600)
bg.tracer()

list = []

roomLen = int(input("Input Room Length: "))
roomWid = int(input("Input Room Width: "))



#Creates a new object and adds it to the list
def new_object():
    name = input("Input Name: ")
    length = int(input("Input Length: "))
    width = int(input("Input Width: "))
    centerx = float(input("Input Center X-Coor: "))
    centery = float(input("Input Center Y-Coor: "))
    rotation = int(input("Input Rotation in Degrees: "))
    new_object = object(name, width, length, centerx, centery, rotation)
    list.append(new_object)

#Changes the size of the room
def resize_room():
    roomLen = int(input("Input Room Length: "))
    roomWid = int(input("Input Room Width: "))

#Prints information about the room followed by each object in the room
def print_objects():
    print(f"The room is {roomLen}ft X {roomWid}ft, {roomLen*roomWid} Square Feet.")
    for i in list:
        print(i)


def draw_map():
    #Pen to draw the map
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.clear()
    pen.speed(0)
    pen.width(2)
    pen.color('Black')
    pen.penup()
    pen.goto(-1*(roomWid*25/2), -1*(roomLen*25/2))
    pen.seth(0)
    pen.pendown()
    for i in range(2):
        pen.forward(25*roomWid)
        pen.left(90)
        pen.forward(25*roomLen)
        pen.left(90)
    pen.width(1)
    pen.color('grey')
    for i in range(int(roomWid/2)):
        pen.forward(25)
        pen.left(90)
        pen.forward(roomLen*25)
        pen.right(90)
        pen.forward(25)
        pen.right(90)
        pen.forward(roomLen*25)
        pen.left(90)
    pen.left(90)
    for i in range(int(roomLen/2)):
        pen.forward(25)
        pen.left(90)
        pen.forward(roomWid*25)
        pen.right(90)
        pen.forward(25)
        pen.right(90)
        pen.forward(roomWid*25)
        pen.left(90)

    
    for i in list:
        i.create_turtle()
        # time.sleep(0.2)
        # print(i)
        # print("Created")

#Saves the map to an image file
def save_map():
    name = input("Enter File Name: ")
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file=f"{name}.eps")
    image = Image.open(f"{name}.eps")
    image.save(f"{name}", "png", bitmap_format= "png")
    




#Class for the objects in a room, has 2 dimensions and a name
class object:
    name = ""
    length = 0
    width = 0
    t = 0
    #Creates the object with the parameters
    def __init__(self, name, width, length, centerx, centery, rotation):
        self.name = name
        self.width = width
        self.length = length
        self.centerx = centerx
        self.centery = centery
        self.rotation = rotation
    
    #Prints information about the object
    def __str__(self):
        return f"{self.name}, {self.width}ft X {self.length}ft, Area: {self.length*self.width} Square Feet."
    
    #The "Get" functions for the objects
    def getWid(self):
        return self.width
    def getLen(self):
        return self.length
    def getRot(self):
        return self.rotation
    def getCenX(self):
        return self.centerx
    def getCenY(self):
        return self.centery
    
    def create_turtle(self):
        if not self.t:
            self.t = turtle.Turtle()
            self.t.hideturtle()
            self.t.shape("square")
            self.t.penup()
            self.t.goto(25*(self.centerx-(roomWid/2)), 25*(self.centery-(roomLen/2)))
            self.t.shapesize(self.width*25/20.0, self.length*25/20.0)
            self.t.seth(self.rotation)
            self.t.showturtle()
        


input1 = input("Input Command: ")

#Cycles through inputs until q is entered
while input1 != "q":
    if input1 == "n":
        new_object()
    elif input1 == "p":
        print_objects()
    elif input1 == "r":
        resize_room()
    elif input1 == "d":
        draw_map()
    elif input1 == "s":
        save_map()
    else:
        input1 = input("Input Not Found Try a New Command: ")
        continue
    
    input1= input("Next Command: ")
