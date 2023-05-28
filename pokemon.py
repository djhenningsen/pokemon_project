import time
import random
import requests
import io
from urllib.request import urlopen
import pygame
from pygame.locals import *

#sprite sheet to draw characters
sprite_url = 'https://pokeapi.co/api/v2'

pygame.init() #initalize pygame


#create some needed colors and fonts
red = (250,0,0)
green = (0,250,0)
grey = (200,200,200)
black = (10,10,10)
gold = (200,160,30)
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font(pygame.font.get_default_font(), 16)

#creating game window
width = 500 
height = 500 
size = (width,height)
screen = pygame.display.set_mode(size) #creates screen of given size
screen.fill(grey) #folls screen with background color


#screen creating
class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, types, strong, weak, moves, EVs, size, x, y):
        self.name = name #name of Pokemon
        self.types = types #type of Pokemon [fire,water,etc.]
        self.strong = strong #what this Pokemon is strong against
        self.weak = weak #what this Pokemon is weak to
        self.moves = moves #list of moves Pokemon can do
        self.attack = EVs['Attack'] #EVs are stat values held in a dic, this one is attack
        self.defense = EVs['Defense'] #EV for defense
        self.speed = EVs['Speed'] #EV for speed
        self.health = EVs['Health'] #health of Pokemon
        self.current_hp = EVs['Health'] #allows for updating health, defaults to max
        self.size = size #sets size of Pokemon on screen
        self.x = x #sets its x position on screen
        self.y = y #sets its y position on screen
        self.hp_x = x #sets x position for healthbar
        self.hp_y = y #sets y position for healthbar
        
        # this bit from documentation of https://pokeapi.co/api/v2
        pygame.sprite.Sprite.__init__(self) #allows for sprite for Pokemon object
        req = requests.get(f'{sprite_url}/pokemon/{name.lower()}') #requests sprite from url
        self.json = req.json() #requests json file for sprite sheet info, can pull stats from here too but we'll just make our own
        self.set_sprite('front_default') #sets sprite for object defaulted to front
        ###########################################################
        
    #for  diplaying move
    def move_message(self, move):
        return str(self.name + ' used ' + move + '.....')
    #for  diplaying heal
    def heal_message(self):
        return str(self.name + ' uses a potion.....')
    #for  diplaying win
    def win_message(self):
        return str('.....' + self.name + ' WINS!')
    #for  diplaying lose
    def lose_message(self):
        return str(self.name + ' has fainted......')
    #for  diplaying miss
    def miss_message(self):
        return str(self.name + ' missed.....')
        
    # this function from documentation of https://pokeapi.co/api/v2
    # allows object to set the sprite for itself using the sprite sheet from url, needed to switch between back and front
    def set_sprite(self, side):
        # set the pokemon's sprite
        image = self.json['sprites'][side]
        image_stream = urlopen(image).read()
        image_file = io.BytesIO(image_stream)
        self.image = pygame.image.load(image_file).convert_alpha()
        
        # scale the image
        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height = self.image.get_height() * scale
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
    ###############################################################################
    # this function from documentation of https://pokeapi.co/api/v2
    # draws the sprite on the pygame screen
    def draw(self, alpha=255):
        sprite = self.image.copy()
        transparency = (255,255,255,alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        screen.blit(sprite,(self.x,self.y))
    ##############################################################
    
    #function for drawing health bar
    def draw_hp(self):
      
        # display the health bar
        bar_scale = 200 // self.health #scales health bar so all equal
        for i in range(self.health): #creates minibars for animation and scaling
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 10) #health bar dimensions
            pygame.draw.rect(screen, red, bar) #draws bar
          
        for i in range(self.current_hp):#creates minibars for animation and scaling
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 10) #health bar dimensions
            pygame.draw.rect(screen, green, bar) #draws bar
    
    #gives invisible rectangle around pokemon (for clicking) 
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
    
#modified from documentation of https://pokeapi.co/api/v2
#for creating move buttons in-game
def create_button(w,h,l,t,text_x,text_y,label):
    
    cursor = pygame.mouse.get_pos()
    button = pygame.Rect(l,t,w,h)
    
    if button.collidepoint(cursor):
        pygame.draw.rect(screen, gold, button)
    else:
        pygame.draw.rect(screen, grey, button)
    
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f'{label}', True, black)
    text_rect = text.get_rect(center=(text_x, text_y))
    screen.blit(text, text_rect)
    
    return button
    

