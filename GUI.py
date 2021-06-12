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
from features_calculater import *
import os

featureDict = {0: "", 1: "Average Color Similarity : ", 2: "Dominant Color Similarity : ", 3: "Histogram Similarity : ", 4: "Object Detection Similarity : "}
searchDict = {1: "average_color", 2: "dominant_color", 3: "histogram", 4: "common_objects"}

win = tk.Tk()
# win.iconbitmap("parser_icon.ico")
win.title("Content Based Image/Video Retriever")
win.configure(background='#0D379B')
win.geometry("1000x700")
win.resizable(False, False)


# ----------------------------
# Global vars:
# ----------------------------

var_selectedFeature = IntVar()
var_ImgVid = IntVar()
searchImages = []
searchVideos = []
imageIndex = 0
videoIndex = 0
imagePath = ""
videoPath = ""
image_features = {}
video_features = {}
images_search_result = []
videos_search_result = []
video_similarity = 0
image_similarity = 0
search_flag = False


# ----------------------------
# Functions:
# ----------------------------


def nextImage():
    openVideoButton.pack_forget()
    videoLabel.pack_forget()
    global imageIndex
    global imagePath
    imagesNum = len(searchImages) - 1
    if imageIndex < imagesNum:
        imageIndex += 1
    elif imageIndex == imagesNum:
        imageIndex = 0
    imagePath = searchImages[imageIndex]
    updateSimilarityLabel()
    image = Image.open(searchImages[imageIndex])
    image = image.resize((250, 250), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    searchImagesViewer.config(image=image)
    searchImagesViewer.image = image
    searchImagesViewer.pack()
    searchImagesViewer.place(x=685, y=130)
    imageIndexLabel.config(text=str(imageIndex + 1) + " of " + str(len(searchImages)) + " Results")
    imageIndexLabel.pack()
    imageIndexLabel.place(x=780, y=470)


def nextVideo():
    global video_similarity
    global videoIndex
    global videoPath
    videosNum = len(searchVideos) - 1
    if videoIndex < videosNum:
        videoIndex += 1
    elif videoIndex == videosNum:
        videoIndex = 0
    videoPath = searchVideos[videoIndex]
    updateSimilarityLabel()
    videoLabel.config(text=videoPath)
    videoLabel.pack()
    videoLabel.place(x=685, y=130)

    videoIndexLabel.config(text=str(videoIndex + 1) + " of " + str(len(searchVideos)) + " Results")
    videoIndexLabel.pack()
    videoIndexLabel.place(x=780, y=470)

    videoSimilarityLabel.pack()
    videoSimilarityLabel.place(x=730, y=510)

def previousImage():
    openVideoButton.pack_forget()
    videoLabel.pack_forget()
    global searchImagesViewer
    global imageIndex
    global searchImages
    global imagePath
    imagesNum = len(searchImages) - 1
    if imageIndex == 0:
        imageIndex = imagesNum
    elif imageIndex <= imagesNum:
        imageIndex -= 1
    imagePath = searchImages[imageIndex]
    updateSimilarityLabel()
    image = Image.open(searchImages[imageIndex])
    image = image.resize((250, 250), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)

    searchImagesViewer.config(image=image)
    searchImagesViewer.image = image
    searchImagesViewer.pack()
    searchImagesViewer.place(x=685, y=130)

    imageIndexLabel.config(text=str(imageIndex + 1) + " of " + str(len(searchImages)) + " Results")
    imageIndexLabel.pack()
    imageIndexLabel.place(x=780, y=470)


def previousVideo():
    searchImagesViewer.pack_forget()
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
    updateSimilarityLabel()

    videoLabel.config(text=videoPath)
    videoLabel.pack()
    videoLabel.place(x=685, y=130)

    videoIndexLabel.config(text=str(videoIndex + 1) + " of " + str(len(searchVideos)) + " Results")
    videoIndexLabel.pack()
    videoIndexLabel.place(x=780, y=470)
    videoSimilarityLabel.pack()
    videoSimilarityLabel.place(x=730, y=510)


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

def features_sort():
    global images_search_result
    global searchImages
    global imagePath
    global imageIndex
    global search_flag

    global videos_search_result
    if search_flag:
        if var_ImgVid.get() == 0:
            imageIndex = 0
            searchImages.clear()

            # openVideoButton.place_forget()
            # nextVidButton.place_forget()
            # prevVidButton.place_forget()
            # copyVideoPathButton.place_forget()
            # videoIndexLabel.place_forget()
            # videoLabel.place_forget()
            # videoSimilarityLabel.place_forget()
            # key_frames.place_forget()

            images_search_result = sort_by(images_search_result, searchDict.get(var_selectedFeature.get()))
            for record in images_search_result:
                path = record.get("path")
                searchImages.append(path)
            imagePath = searchImages[imageIndex]
            image = Image.open(searchImages[imageIndex])
            image = image.resize((250, 250), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            searchImagesViewer.config(image=image)
            searchImagesViewer.image = image
            searchImagesViewer.pack()
            searchImagesViewer.place(x=685, y=130)

            nextImageButton.pack()
            nextImageButton.place(x=860, y=425)

            prevImageButton.pack()
            prevImageButton.place(x=740, y=425)

            copyPathButton.pack()
            copyPathButton.place(x=634, y=425)

            imageIndexLabel.config(text=str(imageIndex + 1) + " of " + str(len(searchImages)) + " Results")
            imageIndexLabel.pack()
            imageIndexLabel.place(x=780, y=470)
            similarityLabel.pack()
            similarityLabel.place(x=730, y=510)

            updateSimilarityLabel()
        else:
            global videoIndex
            global searchVideos
            global videoPath
            videoIndex = 0
            searchVideos.clear()
            # searchImagesViewer.place_forget()
            # nextImageButton.place_forget()
            # prevImageButton.place_forget()
            # copyPathButton.place_forget()
            # imageIndexLabel.place_forget()
            # similarityLabel.place_forget()
            videos_search_result = search_by_video_features(video_features, get_saved_videos_features(),
                                                            searchDict.get(var_selectedFeature.get()))
            for record in videos_search_result:
                path = record.get("path")
                searchVideos.append(path)

            # to be changed with network image
            videoPath = searchVideos[videoIndex]

            videoLabel.config(text=videoPath)
            videoLabel.pack()
            videoLabel.place(x=685, y=130)

            openVideoButton.pack()
            openVideoButton.place(x=730, y=180)

            nextVidButton.pack()
            nextVidButton.place(x=860, y=425)

            prevVidButton.pack()
            prevVidButton.place(x=740, y=425)

            copyVideoPathButton.pack()
            copyVideoPathButton.place(x=634, y=425)

            videoIndexLabel.config(text=str(videoIndex + 1) + " of " + str(len(searchVideos)) + " Results")
            videoIndexLabel.pack()
            videoIndexLabel.place(x=780, y=470)

            updateSimilarityLabel()
            videoSimilarityLabel.pack()
            videoSimilarityLabel.place(x=730, y=510)

def primarySearch():
    global videoLabel
    global searchImagesViewer
    global openVideoButton
    global images_search_result
    global videos_search_result
    global search_flag
    if var_selectedFeature.get() == 0:
        tk.messagebox.showwarning(title="Warning", message="Please choose any feature to filter with.")
    else:
        if var_ImgVid.get() == 0:
            search_flag = True
            global searchImages
            searchImages.clear()
            global imageIndex
            imageIndex = 0
            global imagePath

            # elmoshkla hna dol msh by5tfo
            openVideoButton.place_forget()
            nextVidButton.place_forget()
            prevVidButton.place_forget()
            copyVideoPathButton.place_forget()
            videoIndexLabel.place_forget()
            videoLabel.place_forget()
            videoSimilarityLabel.place_forget()

            imagePath = fileEntryTextField.get()
            images_search_result = search_by_image(imagePath)
            images_search_result = sort_by(images_search_result, searchDict.get(var_selectedFeature.get()))

            for record in images_search_result:
                path = record.get("path")
                searchImages.append(path)

            imagePath = searchImages[imageIndex]

            image = Image.open(searchImages[imageIndex])
            image = image.resize((250, 250), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)

            searchImagesViewer.config(image=image)
            searchImagesViewer.image = image
            searchImagesViewer.pack()
            searchImagesViewer.place(x=685, y=130)

            nextImageButton.pack()
            nextImageButton.place(x=860, y=425)

            prevImageButton.pack()
            prevImageButton.place(x=740, y=425)

            copyPathButton.pack()
            copyPathButton.place(x=634, y=425)

            imageIndexLabel.config(text=str(imageIndex + 1) + " of " + str(len(searchImages)) + " Results")
            imageIndexLabel.pack()
            imageIndexLabel.place(x=780, y=470)

            updateSimilarityLabel()
            similarityLabel.pack()
            similarityLabel.place(x=730, y=510)
        else:
            global videoPath
            global searchVideos
            global videoIndex
            videoIndex = 0
            searchVideos.clear()

            # elmoshkla hna dol msh by5tfo

            searchImagesViewer.place_forget()
            nextImageButton.place_forget()
            prevImageButton.place_forget()
            copyPathButton.place_forget()
            imageIndexLabel.place_forget()
            similarityLabel.place_forget()
            videos_search_result = search_by_video_features(video_features, get_saved_videos_features(),
                                                            searchDict.get(var_selectedFeature.get()))
            for record in videos_search_result:
                path = record.get("path")
                searchVideos.append(path)

            # to be changed with network image
            videoPath = searchVideos[videoIndex]

            videoLabel.config(text=videoPath)
            videoLabel.pack()
            videoLabel.place(x=685, y=130)

            openVideoButton.pack()
            openVideoButton.place(x=730, y=180)

            nextVidButton.pack()
            nextVidButton.place(x=860, y=425)

            prevVidButton.pack()
            prevVidButton.place(x=740, y=425)

            copyVideoPathButton.pack()
            copyVideoPathButton.place(x=634, y=425)

            videoIndexLabel.config(text=str(videoIndex + 1) + " of " + str(len(searchVideos)) + " Results")
            videoIndexLabel.pack()
            videoIndexLabel.place(x=780, y=470)


            updateSimilarityLabel()
            videoSimilarityLabel.pack()
            videoSimilarityLabel.place(x=730, y=510)


def search():
    primarySearch()
    # if var_selectedFeature.get() != 0:
    #     updateSimilarityLabel()


def updateSimilarityLabel():
    global video_similarity
    global image_similarity
    global images_search_result
    if var_ImgVid.get() == 0:
        feature = searchDict.get(var_selectedFeature.get())
        image_similarity = images_search_result[imageIndex].get(feature)
        similarityLabel.config(text=featureDict.get(var_selectedFeature.get()) + str(image_similarity))
    else:
        video_similarity = videos_search_result[videoIndex].get('similarity')
        videoSimilarityLabel.config(text=featureDict.get(var_selectedFeature.get()) + str(video_similarity))


def selectFileType():

    if (var_ImgVid.get()) == 0:

        directoryLabel.config(text="Enter Image Path")
        directoryLabel.pack()
        directoryLabel.place(bordermode=INSIDE, x=240, y=20)

        OpenFile.config(text="Open Image", command=openImage)
        OpenFile.pack()
        OpenFile.place(x=800, y=18)
    else:
        directoryLabel.config(text="Enter Video Path")
        directoryLabel.pack()
        directoryLabel.place(bordermode=INSIDE, x=240, y=20)

        OpenFile.config(text="Open Video", command=openVid)
        OpenFile.pack()
        OpenFile.place(x=800, y=18)


def openImage():
    global search_flag
    search_flag = False
    global image_features
    global imagePath
    filename = filedialog.askopenfilename()
    if (len(Entry.get(fileEntryTextField))):
        fileEntryTextField.delete(0, END)
    fileEntryTextField.insert(END, filename)
    if fileEntryTextField.get():
        photo_label1.pack()
        photo_label1.place(bordermode=INSIDE, x=110, y=100)
        # Select the Imagename from a folder

        key_frames.place_forget()


        imagePath = fileEntryTextField.get()
        # opens the image
        img = Image.open(imagePath)
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
        image_features = get_image_features(imagePath)
        print(image_features)
        show_search()
        show_features(image_features['avg_color'], image_features['dominant_color'])


def openVid():
    global search_flag
    search_flag = False
    global video_features
    global videoPath
    filename = filedialog.askopenfilename()
    if (len(Entry.get(fileEntryTextField))):
        fileEntryTextField.delete(0, END)
    fileEntryTextField.insert(END, filename)
    if fileEntryTextField.get():
        video_label1.pack()
        video_label1.place(bordermode=INSIDE, x=110, y=100)

        videoPath = fileEntryTextField.get()
        vid = Label(win)
        vid.pack()
        vid.place(x=30, y=130)
        player = tkvideo(videoPath, vid, loop=1, size=(250, 250))
        player.play()
        average_rectangle.place_forget()
        average_rectangle_label.place_forget()
        dominant_rectangle.place_forget()
        dominant_rectangle_label.place_forget()
        video_features = calculate_video_features(videoPath)
        # video_features = get_saved_videos_features()[0]
        x = [0, 255, 0]
        y = [0, 0, 0]
        show_search()
        show_features(x, y)


def show_features(avg, dom):
    if var_ImgVid.get() == 0:
        Average_color = rgb_to_hex(avg[0], avg[1], avg[2])

        average_rectangle_label.pack()
        average_rectangle_label.place(x=47, y=400)

        average_rectangle.config(bg=Average_color)
        average_rectangle.pack()
        average_rectangle.place(bordermode=INSIDE, x=30, y=430)

        Dominant_color = rgb_to_hex(dom[0], dom[1], dom[2])

        dominant_rectangle_label.pack()
        dominant_rectangle_label.place(x=167, y=400)

        dominant_rectangle.config(bg=Dominant_color)
        dominant_rectangle.pack()
        dominant_rectangle.place(bordermode=INSIDE, x=150, y=430)
    else:
        var = len(video_features.get('frames'))
        key_frames.config(text="Key frames number is " + str(var))
        key_frames.pack()
        key_frames.place(x=90, y=475)
    # histogramLabel = tk.Label(win, text="Histogram", bg="#0D379B", fg="white")
    # histogramLabel.pack()
    # histogramLabel.place(x=115, y=475)
    # f = Figure(figsize=(5, 4), dpi=40)
    # canvas = FigureCanvasTkAgg(f, master=win)
    # canvas.get_tk_widget().pack()
    # canvas.get_tk_widget().place(x=45, y=507)
    # p = f.gca()
    # hist = np.array(histogram, dtype=np.float32).flatten()
    # p.hist(hist, 3000)
    # canvas.draw()


def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


def show_search():
    searchButton.pack()
    searchButton.place(x=450, y=120)

    filtrationLabel.pack()
    filtrationLabel.place(bordermode=INSIDE, x=10, y=65)

    avgColorRadioButton.pack()
    avgColorRadioButton.place(bordermode=OUTSIDE, x=250, y=65)

    dominantColorRadioButton.pack()
    dominantColorRadioButton.place(bordermode=OUTSIDE, x=400, y=65)

    histogramRadioButton.pack()
    histogramRadioButton.place(bordermode=OUTSIDE, x=525, y=65)

    objectDetectionRadioButton.pack()
    objectDetectionRadioButton.place(bordermode=OUTSIDE, x=650, y=65)


# ----------------------------
# Layout Elements:
# ----------------------------
#video
videoLabel = tk.Label(win, text=videoPath, bg="#0D379B", fg="white")

openVideoButton = tk.Button(text="Open Video Externally", command=openVidExternally, width=20,
                            activebackground="white",
                            activeforeground="#0D379B")
nextVidButton = tk.Button(win, text="Next Video ->", command=nextVideo, width=15,
                          activebackground="white",
                          activeforeground="#0D379B")
prevVidButton = tk.Button(win, text="<- Previous Video", command=previousVideo, width=15,
                          activebackground="white",
                          activeforeground="#0D379B")
copyVideoPathButton = tk.Button(win, text="Copy Video Path", command=addToClipBoard, width=13,
                           activebackground="white",
                           activeforeground="#0D379B")
key_frames = tk.Label(win, text="", bg="#0D379B", fg="white")
videoIndexLabel = tk.Label(win, text="",
                           bg="#0D379B", fg="white")
video_label1 = tk.Label(win, text="Selected Video", bg="#0D379B", fg="white")
videoSimilarityLabel = tk.Label(win, text="",
                           bg="#0D379B", fg="white")

#img
similarityLabel = tk.Label(win, text="",
                           bg="#0D379B", fg="white")
searchImagesViewer = tk.Label(win, image=[])
imageIndexLabel = tk.Label(win, text="", bg="#0D379B", fg="white")
nextImageButton = tk.Button(win, text="Next Image ->", command=nextImage, width=15, activebackground="white",
                            activeforeground="#0D379B")
prevImageButton = tk.Button(win, text="<- Previous Image", command=previousImage, width=15, activebackground="white",
                            activeforeground="#0D379B")
copyPathButton = tk.Button(win, text="Copy Img Path", command=addToClipBoard, width=13, activebackground="white",
                           activeforeground="#0D379B")
photo_label1 = tk.Label(win, text="Selected Image", bg="#0D379B", fg="white")
average_rectangle_label = tk.Label(win, text="Average Color", bg="#0D379B", fg="white")
average_rectangle = tk.Label(win, width=15, height=2, bg='white', fg="#683838")
dominant_rectangle_label = tk.Label(win, text="Dominant Color", bg="#0D379B", fg="white")
dominant_rectangle = tk.Label(win, width=15, height=2, bg='white', fg="#683838")

#non img/video

fileEntryTextField = Entry(win, width=70, bg="white", fg="#0D379B")
fileEntryTextField.pack()
fileEntryTextField.place(bordermode=OUTSIDE, x=350, y=20)


directoryLabel = tk.Label(win, text="Enter Image Path:", bg="#0D379B", fg="white")
directoryLabel.pack()
directoryLabel.place(bordermode=INSIDE, x=240, y=20)

upperLeftTitle = tk.Label(win, text="Content Base Image/Video Retriever", width=28, height=2, bg="white", fg="#0D379B")
upperLeftTitle.pack()
upperLeftTitle.place(bordermode=INSIDE, x=0, y=10)
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

searchButton = tk.Button(win, text="Search", command=search, width=10, activebackground="white",
                         activeforeground="#0D379B")
filtrationLabel = tk.Label(win, text="Choose your preferred filtration feature :", bg="#0D379B", fg="white")
avgColorRadioButton = Radiobutton(win, text="Average Color", selectcolor="#0D379B", highlightcolor="white",
                                  activebackground="#0D379B",
                                  bg="#0D379B", fg="white", variable=var_selectedFeature, value=1, command=features_sort)
dominantColorRadioButton = Radiobutton(win, text="Dominant Color", selectcolor="#0D379B", highlightcolor="white",
                                       activebackground="#0D379B",
                                       bg="#0D379B", fg="white", variable=var_selectedFeature, value=2, command=features_sort)
histogramRadioButton = Radiobutton(win, text="Histogram", selectcolor="#0D379B", highlightcolor="white",
                                   activebackground="#0D379B",
                                   bg="#0D379B", fg="white", variable=var_selectedFeature, value=3, command=features_sort)

objectDetectionRadioButton = Radiobutton(win, text="Object Detection", selectcolor="#0D379B",
                                         highlightcolor="white",
                                         activebackground="#0D379B",
                                         bg="#0D379B", fg="white", variable=var_selectedFeature, value=4, command=features_sort)


win.mainloop()

