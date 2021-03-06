#Lillie Widmayer
#TP prelim code

from __future__ import print_function
from __future__ import division
from mathAlgorithms import *
from Tkinter import *
import pytesseract
from PIL import Image
import cv2
import os


def init(data):
    data.gameState = "start"
    data.startButtonCx = data.width/2
    data.startButtonCy = 2*data.height/3
    data.startButtonLength = 57
    data.startButtonHeight = 15
    data.buttonLength = 100
    data.buttonHeight = 50
    data.equation = ""
    data.answer = 0
    data.fileName = ""

def drawStart(canvas, data):
    canvas.create_rectangle(data.startButtonCx-data.startButtonLength,
        data.startButtonCy-data.startButtonHeight, 
        data.startButtonCx+data.startButtonLength, 
        data.startButtonCy+data.startButtonHeight, fill="lightblue")
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
    canvas.create_text(data.width /4, data.height/2, text="Click to Load an" +
        " Image", font="Impact 20")
    canvas.create_text(3*data.width/4, data.height/2, text="Click to use Camera"
        , font="Impact 20")



def doMathScreen(canvas, data):
    canvas.create_rectangle(data.width-50, data.height-50, data.width-10,
        data.height-10, fill="RoyalBlue1")   
    canvas.create_text(data.width-30, data.height-30, text="Home", 
        font="Times 10")
    ans = whichAlgorithm(data.equation)
    if ans != None:
        if "=" in data.equation:
            canvas.create_text(data.width/2, data.height/2,
                text=("%s %s" % (data.equation, ans)), font="Impact 50")
        else:
            canvas.create_text(data.width/2, data.height/2,
                text=("%s = %s" % (data.equation, ans)), font="Impact 50")
    else:    
        data.gameState = "error"

def errorScreen(canvas, data):
    canvas.create_rectangle(data.width/2-45, data.height/2 + 40, 
        data.width/2+45, data.height/2+70, fill="RoyalBlue1")   
    canvas.create_text(data.width/2, data.height/2+55, text="Try Again", 
        font="Times 15")
    canvas.create_text(data.width/2, data.height/2, font="Impact 20",
        text="          Uh Oh! \n Retake Picture")

def openCamera():
#modified from Vasu's github code snippets
    window_name = "Camera"
    cam_index = 0
    cv2.namedWindow(window_name)
    cap = cv2.VideoCapture(cam_index)
    cap.open(cam_index)
# Loop until spacebar is pressed
    while True:
        ret, frame = cap.read()
        if frame is not None:
            cv2.imshow(window_name, frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 32:
#take photo if spacebar is pressed
            ret, picture = cap.read()
            cv2.imshow(window_name, picture)
            cv2.imwrite("mathImage.png", picture)
            break

def solveEquation(data):
    fileName = "mathImage.png"
    image = cv2.imread(fileName)
    data.equation = pytesseract.image_to_string(Image.open(fileName))


def loadImage(data):
    fileName = raw_input("File Name: ")
    image = cv2.imread(fileName)
    data.equation = pytesseract.image_to_string(Image.open(fileName))

def mousePressed(event, data):
    if data.gameState == "start":
        if (event.x > data.startButtonCx-data.startButtonLength and event.x < 
            data.startButtonCx+data.startButtonLength):
            if (event.y > data.startButtonCy-data.startButtonHeight and 
                event.y < data.startButtonCy+data.startButtonHeight):
                    data.gameState = "solve"

    if data.gameState == "solve":
        if (event.x > data.width/4-data.buttonLength and 
            event.x < data.width/4 + data.buttonLength):
            if (event.y > data.height/2-data.buttonHeight and event.y < 
                data.height/2+data.buttonHeight):
                loadImage(data)
                data.gameState = "doMath"            
                # whichAlgorithm(data)


    if data.gameState == "solve":
        if (event.x > 3*data.width/4-data.buttonLength and 
            event.x < 3*data.width/4 + data.buttonLength):
            if (event.y > data.height/2-data.buttonHeight and event.y < 
                data.height/2+data.buttonHeight):
                openCamera()
                solveEquation(data)
                data.gameState = "doMath"

    if data.gameState == "error":
        if (event.x > data.width/2-45 and event.x < data.width/2+45):
            if (event.y > data.height/2+40 and event.y < data.height/2+70):
                openCamera()
                solveEquation(data)
                data.gameState = "doMath"

    if data.gameState == "doMath":
        if (event.x > data.width-50 and event.x < data.width-10):
            if (event.y > data.height-50 and event.y < data.height-10):
                cv2.destroyAllWindows()
                data.gameState = "start"


def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if data.gameState == "start":
        drawStart(canvas, data)
    elif data.gameState == "solve":
        drawSolve(canvas,data)
    elif data.gameState == "doMath":
        doMathScreen(canvas, data)
    elif data.gameState == "error":
        errorScreen(canvas, data)



###############################
#run function from 112 Website
###############################

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

run(500, 500)
