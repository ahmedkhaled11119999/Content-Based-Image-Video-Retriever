from tkvideo import tkvideo
import numpy as np
import cv2 as cv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import glob
from tkinter import Entry
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
from features_calculater import get_image_features
import os


win = tk.Tk()
var_selectedFeature = IntVar()
var_ImgVid = IntVar()
featureDict = {0: "", 1: "Average Color Similarity : ", 2: "Dominant Color Similarity : ", 3: "Histogram Similarity : ", 4: "Object Detection Similarity : "}
featureLabel = tk.Label(win, text=featureDict.get(var_selectedFeature.get())+"0.55",
                                  bg="#0D379B", fg="white")
newImageLabel = tk.Label(win)
videoLabel = tk.Label(win)
openVideoButton = tk.Button(win)

# win.iconbitmap("parser_icon.ico")
win.title("Content Based Image/Video Retriever")
win.configure(background='#0D379B')
win.geometry("1000x700")
win.resizable(False, False)

fileEntryTextField = Entry()

# ----------------------------
# Functions:
# ----------------------------
searchImages = []
searchVideos = []
imageIndex = 0
videoIndex = 0
imagePath = ""
videoPath = ""

def nextImage():
    openVideoButton.destroy()
    videoLabel.destroy()
    global newImageLabel
    global imageIndex
    global searchImages
    global imagePath
    imagesNum = len(searchImages) - 1
    if imageIndex < imagesNum:
        imageIndex += 1
    elif imageIndex == imagesNum:
        imageIndex = 0
    imagePath = searchImages[imageIndex]
    image = Image.open(searchImages[imageIndex])
    image = image.resize((250, 250), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    newImageLabel.config(image=image)
    newImageLabel.image = image
    newImageLabel.pack()
    newImageLabel.place(x=685, y=130)
    indexLabel = tk.Label(win, text=str(imageIndex+1)+" of "+str(len(searchImages))+" Results", bg="#0D379B", fg="white")
    indexLabel.pack()
    indexLabel.place(x=780, y=470)

def nextVideo():
    global videoLabel
    videoLabel.pack_forget()
    newImageLabel.destroy()
    global videoIndex
    global searchVideos
    global videoPath
    videosNum = len(searchVideos) - 1
    if videoIndex < videosNum:
        videoIndex += 1
    elif videoIndex == videosNum:
        videoIndex = 0
    videoPath = searchVideos[videoIndex]
    videoLabel.config(text=videoPath)
    videoLabel.pack()
    videoLabel.place(x=685, y=130)
    indexLabel = tk.Label(win, text=str(videoIndex+1)+" of "+str(len(searchVideos))+" Results", bg="#0D379B", fg="white")
    indexLabel.pack()
    indexLabel.place(x=780, y=470)

def previousImage():
    openVideoButton.destroy()
    videoLabel.destroy()
    global newImageLabel
    global imageIndex
    global searchImages
    global imagePath
    imagesNum = len(searchImages) - 1
    if imageIndex == 0:
        imageIndex = imagesNum
    elif imageIndex <= imagesNum:
        imageIndex -= 1
    imagePath = searchImages[imageIndex]
    image = Image.open(searchImages[imageIndex])
    image = image.resize((250, 250), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    newImageLabel.config(image=image)
    newImageLabel.image = image
    newImageLabel.pack()
    newImageLabel.place(x=685, y=130)
    indexLabel = tk.Label(win, text=str(imageIndex+1) + " of " + str(len(searchImages)) + " Results", bg="#0D379B",
                          fg="white")
    indexLabel.pack()
    indexLabel.place(x=780, y=470)

def previousVideo():
    newImageLabel.destroy()
    global videoLabel
    videoLabel.pack_forget()
    global videoIndex
    global searchVideos
    global videoPath
    videosNum = len(searchVideos) - 1
    if videoIndex == 0:
        videoIndex = videosNum
    elif videoIndex <= videosNum:
        videoIndex -= 1
    videoPath = searchVideos[videoIndex]
    videoLabel.config(text=videoPath)
    videoLabel.pack()
    videoLabel.place(x=685, y=130)
    indexLabel = tk.Label(win, text=str(videoIndex+1)+" of "+str(len(searchVideos))+" Results", bg="#0D379B", fg="white")
    indexLabel.pack()
    indexLabel.place(x=780, y=470)

def addToClipBoard():
    global videoPath
    global imagePath
    if var_ImgVid.get() == 0:
        command = 'echo ' + imagePath.strip() + '| clip'
        os.system(command)
    else:
        command = 'echo ' + videoPath.strip() + '| clip'
        os.system(command)

def openVidExternally():
    cap = cv.VideoCapture(videoPath)
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
        cv.imshow(videoPath, gray)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

def primarySearch():
    global videoLabel
    global newImageLabel
    global openVideoButton
    if var_selectedFeature.get() == 0:
        tk.messagebox.showwarning(title="Warning", message="Please choose any feature to filter with.")
    else:
        if var_ImgVid.get() == 0:
            global searchImages
            searchImages.clear()
            global imageIndex
            imageIndex = 0
            global imagePath
            openVideoButton.destroy()
            videoLabel.destroy()
            #Todo: remove glob and initialize searchImages with similarities
            for img in glob.glob("C:/Users/Legion/Desktop/*.png"):
                searchImages.append(img)
            # to be changed with network image
            imagePath = searchImages[imageIndex]
            image = Image.open(searchImages[imageIndex])
            image = image.resize((250, 250), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            newImageLabel = tk.Label(image=image)
            newImageLabel.image = image
            newImageLabel.pack()
            newImageLabel.place(x=685, y=130)

            nextImageButton = tk.Button(win, text="Next Image ->", command=nextImage, width=15, activebackground="white",
                                        activeforeground="#0D379B")
            nextImageButton.pack()
            nextImageButton.place(x=860, y=425)
            prevImageButton = tk.Button(win, text="<- Previous Image", command=previousImage, width=15, activebackground="white",
                                        activeforeground="#0D379B")
            prevImageButton.pack()
            prevImageButton.place(x=740, y=425)
            copyPathButton = tk.Button(win, text="Copy Img Path", command=addToClipBoard, width=13, activebackground="white",
                                      activeforeground="#0D379B")
            copyPathButton.pack()
            copyPathButton.place(x=634, y=425)
            indexLabel = tk.Label(win, text=str(imageIndex+1)+" of "+str(len(searchImages))+" Results", bg="#0D379B", fg="white")
            indexLabel.pack()
            indexLabel.place(x=780, y=470)
            featureLabel.pack()
            featureLabel.place(x=730, y=510)
        else:
            newImageLabel.destroy()
            global videoPath
            global searchVideos
            searchVideos.clear()
            global videoIndex
            videoIndex = 0
            # Todo: remove glob and initialize searchVideos with similarities
            for vid in glob.glob("C:/Users/Legion/Desktop/*.mp4"):
                searchVideos.append(vid)
            # to be changed with network image
            videoPath = searchVideos[videoIndex]
            videoLabel = tk.Label(text=videoPath, bg="#0D379B", fg="white")
            videoLabel.pack()
            videoLabel.place(x=685, y=130)
            openVideoButton = tk.Button(text="Open Video Externally", command=openVidExternally, width=20,
                                      activebackground="white",
                                      activeforeground="#0D379B")
            openVideoButton.pack()
            openVideoButton.place(x=730, y=180)
            nextVidButton = tk.Button(win, text="Next Video ->", command=nextVideo, width=15,
                                        activebackground="white",
                                        activeforeground="#0D379B")
            nextVidButton.pack()
            nextVidButton.place(x=860, y=425)
            prevVidButton = tk.Button(win, text="<- Previous Video", command=previousVideo, width=15,
                                        activebackground="white",
                                        activeforeground="#0D379B")
            prevVidButton.pack()
            prevVidButton.place(x=740, y=425)
            copyPathButton = tk.Button(win, text="Copy Video Path", command=addToClipBoard, width=13,
                                       activebackground="white",
                                       activeforeground="#0D379B")
            copyPathButton.pack()
            copyPathButton.place(x=634, y=425)
            indexLabel = tk.Label(win, text=str(videoIndex+1) + " of " + str(len(searchVideos)) + " Results",
                                  bg="#0D379B", fg="white")
            indexLabel.pack()
            indexLabel.place(x=780, y=470)
            featureLabel.pack()
            featureLabel.place(x=730, y=510)

def search():
    primarySearch()
    updateFeatureLabel()

def updateFeatureLabel():
    featureLabel.pack_forget()
    featureLabel.config(text=featureDict.get(var_selectedFeature.get())+"0.55")


def selectFileType():
    if (var_ImgVid.get()) == 0:
        directoryLabel = tk.Label(win, text="Enter Image Path:", bg="#0D379B", fg="white")
        directoryLabel.pack()
        directoryLabel.place(bordermode=INSIDE, x=240, y=20)

        OpenFile = tk.Button(win, text="Open Image", command=openImage, width=10, activebackground="white",
                             activeforeground="#0D379B")
        OpenFile.pack()
        OpenFile.place(x=800, y=18)
    else:
        directoryLabel = tk.Label(win, text="Enter Video Path:", bg="#0D379B", fg="white")
        directoryLabel.pack()
        directoryLabel.place(bordermode=INSIDE, x=240, y=20)

        OpenFile = tk.Button(win, text="Open Video", command=openVid, width=10, activebackground="white",
                             activeforeground="#0D379B")
        OpenFile.pack()
        OpenFile.place(x=800, y=18)



def openImage():
    filename = filedialog.askopenfilename()
    if (len(Entry.get(fileEntryTextField))):
        fileEntryTextField.delete(0, END)
    fileEntryTextField.insert(END, filename)
    if fileEntryTextField.get():
        photo_label1 = tk.Label(win, text="Selected Photo", bg="#0D379B", fg="white")
        photo_label1.pack()
        photo_label1.place(bordermode=INSIDE, x=110, y=100)
        # Select the Imagename from a folder
        x = fileEntryTextField.get()

        # opens the image
        img = Image.open(x)

        # resize the image and apply a high-quality down sampling filter
        img = img.resize((250, 250), Image.ANTIALIAS)

        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)

        # create a label
        panel = Label(win, image=img)

        # set the image as img
        panel.image = img
        panel.pack()
        panel.place(x=30, y=130)
        features = get_image_features(x)
        show_search()
        show_features(features['avg_color'], features['dominate_color'])


def openVid():
    filename = filedialog.askopenfilename()
    if (len(Entry.get(fileEntryTextField))):
        fileEntryTextField.delete(0, END)
    fileEntryTextField.insert(END, filename)
    if fileEntryTextField.get():
        videoLabel = tk.Label(win, text="Selected Video", bg="#0D379B", fg="white")
        videoLabel.pack()
        videoLabel.place(bordermode=INSIDE, x=110, y=100)
        # Select the video from a folder
        vidPath = fileEntryTextField.get()

        vid = Label(win)
        vid.pack()
        vid.place(x=30, y=130)
        player = tkvideo(vidPath, vid, loop=1, size=(250, 250))
        player.play()
        #todo: replace x,y with list of the real rgb
        x = [0, 255, 0]
        y = [0, 0, 0]
        show_search()
        show_features(x, y)

def show_features(avg, dom):
    Average_color = rgbtohex(avg[0], avg[1], avg[2])
    average_label1 = tk.Label(win, text="Average Color", bg="#0D379B", fg="white")
    average_label1.pack()
    average_label1.place(x=47, y=400)
    average_label = tk.Label(win, text="", width=15, height=2, bg=Average_color, fg="#683838")
    average_label.pack()
    average_label.place(bordermode=INSIDE, x=30, y=430)

    Dominant_color = rgbtohex(dom[0], dom[1], dom[2])
    dominant_label1 = tk.Label(win, text="Dominant Color", bg="#0D379B", fg="white")
    dominant_label1.pack()
    dominant_label1.place(x=167, y=400)
    dominant_label = tk.Label(win, text="", width=15, height=2, bg=Dominant_color, fg="#683838")
    dominant_label.pack()
    dominant_label.place(bordermode=INSIDE, x=150, y=430)

    histogramLabel = tk.Label(win, text="Histogram", bg="#0D379B", fg="white")
    histogramLabel.pack()
    histogramLabel.place(x=115, y=475)
    f = Figure(figsize=(5, 4), dpi=40)
    canvas = FigureCanvasTkAgg(f, master=win)
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().place(x=45, y=507)
    p = f.gca()
    #todo: Add histogram values in the below x variable
    x = np.random.normal(256, 1, 5000)
    p.hist(x, 256)
    canvas.draw()


def rgbtohex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


def show_search():
    searchButton = tk.Button(win, text="Search", command=search, width=10, activebackground="white",
                             activeforeground="#0D379B")
    searchButton.pack()
    searchButton.place(x=450, y=120)
    filtrationLabel = tk.Label(win, text="Choose your preferred filtration feature :", bg="#0D379B", fg="white")
    filtrationLabel.pack()
    filtrationLabel.place(bordermode=INSIDE, x=10, y=65)
    avgColorRadioButton = Radiobutton(win, text="Average Color", selectcolor="#0D379B", highlightcolor="white",
                                      activebackground="#0D379B",
                                      bg="#0D379B", fg="white", variable=var_selectedFeature, value=1)
    avgColorRadioButton.pack()
    avgColorRadioButton.place(bordermode=OUTSIDE, x=250, y=65)


    dominantColorRadioButton = Radiobutton(win, text="Dominant Color", selectcolor="#0D379B", highlightcolor="white",
                                           activebackground="#0D379B",
                                           bg="#0D379B", fg="white", variable=var_selectedFeature, value=2)
    dominantColorRadioButton.pack()
    dominantColorRadioButton.place(bordermode=OUTSIDE, x=400, y=65)


    histogramRadioButton = Radiobutton(win, text="Histogram", selectcolor="#0D379B", highlightcolor="white",
                                       activebackground="#0D379B",
                                       bg="#0D379B", fg="white", variable=var_selectedFeature, value=3)
    histogramRadioButton.pack()
    histogramRadioButton.place(bordermode=OUTSIDE, x=525, y=65)

    objectDetectionRadioButton = Radiobutton(win, text="Object Detection", selectcolor="#0D379B",
                                             highlightcolor="white",
                                             activebackground="#0D379B",
                                             bg="#0D379B", fg="white", variable=var_selectedFeature, value=4)
    objectDetectionRadioButton.pack()
    objectDetectionRadioButton.place(bordermode=OUTSIDE, x=650, y=65)





# ----------------------------
# label in the LEFT
# ----------------------------

upperLeftTitle = tk.Label(win, text="Content Base Image/Video Retriever", width=28, height=2, bg="white", fg="#0D379B")
upperLeftTitle.pack()
upperLeftTitle.place(bordermode=INSIDE, x=0, y=10)

directoryLabel = tk.Label(win, text="Enter Image Path:", bg="#0D379B", fg="white")
directoryLabel.pack()
directoryLabel.place(bordermode=INSIDE, x=240, y=20)

fileEntryTextField = Entry(win, width=70, bg="white", fg="#0D379B")
fileEntryTextField.pack()
fileEntryTextField.place(bordermode=OUTSIDE, x=350, y=20)

OpenFile = tk.Button(win, text="Open Image", command=openImage, width=10, activebackground="white",
                     activeforeground="#0D379B")
OpenFile.pack()
OpenFile.place(x=800, y=18)

imageRadio = Radiobutton(win, text="Image Input", variable=var_ImgVid, value=0,
                  command=selectFileType)
imageRadio.pack()
imageRadio.place(x=900, y=10)


videoRadio = Radiobutton(win, text="Video Input", variable=var_ImgVid, value=1,
                  command=selectFileType)
videoRadio.pack()
videoRadio.place(x=900, y=50)




win.mainloop()

