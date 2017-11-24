#Lillie Widmayer
#TP prelim code

from Tkinter import *
import numpy as np
import pytesseract
from PIL import Image
import cv2
import os

def init(data):
    data.gameState = "start"
    data.startButtonCx = data.width/2
    data.startButtonCy = 2*data.height/3
    data.startButtonLength = 55
    data.startButtonHeight = 15
    data.buttonLength = 100
    data.buttonHeight = 50
    data.equation = ""

def drawStart(canvas, data):
    canvas.create_rectangle(data.startButtonCx-data.startButtonLength,
        data.startButtonCy-data.startButtonHeight, 
        data.startButtonCx+data.startButtonLength, 
        data.startButtonCy+data.startButtonHeight, fill="lightblue", width=0)
    canvas.create_text(data.startButtonCx, data.startButtonCy, text=("Click " +
        "to Start"), font="Times 20")
    canvas.create_text(data.width/2, data.height/3, text="MathMate", 
        font="Impact 50")

def drawSolve(canvas, data):
    canvas.create_rectangle(data.width/4-data.buttonLength, 
        data.height/2-data.buttonHeight, data.width/4 + data.buttonLength,
        data.height/2+data.buttonHeight)
    canvas.create_rectangle(3*data.width/4-data.buttonLength, 
        data.height/2-data.buttonHeight, 3*data.width/4 + data.buttonLength,
        data.height/2+data.buttonHeight)
    canvas.create_text(data.width/4, data.height/2, text="Click to Load an" +
        " Image", font="Impact 20")
    canvas.create_text(3*data.width/4, data.height/2, text="Click to use Camera"
        , font="Impact 20")

def loadingImage(data):
    # image = input("Enter File Name: ")
    data.gameState = "doMath"
    image = cv2.imread("testImage.png")
    fileName = "{}.png".format(os.getpid())
    cv2.imwrite(fileName, image)
    # equation = tesseract_images/testImage.png stdout
    
    data.equation = pytesseract.image_to_string(Image.open(fileName))
    # canvas.create_text(data.width/2, data.height/2, text = equation)
    os.remove(fileName)
    cv2.waitKey(0)

def doMathScreen(canvas, data):
    canvas.create_text(data.width/2, data.height/2, text=str(data.equation))

def openCamera():
    cam = cv2.VideoCapture(0)
    k = cv2.waitKey(0) & 0xFF
    while True:
        _, frame = cam.read()

        cv2.imshow('frame', frame)

        if k == 32:
#take photo if spacebar is pressed
            ret, picture = cam.read()
            cv2.imshow("image", picture)
            cv2.imread("mathImage.png")
            cv2.imwrite("mathImage.png", picture)


def mousePressed(event, data):
    if data.gameState == "start":
        if (event.x > data.startButtonCx-data.startButtonLength and event.x < 
            data.startButtonCx+data.startButtonLength):
            if (event.y > data.startButtonCy-data.startButtonHeight and event.y <
                    data.startButtonCy+data.startButtonHeight):
                    data.gameState = "solve"

    if data.gameState == "solve":
        if (event.x > data.width/4-data.buttonLength and 
            event.x < data.width/4 + data.buttonLength):
            if (event.y > data.height/2-data.buttonHeight and event.y < 
                data.height/2+data.buttonHeight):
                data.gameState = "doMath"            
                loadingImage(data)


    if data.gameState == "solve":
        if (event.x > 3*data.width/4-data.buttonLength and 
            event.x < 3*data.width/4 + data.buttonLength):
            if (event.y > data.height/2-data.buttonHeight and event.y < 
                data.height/2+data.buttonHeight):
                openCamera()


def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if data.gameState == "start":
        drawStart(canvas, data)
    if data.gameState == "solve":
        drawSolve(canvas,data)
    if data.gameState == "doMath":
        doMathScreen(canvas, data)


############################
#run function from 112 website
############################
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(500,500)