#playable Pokemon 
#can add more using info from https://pokemondb.net/pokedex/game/firered-leafgreen
Squirtle = Pokemon('Squirtle', ['Water'], ['Fire','Water','Ice','Steel'], ['Grass','Electric'], ['Bubblebeam','Shell Smash','Tackle','Hydro Pump'], {'Attack':48,'Defense':65,'Speed':43,'Health':44}, 120, 0, 50)
Charmander = Pokemon('Charmander', ['Fire'], ['Grass','Bug','Ice','Fire','Fairy','Steel'], ['Water','Rock','Ground'], ['Ember','Inferno','Scratch','Dragon Breath'], {'Attack':52,'Defense':43,'Speed':65,'Health':39}, 120, 75, 50)
Bulbasaur = Pokemon('Bulbasaur', ['Grass'], ['Water','Electric','Grass','Fighting','Fairy'], ['Fire','Ice','Flying','Psychic'], ['Vine Whip','Razor Leaf','Tackle','Solar Beam'], {'Attack':49,'Defense':49,'Speed':45,'Health':45}, 120, 150, 50)
Pikachu = Pokemon('Pikachu', ['Electric'], ['Electric','Flying','Steel'], ['Ground'], ['Thunder Shock','Tail Whip','Iron Tail','Thunderbolt'], {'Attack':55,'Defense':40,'Speed':90,'Health':35}, 120, 225, 50)
Psyduck = Pokemon('Psyduck',['Water'], ['Fire','Water','Ice','Steel'], ['Grass','Electric'], ['Scratch','Water Gun','Surf','Hydro Pump'], {'Attack':52,'Defense':48,'Speed':55,'Health':50}, 120, 300, 50)
Magikarp = Pokemon('Magikarp',['Water'], ['Fire','Water','Ice','Steel'], ['Grass','Electric'], ['Splash','Tackle','Flail','Hydro Pump'], {'Attack':90,'Defense':55,'Speed':80,'Health':20}, 120, 385, 50)
Ekans = Pokemon('Ekans', ['Poison'], ['Grass','Fighting','Poision','Bug','Fairy'], ['Ground','Psychic'],['Wrap','Poison Sting','Acid','Bite'],{'Attack':60,'Defense':44,'Speed':55,'Health':35}, 120, 0, 150)
Mankey = Pokemon('Mankey', ['Fighting'], ['Bug','Rock','Dark'], ['Flying','Psycic','Fairy'], ['Scratch','Karate Chop','Cross Chop','Thrash'],{'Attack':80,'Defense':35,'Speed':70,'Health':40}, 120, 75, 150)
Caterpie = Pokemon('Caterpie', ['Bug'], ['Grass','Fighting','Ground'],['Fire','Flying','Rock'], ['String Shot','Tackle','Bug Bite'],{'Attack':30,'Defense':35,'Speed':45,'Health':45}, 120, 155, 150)
Sandshrew = Pokemon('Sandshrew', ['Ground'], ['Electric','Poison','Rock'], ['Water','Grass','Ice'], ['Scratch','Bulldoze','Slash','Earthquake'],{'Attack':75,'Defense':85,'Speed':40,'Health':50}, 120, 225, 150)
Geodude = Pokemon('Geodude', ['Rock','Ground'], ['Normal','Fire','Flying','Rock','Electric','Poison'], ['Water','Grass','Ice','Fighting','Ground','Steel'], ['Tackle','Rock Throw','Earthquake','Stone Edge'],{'Attack':80,'Defense':100,'Speed':20,'Health':40}, 120, 300, 150)
Eevee = Pokemon('Eevee',['Normal'],['Ghost'],['Fighting'],['Tackle','Quick Attack','Bite','Dig'],{'Attack':55,'Defense':50,'Speed':55,'Health':55}, 120, 385, 150)

#list of playable Pokemon
pokemons = [Squirtle,Charmander,Bulbasaur,Pikachu,Psyduck,Magikarp,Ekans,Mankey,Caterpie,Sandshrew,Geodude,Eevee]

