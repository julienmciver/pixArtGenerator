import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter.filedialog import FileDialog
#from resizeimage import resizeimage
import math
from PIL import Image, ImageOps
import webbrowser
import time
import os
import numpy as np
import PIL as pil
import shutil


colors = []
colors2 = []
imageData = []
imRows = 0
imCols = 0
finalAr = []
newIm = None
colorPallette = []
totalBlocks = []
loadingScreenSpecs = {
    "background-color" : "#ffffff",
    "bar-color" : "#cc33ff",
    "discreet" : True
}

def getPixels(im):
    width, height = im.size
    return width*height


def compareColors(r,g,b, cond, ret):
    # so the formula is d^2 = (r - colours[0][0]^2 etc.)
    global colors
    global colors2
               
    if ((r == g == b) and (r == None)):
        return None
        
    elif (cond):    
        shortestCol = 100000000000
        color = []
        
        for i in colors:
            d2 = (i[0] - r)**2 + (i[1] - g)**2 + (i[2] - b)**2
            
            if (d2 <= shortestCol):
                shortestCol = d2
               
                
                color = []
                
                
                color = i
            
        colors = colors2
        hexCode = ['#%02x%02x%02x' % (color[0], color[1], color[2]), color[3]]
        
        #gdArray.append(color[3])
        if (ret == "hex"): 
            return hexCode
        elif (ret == "rgb"):
        
            return [color[0], color[1], color[2], color[3]]
    else:
        return ['#%02x%02x%02x' % (r, g, b), None]





def findPallette(img, loadingScreen):
    #1) count the instances of each rgb value in the image
    global colors2
    global root
    global colorsEnt
    entry_number = int(colorsEnt.get())
    colors.clear()
    colorSums = []
    colorsFound = []
    color_ = {}
    width, height = img.size
    im = img.load()
    count = 0
    pix = getPixels(img)

    #calculate percentage: count/size
    size = width*height
    perc = 0
    chunks = 1

    for i in range (height):
        for c in range(width):
            pixel = tuple([im[c,i]])
            count += 1
            perc = count/size
            
            if not (pixel in color_):
                
                color_[pixel] = 1
            else:
                color_[pixel] += 1
            
            if (perc >= 0.05*chunks):
                chunks += 1
                updateLoadingScreen(loadingScreen, perc)
             
    order_of_vals = sorted(color_.items(), key=lambda x: x[1], reverse=True)
    totalLength = len(order_of_vals)
    for i in range(entry_number):
        #colors.append((order_of_vals[i][0][0],order_of_vals[i][0][1],order_of_vals[i][0][2]))
        colors.append([int(order_of_vals[i][0][0][0]),int(order_of_vals[i][0][0][1]), int(order_of_vals[i][0][0][2]),i])
    colors2 = colors
    print("Number of colors in original Image: " + str(len(order_of_vals)))
    return colors









def extractPallette():
    file = open("mosaic_colorPallette.txt", "r")
    list1 = file.read().splitlines()
    
    list2 = []
    for i, j in enumerate(list1):
        tempi = j.split("_")
        
        list2.append([int(tempi[0]), int(tempi[1]), int(tempi[2]), i])
    file.close()
    return list2



def updateLoadingScreen(screen, percentage):
    global loadingScreenSpecs
    global root
    width = screen.winfo_width()
    height = screen.winfo_height()
    rec_width = width*percentage
    if (percentage < 1):
        bar_color = loadingScreenSpecs["bar-color"]
    else:
            bar_color = "red"
        
    screen.delete("all")
    screen.create_rectangle(0,0,rec_width, height, fill = bar_color)
    
    root.update()
 

