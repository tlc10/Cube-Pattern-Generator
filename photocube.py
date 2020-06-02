from tkinter import *
from tkinter.filedialog import askopenfilename              #import des différents modules
from PIL import Image, ImageTk
import svgwrite
import subprocess

class Application(Frame):                                   #création d'une classe nommée Application

    def __init__(self, master=None):                        #création de la définition __init__ qui renferme les variables. On attribut à chaque variable une
        Frame.__init__(self, master)                        #méthode (self.)

        self.PATH = "C:\\Users\\Lenovo\\Documents\\Thomas\\Documents\\Photo cube projet isn\\"       #chemin d'accés vers le dossier renfermant le projet
        self.SVG_VIEWER_PATH = "C:\\Program Files\\Inkscape\\inkscape.exe"                           #chemin d'accés vers le logiciel Inkscape
        self.CANVAS_WIDTH_PIXELS = 500
        self.CANVAS_HEIGHT_PIXELS = 500
        self.CANVAS = Canvas(master,width=self.CANVAS_WIDTH_PIXELS,height=self.CANVAS_HEIGHT_PIXELS,bg="white")
        self.CANVAS.pack()
        self.IMAGES = []
        self.IMAGES_DISPLAY = []
        self.TKIMAGES = []
        self.MARGIN_H = []
        self.SIZE = []
        self.X = []
        self.Y = []
        self.CURRENT_INDEX = 0

        self.pack()
        self.createWidgets()

    def updateSquare(self):                             #création de la définition updatesquare qui permet de créer le square
        self.CANVAS.delete(ALL)
        self.CANVAS.create_image(self.CANVAS_WIDTH_PIXELS/2,self.CANVAS_HEIGHT_PIXELS/2,image=self.TKIMAGES[self.CURRENT_INDEX])
        xs = self.X[self.CURRENT_INDEX]
        ys = self.Y[self.CURRENT_INDEX] + self.MARGIN_H[self.CURRENT_INDEX]
        print(str(xs) + " "  + str(ys) + " " + str(self.SIZE[self.CURRENT_INDEX]))
        self.CANVAS.create_rectangle(xs,ys,xs+self.SIZE[self.CURRENT_INDEX],ys+self.SIZE[self.CURRENT_INDEX],outline='black',width=2)

    def updateCurrentIndex(self):                       #mise à jour du compteur du nombre de photos carrées extraites de l'image initiale 
        self.W_LABEL.destroy()
        self.W_LABEL = Label(self, text = str(self.CURRENT_INDEX))
        self.W_LABEL.pack()
        
        
        
    def openFile(self):                                 #ouverture d'une image choisie dans le canevas 
        name = askopenfilename(initialdir=self.PATH,
                               filetypes =(("All Files", "*.*"),("PNG Image File", "*.png"),("JPG Image Files","*.jpg")),
                               title = "Choose an image file." ) 
        print (name) 
 
        image = Image.open(name)
        image.load()
        print(image.format,image.size,image.mode)
        self.IMAGES.append(image)
        w = int(self.CANVAS_WIDTH_PIXELS)
        h = int(( w * image.size[1] ) / image.size[0])
        self.MARGIN_H.append(int((self.CANVAS_HEIGHT_PIXELS - h ) / 2))
        image_small = image.resize((w,h),Image.ANTIALIAS)
        print(image_small.format,image_small.size,image_small.mode)
        self.IMAGES_DISPLAY.append(image_small)

        max_size = min(image_small.size)
        self.SIZE.append(max_size/2)
        self.W_SIZE.destroy()
        self.W_SIZE = Scale(self,from_=20, to=max_size, orient=HORIZONTAL)
        self.W_SIZE.set(float(self.SIZE[self.CURRENT_INDEX]))
        self.W_SIZE["command"] = self.changeSize
        self.W_SIZE.pack()
        
        self.X.append(0)
        self.Y.append(0)
        
        tkimage = ImageTk.PhotoImage(image_small)
        self.TKIMAGES.append(tkimage)

        self.updateSquare()

        

    def changeSize(self,value):                                                                        #change la taille du square
        size_max_x = self.IMAGES_DISPLAY[self.CURRENT_INDEX].size[0] - self.X[self.CURRENT_INDEX]
        size_max_y = self.IMAGES_DISPLAY[self.CURRENT_INDEX].size[1] - self.Y[self.CURRENT_INDEX]
        size_max_min = size_max_x
        if (size_max_y <  size_max_min):
            size_max_min = size_max_y
        if (float(value) < size_max_min) :
            self.SIZE[self.CURRENT_INDEX] = float(value)
            self.updateSquare()
        else :
            self.W_SIZE.set(size_max_min)

    def changeX(self,value):                                                                           #change la position du square en X
        vmax = self.IMAGES_DISPLAY[self.CURRENT_INDEX].size[0] - self.SIZE[self.CURRENT_INDEX]
        if (float(value) < vmax):
            self.X[self.CURRENT_INDEX] = float(value)
            self.updateSquare()
        else :
            self.W_X.set(vmax)
            

    def changeY(self,value):                                                                           #change la position du square en Y
        vmax = self.IMAGES_DISPLAY[self.CURRENT_INDEX].size[1] - self.SIZE[self.CURRENT_INDEX]
        if ( (float(value) < vmax)):
            self.Y[self.CURRENT_INDEX] = float(value)
            self.updateSquare()
        else :
            self.W_Y.set(vmax)
            

    def nextImage(self):                                                                          #enregistre sous un fichier l'image extraite à partir du 
        s = float(self.IMAGES[self.CURRENT_INDEX].size[0]) / float(self.CANVAS_WIDTH_PIXELS)      #square
        left = int(self.X[self.CURRENT_INDEX] * s )
        top = int(( self.Y[self.CURRENT_INDEX] ) * s ) 
        right = int( ( self.X[self.CURRENT_INDEX] + self.SIZE[self.CURRENT_INDEX] ) * s )
        bottom = int( ( self.Y[self.CURRENT_INDEX] + self.SIZE[self.CURRENT_INDEX] ) * s )
        res = self.IMAGES[self.CURRENT_INDEX].crop((left,top,right,bottom))
        name = "out_" + "%02d" % self.CURRENT_INDEX + ".png"
        filename = self.PATH + name
        res.save(filename,"png")

        self.CURRENT_INDEX += 1
        self.updateCurrentIndex()

    def generateSVG(self):                                                             #generation du SVG dans Inkscape
        name = "cube.svg"
        filename = self.PATH + name
        svg_document = svgwrite.Drawing(filename = filename,size = ("297mm", "210mm"))
        c = 60                                                                      #c coté du square
        c_s = str(c)+"mm"
        x = 28.5
        y = 75
        
        svg_document.add(svg_document.image(href="out_00.png",
                                            insert=(str(x)+"mm",str(y)+"mm"),
                                            size = (c_s,c_s)))                                 #implantation des 6 images extraites dans le fichier SVG
        x += c
        svg_document.add(svg_document.image(href="out_01.png",
                                            insert=(str(x)+"mm",str(y)+"mm"),
                                            size = (c_s,c_s)))
        x += c
        svg_document.add(svg_document.image(href="out_02.png",
                                            insert=(str(x)+"mm",str(y)+"mm"),
                                            size = (c_s,c_s)))
        x += c
        svg_document.add(svg_document.image(href="out_03.png",
                                            insert=(str(x)+"mm",str(y)+"mm"),                        
                                            size = (c_s,c_s)))
        x = 28.5
        y = 75

        x += c
        y -= c
        
        svg_document.add(svg_document.image(href="out_04.png",
                                            insert=(str(x)+"mm",str(y)+"mm"),
                                            size = (c_s,c_s)))
        x = 28.5
        y = 75

        x += c
        y += c
        
        svg_document.add(svg_document.image(href="out_05.png",
                                            insert=(str(x)+"mm",str(y)+"mm"),
                                            size = (c_s,c_s)))

        #création des languettes dans le SVG
        
        svg_document.add(svg_document.line((str(28.5) + "mm", str(75) + "mm"), (str(18.5) + "mm", str(85) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(18.5) + "mm", str(85) + "mm"), (str(18.5) + "mm", str(125) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))
        
        svg_document.add(svg_document.line((str(18.5) + "mm", str(125) + "mm"), (str(28.5) + "mm", str(135) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(88.5) + "mm", str(15) + "mm"), (str(78.5) + "mm", str(25) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(78.5) + "mm", str(25) + "mm"), (str(78.5) + "mm", str(65) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(78.5) + "mm", str(65) + "mm"), (str(88.5) + "mm", str(75) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(88.5) + "mm", str(135) + "mm"), (str(78.5) + "mm", str(145) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(78.5) + "mm", str(145) + "mm"), (str(78.5) + "mm", str(185) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(78.5) + "mm", str(185) + "mm"), (str(88.5) + "mm", str(195) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(148.5) + "mm", str(75) + "mm"), (str(158.5) + "mm", str(65) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(158.5) + "mm", str(65) + "mm"), (str(198.5) + "mm", str(65) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(198.5) + "mm", str(65) + "mm"), (str(208.5) + "mm", str(75) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(208.5) + "mm", str(75) + "mm"), (str(218.5) + "mm", str(65) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(218.5) + "mm", str(65) + "mm"), (str(258.5) + "mm", str(65) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(258.5) + "mm", str(65) + "mm"), (str(268.5) + "mm", str(75) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(148.5) + "mm", str(135) + "mm"), (str(158.5) + "mm", str(145) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(158.5) + "mm", str(145) + "mm"), (str(198.5) + "mm", str(145) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(198.5) + "mm", str(145) + "mm"), (str(208.5) + "mm", str(135) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(208.5) + "mm", str(135) + "mm"), (str(218.5) + "mm", str(145) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(218.5) + "mm", str(145) + "mm"), (str(258.5) + "mm", str(145) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))

        svg_document.add(svg_document.line((str(258.5) + "mm", str(145) + "mm"), (str(268.5) + "mm", str(135) + "mm"), stroke=svgwrite.rgb(0, 0, 0, '%')))



        
        
        
        print(svg_document.tostring())
        svg_document.save()

        list = []                                             #ouverture directe du SVG dans Inkscape suite au clic sur le bouton GENERATE
        list.append(self.SVG_VIEWER_PATH)
        list.append(self.PATH + "cube.svg")
        print(list)
        subprocess.call(list)
        
    
    def createWidgets(self):                            #création des 7 boutons du Tkinter
        
        self.W_QUIT = Button(self)           #ferme le programme 
        self.W_QUIT["text"] = "QUIT"
        self.W_QUIT["fg"]   = "red"
        self.W_QUIT["command"] =  self.quit
        self.W_QUIT.pack({"side": "left"})

        self.W_OPENFILE = Button(self)        #ouvre l'image sélectionnée dans le canevas
        self.W_OPENFILE["text"] = "Open",
        self.W_OPENFILE["command"] = self.openFile
        self.W_OPENFILE.pack({"side": "left"})

        self.W_SIZE = Scale(self,from_=0, to=600, orient=HORIZONTAL)     #scale qui modifie la taille du square
        self.W_SIZE["command"] = self.changeSize
        self.W_SIZE.pack({"side": "left"})

        self.W_X = Scale(self,from_=0, to=600, orient=HORIZONTAL)        #scale qui modifie la position du square en X 
        self.W_X["command"] = self.changeX
        self.W_X.pack({"side": "left"})

        self.W_Y = Scale(self,from_=0, to=400, orient=VERTICAL)          #scale qui modifie la position du square en Y 
        self.W_Y["command"] = self.changeY
        self.W_Y.pack({"side": "left"})

        self.W_NEXT_IMAGE = Button(self)                       #permet de crowper l'image sélectionée avec le square (met à jour en même temps le compteur)
        self.W_NEXT_IMAGE["text"] = "NEXT IMAGE"
        self.W_NEXT_IMAGE["command"] = self.nextImage
        self.W_NEXT_IMAGE.pack({"side": "left"})

        self.W_GENERATE = Button(self)                        #génére le patron du cube dans Inkscape (format SVG) et l'ouvre directement
        self.W_GENERATE["text"] = "GENERATE"
        self.W_GENERATE["command"] = self.generateSVG
        self.W_GENERATE.pack({"side": "left"})

        self.W_LABEL = Label(self, text="0")      #compteur 
        self.W_LABEL.pack()

#MAINPROGRAM

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()




