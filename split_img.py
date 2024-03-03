from PIL import Image
import tkinter
from tkinter import filedialog
from tkinter import ttk

def split_img(img):
    long, haut = img.size
    long16, haut16 = long//16, haut//16
    for i in range(long16):
        for j in range(haut16):
            area=img.crop((i*16, j*16, (i+1)*16, (j+1)*16)).copy()
            area.save(f"assets/graphics/splited/test_{i}-{haut16-1-j}_{long16-1}-{haut16-1}.png")
        
def get_file():
    try:
        file_path = filedialog.askopenfilename(initialdir="assets/graphics")
        img = Image.open(file_path).convert("RGBA")
        split_img(img)
    except:
        return get_file()
    
root = tkinter.Tk()

openFile_button = ttk.Button(root, text="Ouvrir un fichier", command=get_file)
openFile_button.pack()

root.mainloop()