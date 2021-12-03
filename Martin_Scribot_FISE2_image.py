from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

class Image:
    def __init__(self):
        """Initialisation d'une image composee d'un tableau numpy 2D vide
        (pixels) et de 2 dimensions (H = height et W = width) mises a 0
        """
        self.pixels = None
        self.H = 0
        self.W = 0


    def set_pixels(self, tab_pixels):
        """ Remplissage du tableau pixels de l'image self avec un tableau 2D (tab_pixels)
        et affectation des dimensions de l'image self avec les dimensions
        du tableau 2D (tab_pixels)
        """
        self.pixels = tab_pixels
        self.H, self.W = self.pixels.shape


    def load(self, file_name):
        """ Lecture d'un image a partir d'un fichier de nom "file_name"""
        self.pixels = io.imread(file_name)
        self.H,self.W = self.pixels.shape
        print("lecture image : " + file_name + " (" + str(self.H) + "x" + str(self.W) + ")")


    def display(self, window_name):
        """Affichage a l'ecran d'une image"""
        fig = plt.figure(window_name)
        if (not (self.pixels is None)):
            io.imshow(self.pixels)
            io.show()
        else:
            print("L'image est vide. Rien à afficher")


    #==============================================================================
    # Methode de binarisation
    # 2 parametres :
    #   self : l'image a binariser
    #   S : le seuil de binarisation
    #   on retourne une nouvelle image binarisee
    #==============================================================================
    def binarisation(self, S):
        im_bin = Image()
        im_bin.W=self.W
        im_bin.H=self.H

        im_bin.set_pixels(np.zeros((self.H, self.W), dtype=np.uint8))

        for i in range(im_bin.H):
            for j in range(im_bin.W):
                if self.pixels[i][j]>=S:
                    im_bin.pixels[i][j]=255
                elif self.pixels[i][j]<S:
                        im_bin.pixels[i][j]=0
        return im_bin
    #==============================================================================
    # Dans une image binaire contenant une forme noire sur un fond blanc
    # la methode 'localisation' permet de limiter l'image au rectangle englobant
    # la forme noire
    # 1 parametre :
    #   self : l'image binaire que l'on veut recadrer
    #   on retourne une nouvelle image recadree
    #==============================================================================      
    
    def localisation(self):
        im_loc = Image()
        Cmin = 30
        Cmax = 0
        lmin = 30
        lmax = 0
        for i in range(self.H):
            for j in range(self.W):
            
                if self.pixels[i][j] == 0 and self.pixels[i][j-1] == 255:
                    if Cmin > j:
                        Cmin = j
                
                if self.pixels[i][j] == 0 and self.pixels[i][j+1] == 255:
                    if Cmax < j:
                        Cmax = j
        
                if self.pixels[i][j] == 0 and self.pixels[i-1][j] == 255:
                    if lmin > i:
                        lmin = i
                
                if self.pixels[i][j] == 0 and self.pixels[i+1][j] == 255:
                    if lmax < i:
                        lmax = i
    
        im_loc.set_pixels(np.zeros((lmax-lmin, Cmax-Cmin), dtype=np.uint8))
        
        for i in range(lmin,lmax):
            for j in range(Cmin,Cmax):
                 im_loc.pixels[i-lmin][j-Cmin] = self.pixels[i][j]
                
        im_loc.H=lmax-lmin
        im_loc.W=Cmax-Cmin
        return im_loc
    
    
    #==============================================================================
    # Methode de redimensionnement d'image
    #==============================================================================
    def resize(self, new_H, new_W):
        im_resized = Image()
        im_resized.H=new_H
        im_resized.W=new_W
        pixels_resized = resize(self.pixels, (new_H,new_W), 0)
        im_resized.set_pixels( np.uint8(pixels_resized*255))
        return im_resized

    #==============================================================================
    # Methode de mesure de similitude entre l'image self et un modele im
    #==============================================================================
    def similitude(self, image):
        n=0
        for i in range(self.H):
            for j in range(self.W):
                if (self.pixels[i][j]==image.pixels[i][j]):
                    n+=1
        return (n/(self.H*self.W))