def newLoadEntry(window, text):
    global root
    bigFrame = Frame(window, pady = 8, bg = "black", padx = 8)
    bigFrame.pack(side = BOTTOM, anchor = S)
    lpLabel = Label(bigFrame, text = text, pady = 2, fg = "white", bg = "black").pack(side = TOP)
    screenFrame = Frame(bigFrame, width = 200, height = 20)
    screen1 = Canvas(screenFrame, bg = loadingScreenSpecs["background-color"], width = 200, height = 20)
    screen1.pack()
    screenFrame.pack(side = LEFT, anchor = W)
    root.update()
    return screen1


#okay: I need a thing that takes an image and a grid size, and resizes the image so that it fits in the grid
def snapToGrid(img, gridx, gridy):
    
    img_w, img_h = img.size    
    if  not (img_w < gridx or img_h < gridy):
        num = max(math.floor(img_w/gridx), math.floor(img_h/gridy))
        
        new_w = num*gridx
        new_h = num*gridy
        img.thumbnail((new_w, new_h), Image.ANTIALIAS)
        img_w, img_h = img.size
        background = Image.new('RGB', (new_w, new_h), (255, 255, 255,255)) #TODO : make this a setting you can do
        print("background1")
    else:
        background = Image.new('RGB', (gridx, gridy), (255, 255, 255,255)) #TODO : make this a setting you can do
        print("background2")
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset)
    
    return background

condi = False

def writeShoppingList(amounts, path):
    directory = "pallette Images"
    dir_ = os.listdir(directory)
    tot = 0
    file_ = open(path + "/shoppingList.txt", 'a')
    file_.truncate(0)
    rgb = extractPallette() #<------ I could make this more efficient
    tempInc = 1
    for i,j in enumerate(dir_):
        if not (amounts[i] == 0):
            tempString = j.split(".")
            file_.write(str(tempInc) + ": "  + tempString[0] + "}" + str(amounts[i]) + "#" +str(rgb[i][0]) + "," + str(rgb[i][1]) + "," + str(rgb[i][2]) + "_")
            tot+= amounts[i]
            tempInc +=1
            
        else:
            tempString = j.split(".")
            file_.write("$$$_")
            tot+= amounts[i]
    file_.write("Total:}" + str(tot))
    file_.close()


