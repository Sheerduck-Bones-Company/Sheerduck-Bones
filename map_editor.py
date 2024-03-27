import pygame, sys, button, os

#On crée une classe permettant de gérer les blocs
class Bloc(pygame.sprite.Sprite):
    def __init__(self,
                    bloc_type:str,                              #Le nom du bloc
                    top_left:tuple = (0,0),                     #Les coordonées du bloc
                    big = False,                                #Si on l'affiche en grand ou non
                    is_above_player = False,                    #S'il doit être devant le joueur ou non
                    is_in_group = False,                        #S'il appartient à une image composée de plusieurs blocs
                    collisions = [False, False, False, False],  #Les collisions du bloc
                    map_path = '',                              #La carte à laquelle il mème si on intéragie avec lui
                    libraryx = 0,                               #Les coordonnées de son image sur la carte bibliothèque
                    libraryy = 0):
        super().__init__()
        self.type = bloc_type
        self.big = big
        self.set_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left
        self.is_above_player = is_above_player
        self.is_in_group = is_in_group
        self.collisions = [elem for elem in collisions]
        self.map_path = map_path
        self.libraryx = libraryx
        self.libraryy = libraryy
    
    #Définir l'image du bloc
    def set_image(self):
        self.image = pygame.image.load(f"assets/graphics/blocs/{self.type}.png").convert_alpha()
        self.info_surface = pygame.Surface((16,16))
        if self.big:
            self.image = pygame.transform.scale(self.image, (64,64))
            self.info_surface = pygame.Surface((64,64))
        self.info_surface.set_alpha(60)
    
    #Récupérer les collisions
    def get_booleans(self):
        return self.is_above_player, self.collisions
    
    #Dessiner les collisions
    def draw_collisions(self):
        for i, collision in enumerate(self.collisions):
            if collision:
                color = (255,0,0)
            else:
                color = (255,255,255)
            pygame.draw.rect(self.info_surface, color, pygame.Rect((i*8)%16, (i//2)*8, 8, 8))
    
    #Afficher si le bloc appartient à une image formée de plusieurs blocs
    def draw_group(self):
        if self.is_in_group:
            pygame.draw.rect(self.info_surface, (0,255,0), pygame.Rect(0, 0, 16, 16))
        else:
            pygame.draw.rect(self.info_surface, (255,0,0), pygame.Rect(0, 0, 16, 16))
    
    #Affiche si le bloc doit être afficher devant le joueur
    def draw_is_above(self):
        if self.is_above_player:
            pygame.draw.rect(self.info_surface, (0,255,0), pygame.Rect(0, 0, 16, 16))
        else:
            pygame.draw.rect(self.info_surface, (255,0,0), pygame.Rect(0, 0, 16, 16))
    
    #Affiche si le bloc mène à une carte quand on intéragie avec lui
    def draw_map_path(self):
        if self.map_path != '':
            pygame.draw.rect(self.info_surface, (0,255,0), pygame.Rect(0, 0, 16, 16))
        else:
            pygame.draw.rect(self.info_surface, (255,0,0), pygame.Rect(0, 0, 16, 16))

#On initialise la fenêtre
pygame.init()
pygame.display.set_caption('Création de map custom')
pygame.display.set_icon(pygame.image.load('assets/graphics/icons/edit_icon.ico'))

#On crée notre écran
screen_width, screen_height = 1500, 900
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)

#On crée la surface sur laquelle on va faire afficher les éléments
map_surface = pygame.Surface((2*screen_width, 2*screen_height))
size_vector = pygame.Vector2(map_surface.get_size())
new_scale = size_vector
dest = map_surface

#On crée notre clock
clock = pygame.time.Clock()
FPS = 60
    
#On défini des états
running = True
is_creating = False
is_choosing = False
is_saving = False
is_leaving = False
is_writting = False
is_writting_numb = False
is_writting_changes = False
is_writting_path = False
is_confirming = False
is_searching_for_info = False
map_saved = False
show_collisions = False
show_group = False
show_is_above = False
show_map_path = False
show_transparent_layer = True

#On défini des listes
pressed = {}
mouse_pressed = {}
img_library = {}
mape = []
map_backup = []
bloc_types = [Bloc(name[:-4], (50+(i%15)*64,50+((i//15)%10)*64), True) for i, name in enumerate(os.listdir('assets/graphics/blocs'))]   #La liste de toutes les images de blocs dans le dossier des graphiques
change_name_bloc = [[]]

#On défini les caractéristiques de la caméra
offset = pygame.Vector2(screen_width*(3/4), screen_height*(3/4))
camera_direction = pygame.Vector2()
zoom_scale = 1
last_zoom_scale = 10

#On crée des boutons
create_new_map_button = button.Button(screen, "create_new_map", 10, 50, perc_height=25)
continue_create_map_button = button.Button(screen, "continue_create_map", -10, 50, perc_height=25)
exit_button = button.Button(screen, "exit2", -0.5, 0.5, 5)
info_button = button.Button(screen, "info", -0.5, 10, 5)
save_button = button.Button(screen, "save", 20, 10, perc_height=15)
saveas_button = button.Button(screen, "saveas", 20, 30, perc_height=15)
cancel_button = button.Button(screen, "cancel", 20, 50, perc_height=15)
dontsave_button = button.Button(screen, "dontsave", 20, 70, perc_height=15)
confirm_button = button.Button(screen, "confirm", 20, 30, perc_height=15)
addchanges_button = button.Button(screen, "addchanges", 25, 10, 50)

#On crée des variables utilisées dans l'affichage de texte
font = pygame.font.SysFont(None, 50)
written_text = ""
file_name = ""
file_name_text = font.render("", True, (0,0,0))
file_name_rect = file_name_text.get_rect(center=(screen_width/2, screen_height/2))
message_text = font.render("", True, (255,0,0))
message_rect = message_text.get_rect()
message_counter = 0
confirm_text = font.render(f"Attention : \"{written_text}\" existe déjà, voulez-vous le remplacer ?", True, (255,0,0))
confirm_rect = confirm_text.get_rect()
info_text = [font.render(text, True, (0,0,0)) for text in ["Contôles utiles :", "", "q/z/d/s = Se déplacer", "LCTRL + Flèche = Ajouter des lignes/colonnes", "LSHIFT + Flèche = Retirer des lignes", "LCTRL + PLUS ou MOINS = Zoom/Dézoom", "LCTRL + z = Annulation de la dernière action", "LCTRL + s = Sauvegarder", "c = Afficher les collisions", "e = Afficher la bibliothèque", "i = Afficher le menu info", "Flèche HAUT ou BAS = Changer de couche"]]

#On défini quelques autres variables
page_number = 1
layer_number = 0
last_layer_number = 0
last_ligne = -1
last_column = -1
last_used_type = "void"
used_type =  "void"
mouse_button = 0
last_mouse_button = 0
img_x_offset = 0
img_y_offset = 0
image_width = 0
image_height = 0
imagex = 0
imagey = 0

#Faire une backup de la map
def addBackup(offsetx=0, offsety=0, delete_layer=False):
    global mape, map_backup, map_saved
    map_saved = False
    if len(map_backup) >= 100:
        del map_backup[0]
    map_backup.append([[[[bloc for bloc in ligne] for ligne in layer] for layer in mape], offsetx, offsety, delete_layer])
   
#Charger une backup de la map
def loadBackup():
    global mape, map_backup, layer_number
    if len(map_backup) >= 1:
        mape = [[[bloc for bloc in ligne] for ligne in layer] for layer in map_backup[-1][0]]
        offset.x -= map_backup[-1][1]
        offset.y -= map_backup[-1][2]
        if map_backup[-1][3]:
            layer_number -= 1
        del map_backup[-1]

#Ecrire un message
def writeMessage(text_message, counter, is_error=False):
    global message_text, message_rect, message_counter
    if is_error:
        message_text = font.render("/!\ : " + text_message, True, (255,0,0))
    else:
        message_text = font.render(text_message, True, (0,255,0))
    message_rect = message_text.get_rect()
    message_rect.center = (screen_width/2, 55)
    message_counter = counter

#Récupérer le contenu d'un fichier
def readFile(file_name):
    mape = []
    global img_library
<<<<<<< HEAD
    #On ouvre le fichier texte
=======
>>>>>>> edf370d83504322eff55ad810ee3c6530e1513ab
    with open(f'assets/map/{file_name}.txt', 'r', encoding='utf-8') as fichier:
        map_text = fichier.read()
        #Pour chaque couche, chaque ligne, on récupère les caractéristiques des blocs
        for lay_index, layer in enumerate(map_text.split('$')):
            mape.append([])
            for lin_index, ligne in enumerate(layer.split('|')):
                mape[lay_index].append([])
                for bloc_index, bloc in enumerate(ligne.split('/')):
                    if bloc == '0':
                        mape[lay_index][lin_index].append(0)
                    else:
                        crt_attributes = bloc.split(',')
                        #On récupère les caractéristiques du bloc
                        
                        #Le nom
                        crt_type = crt_attributes[0]
                        
                        #Si son nom a été rajouté dans les changements de nom d'image, on modifie le nom
                        for change in change_name_bloc[:-1]:
                            if crt_attributes[0] == change[0]:
                                crt_type = change[1]
                        
                        #Si le bloc est devant le joueur
                        if int(crt_attributes[1]) == 1:
                            crt_is_above_player = True
                        else:
                            crt_is_above_player = False
                            
                        #Si le bloc appartient à ue image composée de plusieurs blocs
                        if int(crt_attributes[2]) == 1:
                            crt_is_in_group = True
                        else:
                            crt_is_in_group = False
                        
                        #Les collisions
                        crt_collisions = []
                        for collision in crt_attributes[3]:
                            if int(collision)==1:
                                crt_collisions.append(True)
                            else:
                                crt_collisions.append(False)
                        
                        #Le potentiel lien deu blox à une carte
                        crt_map_path = crt_attributes[4]
                                
                        #On ajoute les caractéristiques du bloc à la liste de la carte
                        if file_name == "bloc_types_map":
                            mape[lay_index][lin_index].append(Bloc(crt_type, (0,0), False, crt_is_above_player, crt_is_in_group, crt_collisions, crt_map_path, bloc_index, lin_index))
                            img_library[crt_type] = (bloc_index, lin_index)
                        else:
                            mape[lay_index][lin_index].append(Bloc(crt_type, (0,0), False, crt_is_above_player, crt_is_in_group, crt_collisions, crt_map_path, img_library.get(crt_type)[0], img_library.get(crt_type)[1]))
    return mape

#Ecrire les éléments de la map dans un fichier texte
def writeMapInFile(mape, file_name):
    #On ouvre ou on crée le fichier texte
    with open(f"assets/map/{file_name}.txt", "w", encoding='utf-8') as fichier:
        map_len = len(mape)
        for layer_index, layer in enumerate(mape):
            layer_len = len(layer)
            for ligne_index, ligne in enumerate(layer):
                ligne_len = len(ligne)
                for bloc_index, bloc in enumerate(ligne):
                    #On écrit les caractéristiques du bloc
                    if bloc == 0:
                        fichier.write("0")
                    else:
                        fichier.write(bloc.type + ',')
                        if bloc.is_above_player:
                            fichier.write('1,')
                        else:
                            fichier.write('0,')
                        
                        if bloc.is_in_group:
                            fichier.write('1,')
                        else:
                            fichier.write('0,')
                        
                        for collision in bloc.collisions:
                            if collision:
                                fichier.write('1')
                            else:
                                fichier.write('0')
                        
                        fichier.write(',' + bloc.map_path)
                                
            #On segmente le fichier avec des caractères spécifiques
                    if bloc_index+1 != ligne_len:
                        fichier.write('/')
                if ligne_index+1 != layer_len:
                    fichier.write('|')
            if layer_index+1 != map_len:
                fichier.write('$')
    

#Sauvegarder la map dans un fichier texte
def save(given_file_name=""):
    global file_name, mape, is_saving, is_leaving, is_writting, is_creating, map_saved, change_name_bloc, bloc_types_map
    
    #Si un nom est donné à l'enregistrement, on change le nom du fichier
    if given_file_name != "":
        file_name = given_file_name

    #On écrit le fichier
    writeMapInFile(mape, file_name)
    
    #Si des changement de noms ont été ajoutés, on modifie également la carte bibliotèque
    if file_name != "bloc_types_map" and len(change_name_bloc) > 1:
        writeMapInFile(bloc_types_map, "bloc_types_map")
        change_name_bloc = [[]]
    
    #On enregistre que la carte est sauvegardée
    map_saved = True
    
    #On quite la fenêtre si on était en train de quitter la fenêtre, ou on reset le nom entrée lors de l'enregistrement
    if is_leaving:
        quit_program()
    elif is_saving:
        is_writting = False
        is_saving = False
        is_creating = True
        writeMessage("Map sauvegardée", 120)
    
#Quitter le programme
def quit_program():
    global running
    running = False
    pygame.quit()
    sys.exit()
                            
#On lance la boucle principale
while running:
    #On efface ce qui est sur l'écran
    screen.fill((255,255,255))
    
    if is_confirming:
        #Si on est en train de confirmer le remplacement un fichier, on affiche les boutons nécessaires
        confirm_button.draw()
        cancel_button.draw()
        screen.blit(confirm_text, confirm_rect)
        
    elif is_writting:
        #Si on est en train d'écrire du texte, on affiche les boutons nécessaires et le texte écrit
        screen.blit(file_name_text, file_name_rect)
        exit_button.draw()
        if not(is_creating or is_writting_numb or is_writting_changes or is_writting_path or is_saving):
            addchanges_button.draw()
    
    elif is_searching_for_info:
        #Si on est dans le menu info, on affiche les lignes d'infos
        exit_button.draw()
        for i, text_ligne in enumerate(info_text):
            screen.blit(text_ligne, text_ligne.get_rect(topleft=(30, 30+i*50)))
    
    elif is_creating:
        #Si on est en train de poser des blocs / configurer les collisions
        
        #Bouger la caméra
        if pressed.get(pygame.K_q):
            camera_direction.x = 1
        elif pressed.get(pygame.K_d):
            camera_direction.x = -1
        else:
            camera_direction.x = 0
                
        if pressed.get(pygame.K_z) and not pressed.get(pygame.K_LCTRL):
            camera_direction.y = 1                
        elif pressed.get(pygame.K_s):
            camera_direction.y = -1
        else:
            camera_direction.y = 0
            
        offset += camera_direction*10/zoom_scale
        
        #Créer une nouvelle surface de destination pour effectuer le bon zoom de manière optimisée
        if last_zoom_scale != zoom_scale:
            last_zoom_scale = zoom_scale
            new_scale = size_vector * zoom_scale
            dest = pygame.Surface(new_scale)
        
        #On efface ce qu'il y a sur l'écran
        map_surface.fill((255,255,255))
        
        #On dessine le contour de l'espace de création
        pygame.draw.rect(map_surface, (0,0,0), pygame.Rect((-5, -5)+offset, (len(mape[0][0])*16+10, len(mape[0])*16+10)))
        pygame.draw.rect(map_surface, (255,255,255), pygame.Rect((0, 0)+offset, (len(mape[0][0])*16, len(mape[0])*16)))
        
        #On affiche chaque bloc
        for lay, layer in enumerate(mape):
            for l, ligne in enumerate(layer):
                for c, bloc in enumerate(ligne):
                    if bloc != 0:
                        bloc.rect.topleft = (c*16, l*16)
                        
                        bloc.image.set_alpha(255)
                        
                        #Si le bloc n'est pas sur la couche actuellement éditée, on le met en transparence
                        if lay != layer_number and show_transparent_layer:
                            bloc.image.set_alpha(70)
                        
                        #On affiche les collisions du bloc
                        if show_collisions:
                            bloc.draw_collisions()
                        
                        #On affiche si le bloc appartient à une image composée de plusieurs blocs
                        if show_group:
                            bloc.draw_group()
                        
                        #On affiche si le bloc est affiché devant le joueur
                        if show_is_above:
                            bloc.draw_is_above()
                        
                        #On affiche si le bloc mène à une carte
                        if show_map_path:
                            bloc.draw_map_path()
                            
                        #On affiche le bloc
                        map_surface.blit(bloc.image, bloc.rect.topleft+offset)
                        
                        if show_group or show_is_above or show_collisions or show_map_path:
                            map_surface.blit(bloc.info_surface, bloc.rect.topleft+offset)
                        
        #On effectue le zoom et on affiche l'écran
        scaled_surf = pygame.transform.scale(map_surface, new_scale, dest)
        scaled_rect = scaled_surf.get_rect(center = (screen_width/2,screen_height/2))
        screen.blit(scaled_surf, scaled_rect)
        
        #On affiche sur quelle couche on se trouve
        layer_text = font.render(f"Layer : {layer_number}", True, (0,0,0))
        screen.blit(layer_text, pygame.Rect((10,10,0,0)))
        
        #On récupère la positions de la souris corrigée du zoom et du décalage de la caméra
        mouse_pos = pygame.mouse.get_pos() - (pygame.Vector2(scaled_rect.left, scaled_rect.top)) - (offset*zoom_scale)
        real_mouse_pos = (mouse_pos[0]/zoom_scale, mouse_pos[1]/zoom_scale)
        #On en déduit la ligne et la colonne du bloc cliqué
        ligne, column = int(real_mouse_pos[1]//16), int(real_mouse_pos[0]//16)
        
        #Lorsque l'on clique, qu'il y a un changer de position/de type utilisé/de bouton cliqué et qu'on ne montre par les collisions
        if (mouse_pressed.get(1) or mouse_pressed.get(3)) and (ligne != last_ligne or column != last_column or used_type != last_used_type or layer_number != last_layer_number or mouse_button != last_mouse_button) and not show_collisions:
            #Changer ajoute ou retire le bloc à une image composées de plusieurs blocs
            if show_group:
                if file_name == "bloc_types_map":
                    try:
                        mape[layer_number][ligne][column].is_in_group = not mape[layer_number][ligne][column].is_in_group
                    except:
                        writeMessage("Veuillez cliquer un bloc", 30, True)
            #Afficher ou non le bloc devant le joueur
            elif show_is_above:
                try:
                    mape[layer_number][ligne][column].is_above_player = not mape[layer_number][ligne][column].is_above_player
                except:
                    writeMessage("Veuillez cliquer un bloc", 30, True)
            #Ajouter un lien à un bloc
            elif show_map_path:
                if mape[layer_number][ligne][column] != 0:
                    is_writting = True
                    is_writting_path = True
                    written_text = mape[layer_number][ligne][column].map_path
                    file_name_text = font.render("Nom de la map liée : " + written_text + ".txt", True, (0,0,0))
                    file_name_rect = file_name_text.get_rect(center=(screen_width/2, screen_height/2))
            else:
                try:
                    if ligne >= 0 and column >= 0:
                        #On place un bloc
                        if mouse_pressed.get(1):
                            #Si c'est la carte bibliothèque, on ajoute juste le bloc
                            if file_name == "bloc_types_map":
                                mape[layer_number][ligne][column] = Bloc(used_type)
                            else:
                            #Si on est sur une carte autre que la carte bibliothèque
                                try:
                                    #Si le bloc appartient à une image composée de plusieurs blocs, on les affiche toutes ou on les affiche selon un paterne répétitif
                                    if len(used_type[0].split('_')) > 1:
                                        #On ajoute le décalage entre le dernier bloc cliqué et le bloc actuellement cliqué
                                        img_x_offset += column-last_column
                                        img_y_offset += ligne-last_ligne
                                        
                                        #Si le bloc actuel fait partie d'un groupe d'image fixe, on affiche tous les blocs de l'image
                                        if used_type[2]:
                                            try:
                                                for ligne_num in range(used_type[5]-(image_height-imagey), used_type[5]+imagey+1, 1):
                                                    for column_num in range(used_type[4]-imagex, used_type[4]-imagex+image_width+1, 1):
                                                        if bloc_types_map[0][ligne_num][column_num] != 0:
                                                            #On réupère le type de bloc qu'il faut poser
                                                            model = bloc_types_map[0][ligne_num][column_num]
                                                            mape[layer_number][ligne-(used_type[5]-ligne_num)][column-(used_type[4]-column_num)] = Bloc(bloc_type = model.type,
                                                                                                                                                        is_above_player = model.is_above_player,
                                                                                                                                                        is_in_group = model.is_in_group,
                                                                                                                                                        collisions = model.collisions,
                                                                                                                                                        libraryx = model.libraryx,
                                                                                                                                                        libraryy = model.libraryy)
                                            except:
                                                writeMessage("Veuillez rajouter des lignes ou des collones", 60, True)
                                                loadBackup()
                                        #Si le bloc fait partie d'une image qui se répète automatique, on place le bloc adéquat
                                        else:
                                            #On récupère les coordonnées du bloc qu'il faut poser
                                            if imagex+img_x_offset == image_width+1:
                                                img_x_offset -= image_width+1
                                            elif int(used_type[0].split('_')[1].split('-')[0])+img_x_offset == -1:
                                                img_x_offset += image_width+1
                                            
                                            if imagey-img_y_offset == image_height+1:
                                                img_y_offset += image_height+1
                                            elif imagey-img_y_offset == -1:
                                                img_y_offset -= image_height+1
                                            
                                            #On récupère le type de bloc qu'il faut poser
                                            model = bloc_types_map[0][ligne2+img_y_offset][column2+img_x_offset]    
                                            mape[layer_number][ligne][column] = Bloc(bloc_type = model.type,
                                                                                    is_above_player = model.is_above_player,
                                                                                    is_in_group = model.is_in_group,
                                                                                    collisions = model.collisions,
                                                                                    libraryx = model.libraryx,
                                                                                    libraryy = model.libraryy)
                                    else:
                                        mape[layer_number][ligne][column] = Bloc(used_type[0], is_above_player=used_type[1], is_in_group=used_type[2], collisions=used_type[3], libraryx=used_type[4], libraryy=used_type[5])
                                        
                                except:
                                    writeMessage("Une erreur est survenue", 30, True)
                        #On efface un bloc
                        elif mouse_pressed.get(3):
                            mape[layer_number][ligne][column] = 0
                except IndexError:
                    #Si on clique en dehors de l'espace d'édition
                    writeMessage("Veuillez rajouter des lignes ou des colonnes", 60, True)
            
            last_ligne, last_column, last_used_type, last_layer_number, last_mouse_button = ligne, column, used_type, layer_number, mouse_button
                
        exit_button.draw()
        info_button.draw()
                
    elif is_choosing:
        #Si on est en train de choisir le type de bloc à poser
        
        #Si on est en train d'éditer la bibliothèque
        if file_name == "bloc_types_map":
            #On affiche chaque type de bloc
            for bloc in bloc_types[(page_number-1)*150:page_number*150]:
                    screen.blit(bloc.image, bloc.rect)
        
        #Si on est en train de créer / éditer une autre map
        else:
            
            #Bouger la caméra
            if pressed.get(pygame.K_q):
                camera_direction.x = 1
            elif pressed.get(pygame.K_d):
                camera_direction.x = -1
            else:
                camera_direction.x = 0
                    
            if pressed.get(pygame.K_z) and not pressed.get(pygame.K_LCTRL):
                camera_direction.y = 1                
            elif pressed.get(pygame.K_s):
                camera_direction.y = -1
            else:
                camera_direction.y = 0
                
            offset2 += camera_direction*10/zoom_scale2
            
            #Créer une nouvelle surface de destination pour effectuer le bon zoom
            if last_zoom_scale2 != zoom_scale2:
                last_zoom_scale2 = zoom_scale2
                new_scale2 = size_vector2 * zoom_scale2
                dest2 = pygame.Surface(new_scale2)
            
            #On efface ce qu'il y a sur l'écran
            bloc_types_surface.fill((255,255,255))
            
            #On dessine le contour de la bibliothèque
            pygame.draw.rect(bloc_types_surface, (0,0,0), pygame.Rect((-5, -5)+offset2, (len(bloc_types_map[0][0])*16+10, len(bloc_types_map[0])*16+10)))
            pygame.draw.rect(bloc_types_surface, (255,255,255), pygame.Rect((0, 0)+offset2, (len(bloc_types_map[0][0])*16, len(bloc_types_map[0])*16)))
            
            #On affiche chaque bloc
            for lay, layer in enumerate(bloc_types_map):
                for l, ligne in enumerate(layer):
                    for c, bloc in enumerate(ligne):
                        if bloc != 0:
                            bloc.rect.topleft = (c*16, l*16)
                            
                            #On affiche les collisions du bloc
                            if show_collisions2:
                                bloc.draw_collisions()
                            
                            #On affiche si le bloc appartient à une image composée de plusieurs blocs
                            if show_group2:
                                bloc.draw_group()
                                
                            #Si le bloc est affiché devant le joueur
                            if show_is_above2:
                                bloc.draw_is_above()
                            
                            #Si le bloc mène à un bloc
                            if show_map_path2:
                                bloc.draw_map_path()
                            
                            #On affiche le bloc
                            bloc_types_surface.blit(bloc.image, bloc.rect.topleft+offset2)
                            
                            if show_group2 or show_is_above2 or show_collisions2 or show_map_path2:
                                bloc_types_surface.blit(bloc.info_surface, bloc.rect.topleft+offset2)
            
            #On effectue le zoom et on affiche l'écran
            scaled_bloc_types_surf = pygame.transform.scale(bloc_types_surface, new_scale2, dest2)
            scaled_bloc_types_rect = scaled_bloc_types_surf.get_rect(center = (screen_width/2,screen_height/2))
            screen.blit(scaled_bloc_types_surf, scaled_bloc_types_rect)
            
            #On récupère la positions de la souris corrigée du zoom et du décalage de la caméra
            mouse_pos2 = pygame.mouse.get_pos() - (pygame.Vector2(scaled_bloc_types_rect.left, scaled_bloc_types_rect.top)) - (offset2*zoom_scale2)
            real_mouse_pos2 = (mouse_pos2[0]/zoom_scale2, mouse_pos2[1]/zoom_scale2)
            #On en déduit la ligne et la colonne du bloc cliqué
            ligne2, column2 = int(real_mouse_pos2[1]//16), int(real_mouse_pos2[0]//16)
        
        exit_button.draw()
        info_button.draw()
        
    elif is_leaving:
        #Si on est en train de quitter la fenêtre
        if file_name != "":
            save_button.draw()
        if file_name != "bloc_types_map":
            saveas_button.draw()
        cancel_button.draw()
        dontsave_button.draw()
        
    elif is_saving:
        #Si on est en train de sauvegarder
        if file_name != "":
            save_button.draw()
        if file_name != "bloc_types_map":
            saveas_button.draw()
        cancel_button.draw()
        
    else:
        #Si on est sur le menu de démarage
        create_new_map_button.draw()
        continue_create_map_button.draw()
        exit_button.draw()
        info_button.draw()
    
    if message_counter > 0:
        #S'il faut montrer un message d'erreur
        screen.blit(message_text, message_rect)
        message_counter -= 1
    
    #On actualise l'écran    
    pygame.display.flip()
    
    #On vérifie des events
    for event in pygame.event.get():
        
        #Quitter la fenêtre
        if event.type == pygame.QUIT:
            quit_program()
        
        if event.type == pygame.KEYDOWN:
            #On ajoute la touche appuyée à une liste et on précise son état
            pressed[event.key] = True
            
            #Mettre en plein écran
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()              
            
            if is_confirming:
                #Quitter la confirmation
                if event.key == pygame.K_ESCAPE:
                    is_confirming = False
                    written_text = ""
                    file_name_text = font.render("Nom du fichier : " + written_text + ".txt", True, (0,0,0))
                    file_name_rect = file_name_text.get_rect(center=(screen_width/2, screen_height/2))
                
                #Confirmer et sauvegarder
                if event.key == pygame.K_RETURN:
                    save(written_text)
                        
            elif is_writting:
                #Effacer
                if event.key == pygame.K_BACKSPACE:
                    if pressed.get(pygame.K_LCTRL):
                        written_text = ''
                    else:
                        written_text = written_text[:-1]
                
                #Cas particulier de la touche 6
                elif event.key == pygame.K_6:
                    if pressed.get(pygame.K_LSHIFT):
                        written_text += '6'
                    else:
                        written_text += "-"
                
                #Cas particulier de la touche 8
                elif event.key == pygame.K_8:
                    if pressed.get(pygame.K_LSHIFT):
                        written_text += '8'
                    else:
                        written_text += "_"
                
                #Cas particulier du point
                elif event.key == pygame.K_SEMICOLON:
                    if pressed.get(pygame.K_LSHIFT):
                        written_text += '.'
                    else:
                        written_text += ";"
                
                #Ecrire une lettre ou un chiffre
                elif (97 <= event.key <= 122) or (48 <= event.key <= 57):
                    if pressed.get(pygame.K_LSHIFT):
                        written_text += chr(event.key-32)
                    else:
                        written_text += chr(event.key)
                
                #Ecrire un chiffre
                elif (1073741913 <= event.key <= 1073741922):
                    written_text += str((event.key - 1073741912)%10)
                
                #Envoyer le texte saisi
                elif event.key == pygame.K_RETURN:
                    if is_writting_numb:
                        #On crée une nouvelle map avec les dimensions données
                        try:
                            #On crée la carte avec la bonne taille
                            width, height = int(written_text.split('x')[0]), int(written_text.split('x')[1])
                            mape = [[[0]*width for i in range(height)]]
                            
                            #On récupère la carte bibliothèque
                            bloc_types_map = readFile("bloc_types_map")
                                
                            #On crée la surface sur laquelle on va faire afficher la bibliothèque
                            bloc_types_surface = pygame.Surface((2*screen_width, 2*screen_height))
                            size_vector2 = pygame.Vector2(bloc_types_surface.get_size())
                            new_scale2 = size_vector
                            dest2 = bloc_types_surface
                                
                            #On crée les caractéristiques de la caméra de la carte bibliothèque
                            offset2 = pygame.Vector2(screen_width*(3/4), screen_height*(3/4))
                            zoom_scale2 = 1
                            last_zoom_scale2 = 10
                            show_collisions2 = False
                            show_is_above2 = False
                            show_group2 = False
                            show_map_path2 = False
                                
                            is_writting = False
                            is_writting_numb = False
                            is_creating = True
                        except:
                            writeMessage("Taille incorrecte", 120, True)
                    
                    #Si on est en train de lier une carte à un bloc
                    elif is_writting_path:
                        #Si la carte existe bien, on rajoute le lien
                        if written_text + '.txt' in os.listdir("assets/map"):
                            mape[layer_number][ligne][column].map_path = written_text
                            writeMessage("Lien ajouté", 60)
                            is_writting = False
                            is_writting_path = False
                        #Si rien n'est écrit, on enlève le lien déjà existant
                        elif written_text == "":
                            mape[layer_number][ligne][column].map_path = written_text
                            writeMessage("Lien retiré", 60)
                            is_writting = False
                            is_writting_path = False
                        else:
                            writeMessage("Carte introuvable", 120, True)

                    #Si on ajoute des changements de nom pour des images
                    elif is_writting_changes:
                        #On entre l'ancien nom
                        if len(change_name_bloc[-1]) == 0:
                            change_name_bloc[-1].append(written_text)
                        #On entre le nouveau nom
                        else:
                            if written_text + ".png" in os.listdir("assets/graphics/blocs"):
                                change_name_bloc[-1].append(written_text)
                                change_name_bloc.append([])
                                is_writting_changes = False
                                writeMessage("Modifications ajoutées", 120)
                            else:
                                writeMessage("Ce nom d'image n'existe pas", 120, True)
                            
                    #Si on est en train de sauvegarder
                    elif is_leaving or is_saving:
                        #On vérifie si le fichier n'existe pas déjà et on sauvgarde
                        if written_text+'.txt' in os.listdir('assets/map') and written_text != file_name:
                            is_confirming = True
                            confirm_text = font.render(f"Attention : \"{written_text}\" existe déjà, voulez-vous le remplacer ?", True, (255,0,0))
                            confirm_rect = confirm_text.get_rect()
                            confirm_rect.center=(screen_width/2, 70)
                        else:
                            save(written_text)
                    
                    #Si on est en train d'ouvrir une carte
                    else:
                        #On ouvre le fichier donné et on interprète le fichier texte
                        try:
                            if written_text != "bloc_types_map":
                                bloc_types_map = readFile("bloc_types_map")
                                
                                #On crée la surface sur laquelle on va faire afficher la bibliothèque
                                bloc_types_surface = pygame.Surface((2*screen_width, 2*screen_height))
                                size_vector2 = pygame.Vector2(bloc_types_surface.get_size())
                                new_scale2 = size_vector
                                dest2 = bloc_types_surface
                                
                                #On crée les caractéristiques de la caméra de la bibliothèque
                                offset2 = pygame.Vector2(screen_width*(3/4), screen_height*(3/4))
                                zoom_scale2 = 1
                                last_zoom_scale2 = 10
                                show_collisions2 = False
                                show_is_above2 = False
                                show_group2 = False
                                show_map_path2 = False
                            
                            mape = readFile(written_text)
                            
                            file_name = written_text
                            is_writting = False
                            is_creating = True
                            
                        except FileNotFoundError:
                            writeMessage("Fichier introuvable", 120, True)
                    
                    written_text = ""
                    
                #Quitter la saisi de texte
                elif event.key == pygame.K_ESCAPE:
                    if is_writting_changes:
                        is_writting_changes = False
                        if len(change_name_bloc[-1]) != 0:
                            del change_name_bloc[-1]
                        file_name_text = font.render("Nom du fichier : .txt", True, (0,0,0))
                        file_name_rect = file_name_text.get_rect(center=(screen_width/2, screen_height/2))
                    else:
                        is_writting = False
                        is_writting_numb = False
                        is_writting_path = False
                    written_text = ""
                        
                #Ecrire une erreur de saisie
                else:
                    writeMessage("Charactère inconnu", 60, True)
                
                #On crée le bon affichage en fonction de ce qu'on est en train d'écrire
                if is_writting_numb:
                    file_name_text = font.render("Taille de la map : " + written_text + " blocs", True, (0,0,0))
                elif is_writting_changes:
                    if len(change_name_bloc[-1]) == 0:
                        file_name_text = font.render("Ancien nom de l'image : " + written_text + ".png", True, (0,0,0))
                    else:
                        file_name_text = font.render("Nouveau nom de l'image : " + written_text + ".png", True, (0,0,0))
                elif is_writting_path:
                    file_name_text = font.render("Nom de la map liée : " + written_text + ".txt", True, (0,0,0))
                else:
                    file_name_text = font.render("Nom du fichier : " + written_text + ".txt", True, (0,0,0))
                file_name_rect = file_name_text.get_rect(center=(screen_width/2, screen_height/2))
            
            elif is_searching_for_info:
                #Quitter le menu info
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                    is_searching_for_info = False
                    
            elif is_creating:
                #Quitter l'éditeur
                if event.key == pygame.K_ESCAPE:
                    if not map_saved:
                        is_leaving = True
                        is_creating = False
                    else:
                        quit_program()
                
                #Ouvrir la bibliothèque de choix        
                if event.key == pygame.K_e:
                    is_creating = False
                    is_choosing = True
                    camera_direction = pygame.Vector2()
                
                #Afficher/faire disparaitre les colisions des blocs
                if event.key == pygame.K_c and not (show_group or show_is_above or show_map_path):
                    if show_collisions:
                        for layer in mape:
                            for ligne in layer:
                                for bloc in ligne:
                                    if bloc != 0:
                                        bloc.set_image()
                    show_collisions = not show_collisions
                
                #Afficher/faire disparaitre les groupes de bloc
                if event.key == pygame.K_g and not (show_collisions or show_is_above or show_map_path):
                    if show_group:
                        for layer in mape:
                            for ligne in layer:
                                for bloc in ligne:
                                    if bloc != 0:
                                        bloc.set_image()
                    show_group = not show_group
                
                #Afficher/faire disparaitre les blocs affichés devant le joueur
                if event.key == pygame.K_r and not (show_collisions or show_group or show_map_path):
                    if show_is_above:
                        for layer in mape:
                            for ligne in layer:
                                for bloc in ligne:
                                    if bloc != 0:
                                        bloc.set_image()
                    show_is_above = not show_is_above
                
                #Afficher/faire disparaitre les liens des blocs
                if event.key == pygame.K_p and not (show_collisions or show_group or show_is_above):
                    if show_map_path:
                        for layer in mape:
                            for ligne in layer:
                                for bloc in ligne:
                                    if bloc != 0:
                                        bloc.set_image()
                    show_map_path = not show_map_path
                    
                #Afficher disparaître le menu d'infos
                if event.key == pygame.K_i:
                    is_searching_for_info = True
                
                #Actver / Désactiver la transparence des couches
                if event.key == pygame.K_l:
                    show_transparent_layer = not show_transparent_layer
                    
                    
                #Passer à la couche suppérieur et en créer une s'il le faut
                if pressed.get(pygame.K_UP) and not (pressed.get(pygame.K_LCTRL) or pressed.get(pygame.K_LSHIFT)):
                    addBackup(delete_layer=True)
                    layer_number += 1
                    if len(mape) == layer_number:
                        mape.append([[0]*len(mape[0][0]) for ligne in mape[0]])
                
                #Passer à la couche inférieur                
                if pressed.get(pygame.K_DOWN) and not (pressed.get(pygame.K_LCTRL) or pressed.get(pygame.K_LSHIFT)):
                    if layer_number >= 1:
                        layer_number -= 1
                
                
                #Ajouter une colonne à gauche
                if pressed.get(pygame.K_LCTRL) and pressed.get(pygame.K_LEFT):
                    addBackup(offsetx=-16)
                    for layer in mape:
                        for ligne in layer:
                            ligne.insert(0, 0)
                    offset.x -= 16
                
                #Ajouter une colonne à droite
                if pressed.get(pygame.K_LCTRL) and pressed.get(pygame.K_RIGHT):
                    addBackup()
                    for layer in mape:
                        for ligne in layer:
                            ligne.append(0)
                
                #Ajouter une ligne en haut
                if pressed.get(pygame.K_LCTRL) and pressed.get(pygame.K_UP):
                    addBackup(offsety=-16)
                    for layer in mape:
                        layer.insert(0, [0]*len(mape[0][0]))
                    offset.y -= 16
                
                #Ajouter une ligne en bas
                if pressed.get(pygame.K_LCTRL) and pressed.get(pygame.K_DOWN):
                    addBackup()
                    for layer in mape:
                        layer.append([0]*len(mape[0][0]))
                    
                
                #Retirer une colonne à droite
                if pressed.get(pygame.K_LSHIFT) and pressed.get(pygame.K_LEFT) and len(mape[0][0]) > 1:
                    addBackup()
                    for layer in mape:
                        for ligne in layer:
                            del(ligne[-1])
                
                #Retirer une colonne à gauche
                if pressed.get(pygame.K_LSHIFT) and pressed.get(pygame.K_RIGHT) and len(mape[0][0]) > 1:
                    addBackup(offsetx=16)
                    for layer in mape:
                        for ligne in layer:
                            del(ligne[0])
                    offset.x += 16
                
                #Retirer une ligne en bas
                if pressed.get(pygame.K_LSHIFT) and pressed.get(pygame.K_UP) and len(mape[0]) > 1:
                    addBackup()
                    for layer in mape:
                        del(layer[-1])
                
                #Retirer une ligne en haut
                if pressed.get(pygame.K_LSHIFT) and pressed.get(pygame.K_DOWN) and len(mape[0]) > 1:
                    addBackup(offsety=16)
                    for layer in mape:
                        del(layer[0])
                    offset.y += 16
                    
                
                #Zoomer
                if pressed.get(pygame.K_LCTRL) and pressed.get(pygame.K_KP_PLUS) and zoom_scale <= 4.5:
                    zoom_scale += 0.5
                
                #Dézoomer
                if pressed.get(pygame.K_LCTRL) and pressed.get(pygame.K_KP_MINUS) and zoom_scale >= 1:
                    zoom_scale -= 0.5
                
                
                #Annuler la dernière action
                if pressed.get(pygame.K_LCTRL) and pressed.get(pygame.K_z):
                    loadBackup()
                
                #Enregistrer la map
                if pressed.get(pygame.K_LCTRL) and pressed.get(pygame.K_s):
                    is_saving = True
                    is_creating = False
                    
            elif is_choosing:
                #Quitter la bibliothèque
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    is_creating = True
                    is_choosing = False
                    
                #Afficher le menu d'infos
                if event.key == pygame.K_i:
                    is_searching_for_info = True
                
                #Si on édite la map bibliothèque
                if file_name == "bloc_types_map":
                    
                    #Passer à la page de blocs suivante
                    if event.key == pygame.K_RIGHT:
                        page_number = page_number%(len(bloc_types)//150+1)+1
                        
                    #Passer à la page de blocs précédente
                    if event.key == pygame.K_LEFT:
                        if page_number == 1:
                            page_number = len(bloc_types)//150+1
                        else:
                            page_number -= 1
                
                #Si on est en train de créer / éditer une autre map que la bobliothèque
                else:
                    #Afficher/faire disparaître les colisisons des blocs
                    if event.key == pygame.K_c and not (show_group or show_is_above or show_map_path):
                        if show_collisions:
                            for layer in bloc_types_map:
                                for ligne in layer:
                                    for bloc in ligne:
                                        if bloc != 0:
                                            bloc.set_image()
                        show_collisions2 = not show_collisions2
                    
                    #Afficher/faire disparaître les groupes de bloc
                    if event.key == pygame.K_g and not (show_collisions or show_is_above or show_map_path):
                        if show_group:
                            for layer in bloc_types_map:
                                for ligne in layer:
                                    for bloc in ligne:
                                        if bloc != 0:
                                            bloc.set_image()
                        show_group2 = not show_group2
                    
                    #Afficher/faire disparaître les blocs devant le joueur
                    if event.key == pygame.K_r and not (show_collisions or show_group or show_map_path):
                        if show_is_above:
                            for layer in bloc_types_map:
                                for ligne in layer:
                                    for bloc in ligne:
                                        if bloc != 0:
                                            bloc.set_image()
                        show_is_above2 = not show_is_above2
                    
                    #Afficher/faire disparaître les liens des blocs
                    if event.key == pygame.K_p and not (show_collisions or show_group or show_is_above):
                        if show_map_path:
                            for layer in bloc_types_map:
                                for ligne in layer:
                                    for bloc in ligne:
                                        if bloc != 0:
                                            bloc.set_image()
                        show_map_path2 = not show_map_path2
                    
                    #Zoomer
                    if pressed.get(pygame.K_LCTRL) and pressed.get(pygame.K_KP_PLUS) and zoom_scale <= 4.5:
                        zoom_scale2 += 0.5
                    
                    #Dézoomer
                    if pressed.get(pygame.K_LCTRL) and pressed.get(pygame.K_KP_MINUS) and zoom_scale >= 1:
                        zoom_scale2 -= 0.5
                    
            elif is_leaving:
                #Annuler la sortie de l'éditeur
                if event.key == pygame.K_ESCAPE:
                    is_leaving = False
                    is_creating = True
                    
            elif is_saving:
                #Annuler la sauvegarde
                if event.key == pygame.K_ESCAPE:
                    is_saving = False
                    is_creating = True
            
            else:
                #Quitter l'éditeur
                if event.key == pygame.K_ESCAPE:        
                    quit_program()
                    
                #Afficher/faire disparaître le menu d'infos
                if event.key == pygame.K_i:
                    is_searching_for_info = True
                    
        #On précise qu'une touche n'est plus pressée
        if event.type == pygame.KEYUP:
            pressed[event.key] = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            #On ajoute le boutton appuyé à une liste et on précise son état
            mouse_pressed[event.button] = True
            mouse_button = event.button
            
            #Si le boutton est la molette on récupère le type du bloc cliqué
            if event.button == 2:
                if is_creating:
                    try:
                        if file_name == "bloc_types_map":
                            used_type = mape[layer_number][ligne][column].type
                        else:
                            bloc = mape[layer_number][ligne][column]
                            used_type = [bloc.type, bloc.is_above_player, bloc.is_in_group, bloc.collisions, bloc.libraryx, bloc.libraryy]
                    except:
                        #On écrit un message d'erreur car aucun bloc n'a été cliqué
                        writeMessage("Veuillez cliquer sur un bloc", 60, True)
                        
            #Si le bouton est le clique gauche
            elif event.button == 1:  
                if is_confirming:
                    #On confirme la sauvegarde et on écrase le fichier pré-existant
                    if confirm_button.rect.collidepoint(event.pos):
                        save(written_text)

                    #On annule la sauvegarde
                    if cancel_button.rect.collidepoint(event.pos):
                        is_confirming = False
                        written_text = ""
                        file_name_text = font.render("Nom du fichier : " + written_text + ".txt", True, (0,0,0))
                        file_name_rect = file_name_text.get_rect(center=(screen_width/2, screen_height/2))
                
                elif is_writting:
                    #On sort de la saisie de texte
                    if exit_button.rect.collidepoint(event.pos):
                        if is_writting_changes:
                            is_writting_changes = False
                            if len(change_name_bloc[-1]) != 0:
                                del change_name_bloc[-1]
                            file_name_text = font.render("Nom du fichier : .txt", True, (0,0,0))
                            file_name_rect = file_name_text.get_rect(center=(screen_width/2, screen_height/2))
                        else:
                            is_writting = False
                            written_text = ""
                    
                    #On retire le dernier changement incomplet
                    if addchanges_button.rect.collidepoint(event.pos) and not(is_creating or is_writting_numb or is_writting_changes):
                        is_writting_changes = True
                        file_name_text = font.render("Ancien nom de l'image : .png", True, (0,0,0))
                        file_name_rect = file_name_text.get_rect(center=(screen_width/2, screen_height/2))
                
                elif is_searching_for_info:
                    #On sort du menu info
                    if exit_button.rect.collidepoint(event.pos):
                        is_searching_for_info = False
                        mouse_pressed[event.button] = False
                        
                elif is_creating:
                    #On quitte l'éditeur en sauvegardant ou non
                    if exit_button.rect.collidepoint(event.pos):
                        if not map_saved:
                            is_leaving = True
                            is_creating = False
                        else:
                            quit_program()
                    
                    #On ouvre le menu info
                    elif info_button.rect.collidepoint(event.pos):
                        is_searching_for_info = True
                        
                    #On ajoute une backup de la map    
                    else:
                        addBackup()
                        #Si on est en train de poser un bloc appartenant à une image composée de plusieurs blocs
                        if file_name != "bloc_types_map":
                            if len(used_type[0].split("_")) > 1:
                                #On récupère la largeur et la hauteur de l'image totale
                                image_width = int(used_type[0].split("_")[2].split("-")[0])
                                image_height = int(used_type[0].split("_")[2].split("-")[1])
                                #On récupère les coordonnée du bloc dans l'image totale
                                imagex = int(used_type[0].split("_")[1].split("-")[0])
                                imagey = int(used_type[0].split("_")[1].split("-")[1])
                                #On calcule le décalage entre le dernier bloc cliqué et le bloc actuellement cliqué
                                img_x_offset = last_column-column
                                img_y_offset = last_ligne-ligne
                        
                    #On vérifie si les collisions sont activées et qu'on en change une
                    if show_collisions:
                        try:
                            bloc = mape[layer_number][ligne][column]

                            if pygame.Rect(bloc.rect.topleft, (8, 8)).collidepoint(real_mouse_pos):
                                bloc.collisions[0] = not bloc.collisions[0]
                            if pygame.Rect(bloc.rect.midtop, (8, 8)).collidepoint(real_mouse_pos):
                                bloc.collisions[1] = not bloc.collisions[1]
                            if pygame.Rect(bloc.rect.midleft, (8, 8)).collidepoint(real_mouse_pos):
                                bloc.collisions[2] = not bloc.collisions[2]
                            if pygame.Rect(bloc.rect.center, (8, 8)).collidepoint(real_mouse_pos):
                                bloc.collisions[3] = not bloc.collisions[3]
                                
                        except:
                            #On écrit un message d'erreur car aucun bloc n'a été cliqué
                            writeMessage("Veuillez cliquer sur un bloc", 60, True)
                        
                elif is_choosing:
                    #Quitter la bibliothèque
                    if exit_button.rect.collidepoint(event.pos):
                        is_creating = True
                        is_choosing = False
                        mouse_pressed[event.button] = False
                        
                    #On ouvre le menu info
                    if info_button.rect.collidepoint(event.pos):
                        is_searching_for_info = True
                    
                    #Si on édite la bibliothèque
                    if file_name == "bloc_types_map":
                        #On vérifie si un bloc a été cliqué et on prend son type
                        for bloc in bloc_types[(page_number-1)*150:page_number*150]:
                            if bloc.rect.collidepoint(event.pos):
                                used_type = bloc.type
                                is_creating = True
                                is_choosing = False
                                mouse_pressed[event.button] = False
                                break
                            
                    #Si on crée / édite une autre map que la bobliothèque
                    else:
                        #On récupère le type et les collisions du bloc cliqué
                        try:
                            bloc = bloc_types_map[0][ligne2][column2]
                            used_type = [bloc.type, bloc.is_above_player, bloc.is_in_group, bloc.collisions, bloc.libraryx, bloc.libraryy]
                            is_choosing = False
                            is_creating = True
                            show_collisions2 = False
                            mouse_pressed[event.button] = False
                                
                        except:
                            #On écrit un message d'erreur car aucun bloc n'a été cliqué
                            writeMessage("Veuillez cliquer sur un bloc", 60, True)
                
                elif is_leaving:
                    #On sauvegarde
                    if save_button.rect.collidepoint(event.pos) and file_name != '':
                        save()
                    
                    #On sauvegarde avec un nom précis
                    if saveas_button.rect.collidepoint(event.pos):
                        is_writting = True
                    
                    #On annule la sortie de l'éditeur
                    if cancel_button.rect.collidepoint(event.pos) and not is_writting:
                        is_leaving = False
                        is_creating = True
                        mouse_pressed[event.button] = False
                    
                    #On sort sans sauvegarder
                    if dontsave_button.rect.collidepoint(event.pos):
                        quit_program()
                        
                elif is_saving:
                    #On sauvegarde
                    if save_button.rect.collidepoint(event.pos) and file_name != '':
                        save()
                        mouse_pressed[event.button] = False
                    
                    #On sauvegarde avec un nom précis
                    if saveas_button.rect.collidepoint(event.pos):
                        is_writting = True
                        mouse_pressed[event.button] = False

                    #On annule la sauvegarde
                    if cancel_button.rect.collidepoint(event.pos) and not is_writting:
                        is_leaving = False
                        is_creating = True
                        mouse_pressed[event.button] = False
                        
                else:
                    #On commence une nouvelle map en demandant les dimensions de bases
                    if create_new_map_button.rect.collidepoint(event.pos):
                        is_writting_numb = True
                        is_writting = True
                        file_name_text = font.render("Taille de la map : " + written_text + " blocs", True, (0,0,0))
                        file_name_rect = file_name_text.get_rect(center=(screen_width/2, screen_height/2))
                    
                    #On continue une map pré-existant en demandant le nom du fichier
                    if continue_create_map_button.rect.collidepoint(event.pos):
                        is_writting = True
                        file_name_text = font.render("Nom du fichier : " + written_text + ".txt", True, (0,0,0))
                        file_name_rect = file_name_text.get_rect(center=(screen_width/2, screen_height/2))
                    
                    #On ouvre le menu info
                    if info_button.rect.collidepoint(event.pos):
                        is_searching_for_info = True
                    
                    #On quitte l'éditeur
                    if exit_button.rect.collidepoint(event.pos):
                        quit_program()
                    
        #On précise si un clique est relaché
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed[event.button] = False
            
        #Changer le zoom de la caméra
        if event.type == pygame.MOUSEWHEEL:
            if is_creating or is_choosing:
                if (5 > zoom_scale + event.y > 0.5) and is_creating:
                    zoom_scale += event.y * 0.08

                if file_name != "bloc_types_map":
                    if (5 > zoom_scale2 + event.y > 0.5) and is_choosing:
                        zoom_scale2 += event.y * 0.08
    
    #On actualise la clock
    clock.tick(FPS)