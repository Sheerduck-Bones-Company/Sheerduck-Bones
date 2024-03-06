from PIL import Image, ImageTk
import tkinter
from tkinter import filedialog
import pygame

def get_file():
    global confirm_button, cancel_button, openFile_button, img, tkimg, canvas, file_path
    try:
        openFile_button.pack_forget()
        
        file_path = filedialog.askopenfilename(initialdir="assets/graphics")
        surface = pygame.image.load(file_path)
        
        max_size = 600
        if surface.get_size()[0] >= surface.get_size()[1]:
            new_width = max_size
            new_height = int(surface.get_size()[1]/surface.get_size()[0]*max_size)
        else:
            new_height = max_size
            new_width = int(surface.get_size()[0]/surface.get_size()[1]*max_size)
            
        surface = pygame.transform.scale(surface, (new_width, new_height))
        raw_str = pygame.image.tostring(surface, 'RGBA', False)
        img = Image.frombytes('RGBA', surface.get_size(), raw_str)
        tkimg = ImageTk.PhotoImage(img)

        canvas.config(width=img.size[0], height=img.size[1])
        canvas.create_image(0,0, anchor=tkinter.NW, image = tkimg)
        
        confirm_button.pack()
        cancel_button.pack()
    except:
        return get_file()
    
def split_img():
    global img, file_path
    long, haut = img.size
    long16, haut16 = long//16, haut//16
    name = file_path.split('/')[-1][:-4]
    for i in range(long16):
        for j in range(haut16):
            area=img.crop((i*16, j*16, (i+1)*16, (j+1)*16)).copy()
            area.save(f"assets/graphics/blocs/{name}_{i}-{haut16-1-j}_{long16-1}-{haut16-1}.png")
    img = None
    file_path = ""
    cancel()

def cancel():
    global confirm_button, cancel_button, openFile_button, canvas, img, file_path
    confirm_button.pack_forget()
    cancel_button.pack_forget()
    canvas.config(width=0, height=0)
    openFile_button.pack()
    img = None
    file_path = ""

root = tkinter.Tk()
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
ico = Image.open('assets/graphics/icons/split_img.ico')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)
root.title("Séparateur d'image")

openFile_button = tkinter.Button(root, text="Ouvrir un fichier", command=get_file)
openFile_button.pack()

canvas = tkinter.Canvas(root, width=0, height=0)
canvas.pack()

confirm_button = tkinter.Button(root, text="Segmenter l'image", command=split_img)
cancel_button = tkinter.Button(root, text="Annuler", command=cancel)

root.mainloop()