from PIL import Image, ImageTk
import tkinter
from tkinter import filedialog
import pygame

#On récupère un fichier dans le navigateur de dossiers
def get_file():
    global confirm_button, cancel_button, openFile_button, img, tkimg, canvas, file_path
    try:
        #On n'affiche plus le bouton pour ouvrir une image
        openFile_button.pack_forget()
        
        #On récupère l'image
        file_path = filedialog.askopenfilename(initialdir="assets/graphics/group_blocs")
        img = Image.open(file_path)
        surface = pygame.image.load(file_path)
        
        #On définie la taille de l'image en fonction d'une taille maximale
        max_size = 600
        if surface.get_size()[0] >= surface.get_size()[1]:
            new_width = max_size
            new_height = int(surface.get_size()[1]/surface.get_size()[0]*max_size)
        else:
            new_height = max_size
            new_width = int(surface.get_size()[0]/surface.get_size()[1]*max_size)
        
        #On agrandie l'image et on la convertie en image tkinter
        surface = pygame.transform.scale(surface, (new_width, new_height))
        raw_str = pygame.image.tostring(surface, 'RGBA', False)
        shown_img = Image.frombytes('RGBA', surface.get_size(), raw_str)
        tkimg = ImageTk.PhotoImage(shown_img)

        #On affiche l'image
        canvas.config(width=shown_img.size[0], height=shown_img.size[1])
        canvas.create_image(0,0, anchor=tkinter.NW, image = tkimg)
        
        #On affiche les boutons de confirmation et d'annulation
        confirm_button.pack()
        cancel_button.pack()
    except:
        #S'il y a une erreur, on redemande l'image
        return get_file()

#On segmente l'image en petite image de 16x16 px
def split_img():
    global img, file_path
    long, haut = img.size
    long16, haut16 = long//16, haut//16
    name = file_path.split('/')[-1][:-4]
    
    #Pour chaque carré de 16x16 px, on crée une petite image
    for i in range(long16):
        for j in range(haut16):
            area=img.crop((i*16, j*16, (i+1)*16, (j+1)*16)).copy()
            area.save(f"assets/graphics/blocs/{name}_{i}-{haut16-1-j}_{long16-1}-{haut16-1}.png")
            
    #On réinitialise la fenêtre
    img = None
    file_path = ""
    cancel()

def cancel():
    global confirm_button, cancel_button, openFile_button, canvas, img, file_path
    #On affiche plus l'image et les boutons de confirmation et d'annulation
    confirm_button.pack_forget()
    cancel_button.pack_forget()
    canvas.config(width=0, height=0)
    openFile_button.pack()
    img = None
    file_path = ""

#On crée la fenêtre
root = tkinter.Tk()
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

#On récupère l'icone de la fenêtre
ico = Image.open('assets/graphics/icons/split_img.ico')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

#On définie le titre de la fenêtre
root.title("Séparateur d'image")

#On crée le boton pour ouvrir une image
openFile_button = tkinter.Button(root, text="Ouvrir un fichier", command=get_file)
openFile_button.pack()

#On crée un canva dans lequel on va afficher l'image
canvas = tkinter.Canvas(root, width=0, height=0)
canvas.pack()

#On crée un bouton de confirmation pour segmenter l'image choisie en petits blocs de 16x16 px
confirm_button = tkinter.Button(root, text="Segmenter l'image", command=split_img)

#On crée un bouton pour annuler la segmentation de l'image en petits blocs de 16x16 px
cancel_button = tkinter.Button(root, text="Annuler", command=cancel)

root.mainloop()