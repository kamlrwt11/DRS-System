import tkinter
import cv2
import PIL.Image,PIL.ImageTk
import threading
from functools import partial
import time
import imutils 

stream = cv2.VideoCapture("clip.mp4")
flag = True
def play(speed):
    global flag
    print(f"You clicked on play.Speed is {speed}")
    
    # play the video in reversed
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    
    grabbed,frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=set_width, height= set_height)
    frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134,26, fill="black", font="Times 26 bold", text="Decision Pending")
    flag = not flag
    

def pending(decision):
    # Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=set_width, height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    
    # Wait for 1 second
    time.sleep(1)
    
    # Display out Sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=set_width, height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    
    # wait for 1.5 second
    time.sleep(1.5)
    
    # Display out/notout image
    if decision == 'out':
        decisionImg = "out.png"
    else:
        decisionImg = "not_out.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=set_width, height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    
    # wait for 1.5 second


def out():
    # Thread is used for safage from blocking so that our program will not stop.
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")


def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")


# width and height of our main screen
set_width = 650
set_height = 368

# tkinter gui starts here
window = tkinter.Tk()
window.title("Third Umpire Decision Review Kit")

# it defines where to add the image, the background and size
canvas = tkinter.Canvas(window, width=set_width, height=set_height)

# it is used to convert an image from one color space to another.
cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)

# it is used for showimg image in our window
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

# to display a graphics image on a canvas & the ancho tag is used for positioning of the image
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()

#buttons to control playback
btn = tkinter.Button(window, text="<<Previous (fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<<Previous (slow)",width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (slow)>>",width=50, command=partial(play, +2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast)>>",width=50, command=partial(play, +25))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()

window.mainloop()
