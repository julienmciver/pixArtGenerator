import os
import PIL as pil
from PIL import Image

directory = "pallette Images"
dir_ = os.listdir(directory)


#takes a string, opens the associated file and returns it
def openFile(file):
    im = Image.open(directory + "/" + file)
    return im

#takes a file, returns average color of pixels

def averageColor(file):
    pixMap = file.load()
    width, height = file.size
    pixAmount = width*height
    totalRGB = [0,0,0]
    for i in range(height):
        for c in range(width):
            totalRGB[0] += tuple(pixMap[c,i])[0]
            totalRGB[1] += tuple(pixMap[c,i])[1]
            totalRGB[2] += tuple(pixMap[c,i])[2]
    totalRGB = [int(totalRGB[0]/pixAmount),int(totalRGB[1]/pixAmount),int(totalRGB[2]/pixAmount)]
    print(totalRGB)
    return totalRGB

#takes a tuple and saves it in a file.
def saveTuple(tuple_, file):
    file.write(str(tuple_[0]) + "_" + str(tuple_[1]) + "_" + str(tuple_[2]) + "\n")

#okay, now to open a file
file = open("mosaic_colorPallette.txt", "a")
file.truncate(0)

for i in dir_:
    im = openFile(i)
    avg_col = averageColor(im)
    saveTuple(avg_col, file)
file.close()