#database for move data that game will pull from for calculations
move_dic = { 'Bubblebeam':[65,100,'Water'], 'Shell Smash':[45,95,'Normal'], 'Tackle':[40,100,'Normal'], 'Hydro Pump':[110,80,'Water'], 
            'Ember':[40,100,'Fire'], 'Inferno':[100,50,'Fire'], 'Scratch':[40,100,'Normal'],'Dragon Breath':[60,100,'Dragon'], 
            'Vine Whip':[45,100,'Grass'], 'Razor Leaf':[55,95,'Grass'], 'Solar Beam':[120,100,'Grass'], 
            'Thunder Shock':[40,100,'Electric'], 'Tail Whip':[40,100,'Normal'], 'Iron Tail':[100,75,'Steel'], 
            'Thunderbolt':[90,100,'Electric'], 'Water Gun':[40,100,'Water'],'Surf':[90,100,'Water'], 'Splash':[45,65,'Normal'], 
            'Flail':[60,100,'Normal'], 'Wrap':[15,90,'Normal'], 'Poison Sting':[15,100,'Poison'], 'Acid':[40,100,'Poison'], 
            'Bite':[60,100,'Dark'], 'Karate Chop':[50,100,'Fighting'], 'Cross Chop':[100,80,'Fighting'], 'Thrash':[120,100,'Normal'], 
            'String Shot':[95,40,'Bug'], 'Bug Bite':[60,100,'Bug'], 'Bulldoze':[60,100,'Ground'], 'Slash':[70,100,'Normal'],
            'Earthquake':[100,100,'Ground'], 'Rock Throw':[50,90,'Physical'], 'Stone Edge':[100,80,'Rock'],
            'Quick Attack':[40,100,'Normal'], 'Dig':[80,100,'Ground'] }

#initialize variables needed for game
game_status = 'pokeSelect' #sets game to selection screen
fightready = False #flag: is game ready for fight
button_render = False #flag: are move buttons rendered
turn = '' #turn flag

#messages needed for move feedback
normal_message = '...it was effective'
counter_message = '...it was SUPER effective'
weak_message = '...it wan not very effective'

