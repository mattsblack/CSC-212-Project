from imageai.Detection import VideoObjectDetection
import os
import math
import turtle
import random
import cv2

execution_path = os.getcwd()

drawn = False

bg = turtle.Screen()
bg.title('Object Map')
bg.setup(900,600)
bg.tracer()

objlist = []

roomLen = 20
roomWid = 20

def new_object(name, width, length, centerx, centery):
    new_object = object(name, width, length, centerx, centery)
    objlist.append(new_object)
    

def forFrame(frame_number, output_array, output_count):
    #default print statement for each frame (from ImageAI)
    print("FOR FRAME " , frame_number)
    print("Output for each object : ", output_array)
    print("Output count for unique objects : ", output_count)
    print("------------END OF A FRAME --------------")
    
    #object creation for the mapping system
    for i in output_array:
        draw = True
        name = i["name"]
        iwidth = i["box_points"][0] - i["box_points"][2]
        iwidth /= 100
        #compares against each existing object to see if the one it sees already exists
        for j in objlist:
            if i["name"] == j.name and (abs(iwidth - j.width)) < 1:
                draw = False
                break
        #if it is not drawn it will draw a new turtle
        if draw:
            # Because you can only receive a limited amount of information from a 2d image random numbers were used to generate unknown dimensions of the object.
            # In theory if the robot was able to move i would have been able to replace this part with actual data.
            length = (random.random()+1)*2
            centerx = iwidth/2 + random.random()*20
            centery = length/2 + random.random() *20
            
            
            # Sends data to the a new object and adds it to a list of all objects found in the room.
            new_object = object(name, iwidth, length, centerx, centery)
            objlist.append(new_object)
            
        
    draw_map()

#function to draw a map of the room
def draw_map():
    global drawn
    if not drawn:
        #Pen to draw the map
        pen = turtle.Turtle()
        pen.hideturtle()
        pen.clear()
        pen.speed(0)
        pen.width(2)
        pen.color('Black')
        pen.penup()
        pen.goto(-1*(roomWid*12.5), -1*(roomLen*12.5))
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
        # Sets bool to true so the map is not redrawn every frame.
        drawn = True

    for i in objlist:
        i.create_turtle()

#class for the objects that are found in the room
class object:
    name = ""
    length = 0
    width = 0
    t = 0
    #Creates the object with the parameters
    def __init__(self, name, width, length, centerx, centery):
        self.name = name
        self.width = width
        self.length = length
        self.centerx = centerx
        self.centery = centery
    
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

    
    #checks if turtle exists already then creates a new if it doesnt
    def create_turtle(self):
        if not self.t:
            self.t = turtle.Turtle()
            self.t.hideturtle()
            self.t.shape("square")
            self.t.penup()
            self.t.goto(25*(self.centerx-(roomWid/2)), 25*(self.centery-(roomLen/2)))
            self.t.shapesize(self.width*1.25, self.length*1.25)
            #self.t.seth(self.rotation)
            self.t.showturtle()
        



#setting up the image detection AI (from ImageAI)
camera = cv2.VideoCapture(0)
detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path , "yolov3.pt"))
detector.loadModel()

#ImageAI video detection code
video_path = detector.detectObjectsFromVideo(
                camera_input=camera,
                output_file_path=os.path.join(execution_path, "camera_detected_video2"),
                frames_per_second=20, log_progress=True, minimum_percentage_probability=40,
                per_frame_function = forFrame, detection_timeout = 120)