def upload():
    global imRows
    global condi
    global imCols
    global imageData
    global finalAr
    global newIm 
    global totalBlocks
    global colors
    global welcomeLabel
    global frame_info
    global colors
    global colors2
    global colsEnt
    global pixelateVar
    global radioVar
    global stgVar
    global stg_width
    global stg_height

    image_uploaded =  tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Image files","*.jpeg *.jpg"),("All files","*.*")))
    
    img = Image.open(image_uploaded)
        
    if (stgVar.get()):
        img = snapToGrid(img, int(stg_width.get()), int(stg_height.get()))
        
    pixAmountx, pixAmounty = img.size
            
    workingImg = img.load()
    pixAmount = getPixels(img)
    
    if not (pixelateVar.get()):
        if (stgVar.get()):
            cols = int(stg_width.get())
        else:
            cols = pixAmountx
    else:
        cols = int(colsEnt.get())
    if not (stgVar.get()):
        rows = math.ceil((cols*pixAmounty)/(pixAmountx))
    else:
        rows = int(stg_height.get())
   
    totalBlocks = [rows, cols, rows*cols]
 
    colorPallette.clear()
    colors.clear()
    
    #loading screen gets created here.
    
    #lp stands for loading pallette
    
    loadingWindow = tk.Toplevel(root)
    
    
    
    

    #TODO make a variable on the root that determines what to do here. for now, 
    if radioVar.get() == 2:
        screen1 = newLoadEntry(loadingWindow, "Finding Color Pallette:")
        colors = findPallette(img, screen1)
    elif radioVar.get() == 4:
        #extract the colors here.
        colors = extractPallette()
        colors2 = colors
    
    #okay, to account for different sized things, we need to modify pixpercolyx and y...
    #so we should be able to put a ratio in there, so that the columns and rows fit the ratio
    
    pixPerColx = math.ceil(pixAmountx/cols)
    pixPerColy = math.ceil(pixAmounty/rows)
    averagePix = []
    counter = 0
    
    newIm = pil.Image.new(mode = "RGB", size = (pixAmountx, pixAmounty))
    

    screen2 = newLoadEntry(loadingWindow, "Modifying image:")
    totWork = rows*cols*(pixPerColx**2)
    perc = 0
    percCount = 0
    chunks = 0
    pixCount = 0
    mosaicString = ""
    for i,c in enumerate(colors):
        mosaicString += str(c[0]) + "!" + str(c[1]) + "!" + str(c[2]) + "!" + str(c[3])
        if not (i == len(colors) - 1):
            mosaicString += ">"
    mosaicString += "_"
    colCount = []
    for k in colors:
        colCount.append(0)
   
    for i in range(rows):
        
        for x in range(cols):
            
            totalColor = [0,0,0]
            counter = 0
            for c in range(pixPerColy):
                for v in range(pixPerColx):
                    try:
                        
                        totalColor[2] += workingImg[v + (pixPerColx)*x,c + pixPerColy*i][2]
                        totalColor[1] += workingImg[v + (pixPerColx)*x,c + pixPerColy*i][1]
                        totalColor[0] += workingImg[v + (pixPerColx)*x,c + pixPerColy*i][0]
                        counter += 1
                    except:
                        pass
            try:
                averagePix.append([math.floor(totalColor[0]/counter),math.floor(totalColor[1]/counter),math.floor(totalColor[2]/counter)])
                
            except:
                averagePix.append([None, None, None])
            try:
                newPix = compareColors(math.floor(totalColor[0]/counter), math.floor(totalColor[1]/counter), math.floor(totalColor[2]/counter), True, "rgb")
                if not (orientVar.get()):
                    mosaicString += (str(i) + ":" + str(x) + "@" + str(newPix[3]))
                else:
                        mosaicString += (str(x) + ":" + str(i) + "@" + str(newPix[3]))
                
                if not(i == rows-1 and x == cols - 1):
                    mosaicString += "#"
                colCount[newPix[3]] += 1
                pixCount += 1
                if not (newPix in colorPallette):
               
                    colorPallette.append(newPix)
            except:
                newPix = [None, None, None]
            # fill in the pixel on a new Image
            for q in range(pixPerColx):
                for w in range(pixPerColy):
                    try:
                        if not (newPix[0] == None):
                            newIm.putpixel((w + (pixPerColx)*x, q + pixPerColy*i), (newPix[0], newPix[1], newPix[2]))
                    except:
                        pass
                    percCount += 1
                    perc = percCount/totWork
                    if (perc >= 0.01*chunks):
                        chunks+=1
                        updateLoadingScreen(screen2, perc)
                          

        #now to make a new grid where the welcome text was:
    
    #clean up averagePix
    
    imageDataCounter = 0
    
    s = True
    anotherS = True

    for i in averagePix:
        if not (i[0] == None):
            imageData.append(i)
            if (s):
                s = False
                imRows+=1
                
            
            
        else:
            s = True
    
    loadingWindow.destroy()
    newIm.show()
    demoWindow = tk.Toplevel(root)
    
    if not (condi):
        new_width  = 300
        new_height = int(new_width * pixAmounty / pixAmountx) 
        imgR = newIm
        imgR = imgR.resize((new_width,new_height))
        #converter = pil.ImageEnhance.Color(imgR)
        #imgR = converter.enhance(0.5)
        img = ImageTk.PhotoImage(imgR)
        
                

        gridContainer = Label(demoWindow, image=img)
        
        gridContainer.image =img # keep a reference!
        gridContainer.pack(side = LEFT, anchor = N, ipady = 15)
        
    
        
        wi, he = newIm.size
        #newSize = (wi-700,he-620)
        #img1 = img1.resize(newSize)
        #gridContainer.create_image(20, 20, anchor=NW, image=imgTk)
        print("Colors used: " + str(len(colorPallette)))
    #if radioVar.get() == 4:
     #   totsString = ""
      #  tempTot = 0
        
       # for i,j in enumerate(colCount):
        #    if not j == 0:
         #       totsString += str(i + 1) + ":\t" + str(j) + "\n"
                
          #  tempTot += j
        
        


        #totsString += "\nTotal:\t" + str(tempTot)
        #tots = Label(demoWindow, text = totsString,justify = "left").pack(side = LEFT, anchor = W)
    lbl = Label(demoWindow, text = "Name of Image:", padx = 5)
    
    saveVar_ = IntVar()
    Checkbutton(demoWindow, text="Save as mosaicProj", variable= saveVar_).pack(side = BOTTOM)
    e1 = tk.Entry(demoWindow, textvariable=user_input_name)
    
    lbl2 = Label(demoWindow, text = "Medium:", padx = 5)
    e2 = tk.Entry(demoWindow, textvariable=user_input_medium)
    
    save_button = Button(demoWindow, text = 'Save', command=lambda: save(saveVar_.get(), mosaicString, colCount), width = 15, pady = 0)
    save_button.pack(side = BOTTOM)
    e1.pack(side = BOTTOM)
    lbl.pack(side = BOTTOM)
    lbl2.pack(side = BOTTOM)
    e2.pack(side = BOTTOM)
    


    counter = 0
    hexCode = None
    imgTempAr = []
    if (condi):
        for i in range(rows):
            for x in range(cols):
                    
                hexCode = compareColors(averagePix[counter][0], averagePix[counter][1], averagePix[counter][2], True, "hex")[0]
                if (not hexCode == None):
                    gridContainer.create_rectangle(spaceBetween_items + x*gridItemSize + x*spaceBetween_items, spaceBetween_items + i*gridItemSize + i*spaceBetween_items, spaceBetween_items + x*gridItemSize + x*spaceBetween_items + gridItemSize, spaceBetween_items + i*gridItemSize + i*spaceBetween_items + gridItemSize, fill = hexCode, outline = hexCode)
                    imageDataCounter += 1
                    if (anotherS):
                        imCols += 1
                        
                counter += 1
            anotherS = False
            imgTempAr.clear()
            imRows = int(imageDataCounter/imCols)
            

            #now to save the imagedata into the right format
    else:
        pass
      # newIm.show()
       # print("save (y/n)?")
        #saveVar = input("Input: ")
        #if (saveVar == "y"):
         #   newIm.save("autogen_pixArt.png")
    mosaicString += "_" + str(pixCount) + "_"
    for i,j in enumerate(colCount):
        mosaicString += str(j)
        if not (i == len(colCount)-1):
            mosaicString += "$"
        
    
        
    
    
    