#start game while not quit
while game_status != 'quit': 
    
    #never ending loop for mouse and keyboard input
    #for loop for every mouse of keyboard 'event'
    for event in pygame.event.get():
        #if event is a keyboard key pressed down
        if event.type == pygame.KEYDOWN:
            #if key is escape key quit game
            if event.key == pygame.K_ESCAPE:
                game_status = 'quit'
                pygame.quit()
                    
        #if event is a mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            #gets coordinates for click
            click = event.pos
            
            #if click occurs during selection screen
            if game_status == 'pokeSelect':
                for i in pokemons:
                    #if click collides with any Pokemon invisible rectangle .get_rect() 
                    if i.get_rect().collidepoint(click):
                        user_pokemon = i #gives user selected character
                        #creates list of pokemon and removes user character for cpu selection
                        cpu_picks = pokemons 
                        cpu_picks.remove(user_pokemon) 
                        
                        #draws user selected pokemon
                        user_pokemon.size = 240
                        user_pokemon.x = 0
                        user_pokemon.y = 250
                        user_pokemon.set_sprite('front_default')
                        user_pokemon.draw()
                        pygame.display.update()
                        
                        #shuffles through Pokemon (display only)
                        for c in range(15): 
                            rd1 = random.randint(0,len(pokemons)-1)
                            cpu_pokemon = pokemons[rd1]
                            cpu_pokemon.size = 240
                            cpu_pokemon.x = 250
                            cpu_pokemon.y = 250
                            cpu_pokemon.set_sprite('front_default')
                            cpu_pokemon.draw()
                            pygame.display.update()
                            time.sleep(0.1)
                            pygame.draw.rect(screen, grey, cpu_pokemon.get_rect())
                            pygame.display.update()
                            cpu_pokemon.x = 1000 #throws pokemon away
                            cpu_pokemon.y = 1000 #throws pokemon away
                        
                        #actually selects Pokemon for cpu
                        rd2 = random.randint(0,len(cpu_picks)-1) #random int
                        cpu_pokemon = cpu_picks[rd2] #cpu picks random char from list
                        #draws cpu pick
                        cpu_pokemon.size = 240
                        cpu_pokemon.x = 250
                        cpu_pokemon.y = 250
                        cpu_pokemon.set_sprite('front_default')
                        #changes fight sign to green
                        pygame.draw.rect(screen, grey, pygame.Rect(250, 250, 50, 50))
                        cpu_pokemon.draw()
                        pygame.display.update()
                        fightready = True #flag: game is now fight ready
            #if click occurs during battle phsae
            elif game_status == 'battle':
                #if during player turn
                if turn == 'player': 
                    #clicking move will move to player move screen
                    if attack_button.collidepoint(click):
                        turn = 'player_move'
                    #if click potion you will heal
                    if heal_button.collidepoint(click):
                        player_heals = player_heals - 1
                        heal_text = font2.render(user_pokemon.heal_message(), True, black) #for rendering text
                        screen.blit(heal_text, (game_message_box_2.x,game_message_box_2.y)) #display text
                        pygame.display.update()
                        time.sleep(1)
                        #loop to animate health bar and to prevent over-heal
                        for i in range(player_healing):
                            if user_pokemon.current_hp == user_pokemon.health:
                                pass
                            user_pokemon.current_hp += 1
                            user_pokemon.draw_hp()
                            time.sleep(0.02)
                            pygame.display.update()
                        
                        turn = 'cpu' #switch to cpu turn
                #if click occurs on player move screen and buttons are rendered
                if (turn == 'player_move' and button_render == True):
                    #for loop for each move
                    for i in range(len(move_buttons)):
                        button = move_buttons[i]
                        #get which button was clicked
                        if button.collidepoint(click):
                            move_choice = user_pokemon.moves[i] #get move from pokemon move list
                            move = move_dic[move_choice] #get data for move from database
                            hit = random.randrange(0,100,1) #value to see if attack misses
                            if (hit <= move[1]): #if attack hits
                                move_text = font2.render(user_pokemon.move_message(move_choice), True, black) #render text
                                screen.blit(move_text, (game_message_box_1.x,game_message_box_1.y)) #display text
                                pygame.display.update()
                                time.sleep(1)
                                #if move type is cpu weakness
                                if move[2] in cpu_pokemon.weak:
                                    damage = int(round(move[0]*((user_pokemon.attack*2)/(cpu_pokemon.defense*0.5))/10)) #calculate damage
                                    damage_text = font2.render(counter_message, True, black) #render text
                                    screen.blit(damage_text, (game_message_box_2.x,game_message_box_2.y)) #display text
                                    pygame.display.update()
                                    time.sleep(1)
                                #if move type is cpu strength 
                                if move[2] in cpu_pokemon.strong:
                                    damage = int(round((move[0]*((user_pokemon.attack*0.5)/(cpu_pokemon.defense*2)))/10))
                                    damage_text = font2.render(weak_message, True, black)
                                    screen.blit(damage_text, (game_message_box_2.x,game_message_box_2.y))
                                    pygame.display.update()
                                    time.sleep(1)
                                #if move time is neither cpu strength nor weakness
                                if (move[2] not in cpu_pokemon.weak and move[2] not in cpu_pokemon.strong):
                                    damage = int(round((move[0]*(user_pokemon.attack/cpu_pokemon.defense))/10))
                                    damage_text = font2.render(normal_message, True, black)
                                    screen.blit(damage_text, (game_message_box_2.x,game_message_box_2.y))
                                    pygame.display.update()
                                    time.sleep(1)
                                #animate damage in health bar
                                for i in range(damage):
                                    cpu_pokemon.current_hp -= 1
                                    cpu_pokemon.draw_hp()
                                    time.sleep(0.02)
                                    pygame.display.update()
                                    #if the Pokemon reaches zero health, game over
                                    if cpu_pokemon.current_hp <= 0:
                                        game_status = 'game over'
                            #if the attck misses display message
                            else:
                                missed_text = font2.render(user_pokemon.miss_message(), True, black)
                                screen.blit(missed_text, (game_message_box_2.x,game_message_box_2.y))
                                pygame.display.update()
                                time.sleep(1)
                        #fill screeen and redraw everything to delete messages
                        screen.fill(grey)
                        user_pokemon.draw()
                        cpu_pokemon.draw()
                        user_pokemon.draw_hp()
                        cpu_pokemon.draw_hp()
                        
                        turn = 'cpu' #switch to cpu turn
                        button_render = False #flag: move buttons no longer rendered
                        

    #selection screen
    if game_status == 'pokeSelect':
        screen.fill(grey)
        #draw all playable pokemon
        for i in pokemons:
            i.draw() 
        #if fight is not ready, fight sign = red
        if fightready == False:
            start_button = pygame.Rect(200,10,90,40)
            pygame.draw.rect(screen, red, start_button)
            start_txt = font.render('Fight', True, grey)
            screen.blit(start_txt, (205,15))
            pygame.display.update()
        #if game is fight ready
        if fightready == True:
            pygame.draw.rect(screen, (0,200,0), pygame.Rect(200,10,90,40)) #change sign to green
            start_txt = font.render('Fight', True, black)
            screen.blit(start_txt, (205,15))
            for i in pokemons:
                i.draw()
            user_pokemon.draw()
            cpu_pokemon.draw()
            pygame.display.update()
            time.sleep(2)
            game_status = 'pre-battle' #start pre-battle phase
            
        
    
    #pre-battle phase
    if game_status == 'pre-battle':
        #fill screen and redraw everything, and move Pokemon to proper places
        screen.fill(grey)
        user_pokemon.set_sprite('back_default') #face user Pokemon away from user
        user_pokemon.size = 300
        user_pokemon.x = 0
        user_pokemon.hp_x = 200
        user_pokemon.y = 300
        user_pokemon.hp_y = 325
        user_pokemon.draw_hp()
        cpu_pokemon.size = 200
        cpu_pokemon.x = 250
        cpu_pokemon.hp_x = 40
        cpu_pokemon.y = 0
        cpu_pokemon.hp_y = 20
        cpu_pokemon.draw_hp()
        alph = 0
        #fade in Pokemon by changing alpha value
        while alph < 255:
            user_pokemon.draw(alph)
            cpu_pokemon.draw(alph)
            alph += 0.5
            pygame.display.update()
    
        #give each player 3 heals
        player_heals = 3
        cpu_heals = 3
        
        cpu_moves = cpu_pokemon.moves
        #calculate potion strengths
        player_healing = int(round(0.2*user_pokemon.health,0))
        cpu_healing = int(round(0.2*cpu_pokemon.health,0))
        #create text boxes for in game text
        game_message_box_1 = pygame.Rect(20, 190, 225, 35)
        game_message_box_2 = pygame.Rect(20, 225, 225, 35)
        
        #player that has Pokemon with greater EVs['speed'] starts, can use a turn object to flip between user (1) and cpu (2)
        if(user_pokemon.speed > cpu_pokemon.speed):
            turn = 'player'
        else:
            turn = 'cpu'
        pygame.display.update()
        
        game_status = 'battle'
    #game start, continue while both still have health
    if game_status == 'battle': 
        
        #if user turn
        if turn == 'player':
            #redraw everything to delete text
            screen.fill(grey)
            user_pokemon.draw()
            cpu_pokemon.draw()
            user_pokemon.draw_hp()
            cpu_pokemon.draw_hp()
            #create attack and heal buttons (if player has heals left)
            attack_button = create_button(60, 20, 220, 450, 250, 460, 'Move')
            if(player_heals > 0):
                heal_button = create_button(60, 20, 300, 450, 330, 460, 'Potion')
            pygame.display.update()
        #if player selected to move/attack
        if turn == 'player_move':
            move_buttons = []
            #loop to draw buttons for each move
            for i in range(len(user_pokemon.moves)):
                move = user_pokemon.moves[i]
                button_width = 240
                button_height = 70
                left = 10 + i % 2 * button_width
                top = 350 + i // 2 * button_height
                text_center_x = left + 120
                text_center_y = top + 35
                button = create_button(button_width, button_height, left, top, text_center_x, text_center_y, str(move))
                move_buttons.append(button)
            pygame.display.update()
            button_render = True #flag: buttons are rendered
        
        #if cpu turn
        if turn == 'cpu':
            time.sleep(1)
            #redraw everything
            screen.fill(grey)
            user_pokemon.draw()
            cpu_pokemon.draw()
            user_pokemon.draw_hp()
            cpu_pokemon.draw_hp()
            pygame.display.update()
            #if cpu health > 25% then heal
            if(cpu_pokemon.current_hp <= (0.25*cpu_pokemon.health and cpu_heals > 0)):
                cpu_heals = cpu_heals - 1
                heal_text = font2.render(cpu_pokemon.heal_message(), True, black)
                screen.blit(heal_text, (game_message_box_2.x,game_message_box_2.y))
                pygame.display.update()
                #animate heal on health bar
                for i in range(player_healing):
                    if cpu_pokemon.current_hp == cpu_pokemon.health:
                        pass
                    cpu_pokemon.current_hp += 1
                    cpu_pokemon.draw_hp()
                    time.sleep(0.02)
                    pygame.display.update()
                time.sleep(1)
                
            #else attack
            else:
                move_choice = cpu_moves[random.randrange(0,len(cpu_moves)-1,1)]
                cpu_attack = move_dic[move_choice]
                hit = random.randrange(0,100,1)
                if(hit <= cpu_attack[1]):
                    move_text = font2.render(cpu_pokemon.move_message(move_choice), True, black)
                    screen.blit(move_text, (game_message_box_1.x,game_message_box_1.y))
                    pygame.display.update()
                    time.sleep(1)
                    if cpu_attack[2] in user_pokemon.weak:
                        damage = int(round(cpu_attack[0]*((cpu_pokemon.attack*2)/(user_pokemon.defense*0.5))/10))
                        damage_text = font2.render(counter_message, True, black)
                        screen.blit(damage_text, (game_message_box_2.x,game_message_box_2.y))
                        pygame.display.update()
                        time.sleep(1)
                    if cpu_attack[2] in user_pokemon.strong:
                        damage = int(round((cpu_attack[0]*((cpu_pokemon.attack*0.5)/(user_pokemon.defense*2)))/10))
                        damage_text = font2.render(weak_message, True, black)
                        screen.blit(damage_text, (game_message_box_2.x,game_message_box_2.y))
                        pygame.display.update()
                        time.sleep(1)
                    if (cpu_attack[2] not in user_pokemon.weak and cpu_attack[2] not in user_pokemon.strong):
                        damage = int(round((cpu_attack[0]*(cpu_pokemon.attack/user_pokemon.defense))/10))
                        damage_text = font2.render(normal_message, True, black)
                        screen.blit(damage_text, (game_message_box_2.x,game_message_box_2.y))
                        pygame.display.update()
                        time.sleep(1)
                        
                    for i in range(damage):
                        user_pokemon.current_hp -= 1
                        user_pokemon.draw_hp()
                        time.sleep(0.02)
                        pygame.display.update()    
                        if user_pokemon.current_hp <= 0:
                            game_status = 'game over'
                else:
                    missed_text = font2.render(cpu_pokemon.miss_message(), True, black)
                    screen.blit(missed_text, (game_message_box_2.x,game_message_box_2.y))
                    pygame.display.update()
                    time.sleep(1)
            #switch to player turn
            turn = 'player'
    #if game over
    if game_status == 'game over':
        #redraw everything to delete any text
        screen.fill(grey)
        user_pokemon.draw()
        cpu_pokemon.draw()
        user_pokemon.draw_hp()
        cpu_pokemon.draw_hp()
        pygame.display.update()
        #if user won diplay user win cpu lose text
        if user_pokemon.current_hp > 0:   
            win_text = font2.render(user_pokemon.win_message(), True, black)
            lose_text = font2.render(cpu_pokemon.lose_message(), True, black)
            screen.blit(win_text, (game_message_box_2.x,game_message_box_2.y))
            pygame.display.update()
            screen.blit(lose_text, (game_message_box_1.x,game_message_box_1.y))
            pygame.display.update()
            time.sleep(5)
        #if cpu won display cpu win player lose text
        elif cpu_pokemon.current_hp > 0:
            win_text = font2.render(cpu_pokemon.win_message(), True, black)
            lose_text = font2.render(user_pokemon.lose_message(), True, black)
            screen.blit(win_text, (game_message_box_2.x,game_message_box_2.y))
            pygame.display.update()
            screen.blit(lose_text, (game_message_box_1.x,game_message_box_1.y))
            time.sleep(5)

        