def draw():
    pass

def save(check, str_, amounts): 
    if not (check):
        tempString = "pixArt_Images/" + user_input_name.get() + "_pixArt.png"
    else:
        path = "./pixelArt_phone_component/Mosaic Projects/" + user_input_name.get()
        
        tempVar = True
        x = path
        
        
        while tempVar:
            
            try:
                os.mkdir(x)
                tempVar = False
            except:
                print("Replace the " + path.split("/")[-1] + " you already have saved [y/n]\n")
                x = input()
                if x == 'y':
                    shutil.rmtree("path_to_dir")
                else:
                    print("Enter new name for Project:\n")
                    x = input()
                    x = "./pixelArt_phone_component/Mosaic Projects/" + x
           

            
        
        tempString = path + "/image.png"
        mosaicFile = open(path + "/mosaicProj.txt", "w")
        print(user_input_medium.get())
        tempVar1 = user_input_medium.get()
        
        str_ += ("_" + str(orientVar.get()) + "_" + str(user_input_medium.get())    )
        mosaicFile.write(str_)
        mosaicFile.close()
        posFile = open(path+ "/pos.txt",'w')
        posFile.write("0")
        posFile.close()
        writeShoppingList(amounts, path)
    
    newIm.save(tempString)



        
    
     
   
    

#variables - unplaced

root = tk.Tk()
user_input_name = tk.StringVar(root)
user_input_medium = tk.StringVar(root)
root.title("Pixel Art Generator")
radioVar = IntVar()
radioVar.set(1)
gridItemSize = 1
spaceBetween_items = 0
gdArray = []

#okay, rebuilding this thing
img1 = Image.open("pixArt_Images/superman_pixelArt.jpg")
wi, he = img1.size
img = ImageTk.PhotoImage(img1)
img_frame = Frame(root)
img_frame.pack(side = TOP)
panel = Label(img_frame, image = img).pack(side = TOP, anchor = N)

frame_left = Frame(root)
frame_left.pack(anchor = W)


#newSize = (wi-700,he-620)
#img1 = img1.resize(newSize)



frame_btns = Frame(frame_left, height = 10, width = 10, padx = 10, pady = 10)
frame_btns.pack(side = BOTTOM,anchor = S)

frame_info = Frame(root, bg = 'white', borderwidth = 1,  width = 50*(gridItemSize + spaceBetween_items), height =50*(gridItemSize + spaceBetween_items))
frame_info.pack(side = TOP)

welcomeFile = open("welcome.txt")
welcomeText = welcomeFile.read()

welcomeLabel = Label(frame_info, text = welcomeText, padx = 20, pady = 20, justify = LEFT)
welcomeLabel.pack(side = LEFT)

radioFrame = Frame(frame_left)


# Dictionary to create multiple buttons 
values = {"Pre-Selected Color Pallette" : 1, 
          "Image color Pallette" : 2, 
          "image Color Pallette with clustering" : 3, 
          "Mosaic Color Pallette" : 4, 
          "Random Color Pallette" : 5} 
  
for (text, value) in values.items(): 
    if (values == 1):
        Radiobutton(radioFrame, text = text, variable = radioVar, 
        value = value).pack(side = TOP, anchor = W, ipady = 3) 
    else:
        Radiobutton(radioFrame, text = text, variable = radioVar, 
        value = value).pack(side = TOP, anchor = W, ipady = 3) 
radioFrame.pack(side = TOP)


reduceFrame = Frame(frame_btns)
reduceFrame.pack(side = LEFT)
colorsLbl = Label(reduceFrame, text = "# of colors")
colorsLbl.pack(ipady = 4)
colorsEnt = Entry(reduceFrame)
colorsEnt.pack()

pixelateFrame = Frame(frame_btns)
pixelateFrame.pack(side = RIGHT, ipadx = 5)
pixelateVar = IntVar()
Checkbutton(pixelateFrame, text="Pixelate", variable=pixelateVar).pack(side = TOP, anchor = W)
colsEnt = Entry(pixelateFrame)
colsEnt.pack(side = TOP, anchor = W)

stgVar = IntVar()
snapToGirdFrame = Frame(frame_left, pady = 10)
stg_checkBox = Checkbutton(snapToGirdFrame, text = "Snap to Grid", variable = stgVar).pack(side = TOP, anchor = N)

#orientation
orientVar = IntVar()
orientFrame = Frame(frame_left, padx = 20, pady = 10)
orientRad1 = Radiobutton(orientFrame, text = "Rows", value = 0, variable = orientVar).pack(side = LEFT)
orientRad2 = Radiobutton(orientFrame, text = "Columns", value = 1, variable = orientVar).pack(side = LEFT)
orientFrame.pack()
stg_width = Entry(snapToGirdFrame, width = 5, text = "huh")
stg_width.pack(side = LEFT, anchor = W)
stg_height = Entry(snapToGirdFrame, width = 5)
stg_height.pack(side = RIGHT, anchor = E)
snapToGirdFrame.pack(side = BOTTOM, anchor = S)
upload_btn = Button(root, text = 'Upload image', command = upload, width = 15)
upload_btn.pack(side = BOTTOM, anchor = S)


root.mainloop()
