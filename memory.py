import pygame, random

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 

   # 1 create the window
   # display the window
   # get surface of the window
   # use the play method
   # use the quit method
   # User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object
      # comes in existance with 6 instance attributes
      # === objects that are part of every game that we will discuss
      self.bg_color = pygame.Color('black')
      self.surface = surface
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.board_size = 4
      self.image_list = []
      self.score = 0
      self.board = [] # will be represented by a list of lists
      self.tile1_selected = None
      self.tile2_selected = None
      self.create_board()

   def load_image(self):
      # load the images by using a for loop and appending the images into the an empty list
      self.image_list = []
      for i in range(1,9):
         self.image_list.append(pygame.image.load('image'+str(i)+'.bmp'))
      return self.image_list
   
   def create_board(self):
      # create_board is the method to form the basic grid like TTT and filling that with images.
      self.load_image()
      double_list = self.image_list+self.image_list
      random.shuffle(double_list)
      width = self.image_list[0].get_width()
      height = self.image_list[0].get_height()  # taking the width and height of an image appended in an empty list
      for i in range(self.board_size):
         row = []
         for k in range(self.board_size):
            x = k*width
            y = i*height
            self.image = double_list[i*self.board_size + k]
            tile = Tile(x,y,width, height, self.image, self.surface)  # using the Tile class for making an tile containg the images.
            row.append(tile)
         self.board.append(row)

   def play(self):
      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()   # line 82 to line 87 would remain same as per pre-poke framework 
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def play_game(self, position): 
       # This method in Game Class shows how the game starts and flips the tille
        for row in self.board:
            for tile in row:
                if tile.select_expose(position): # taking a select_expose from the Tile class.
                  if self.tile1_selected == None:         
                        tile.pairs_of_tiles(True)  # taking pairs_of_tiles method from Tile class
                        self.tile1_selected = [self.board.index(row), row.index(tile)] #conatins details about rows and column for tile 1 
                  else:
                        tile.pairs_of_tiles(True)
                        self.tile2_selected = [self.board.index(row), row.index(tile)] #for tile 2

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
               self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONUP:  # one of the event of pygame used for clicking
               self.play_game(event.pos)

   def returning_question_mark_image(self):
        # If the 2 clicked tiles flip and they aren't the same images. 
        # That tile will flip into 'image0.bmp'
         if self.tile1_selected != None and self.tile2_selected != None:
            if not self.board[self.tile1_selected[0]][self.tile1_selected[1]].matching_images(self.board[self.tile2_selected[0]][self.tile2_selected[1]]):
                pygame.time.delay(1000) # Delays the tiles from, flipping into 'image0.bmp' when 2 clicked images aren't same.
                self.board[self.tile1_selected[0]][self.tile1_selected[1]].pairs_of_tiles(False)
                self.board[self.tile2_selected[0]][self.tile2_selected[1]].pairs_of_tiles(False)
            
            self.tile1_selected = None
            self.tile2_selected = None  

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      self.surface.fill('black') # clear the display surface first
      for row in self.board:
         for tile in row:
            tile.draw() # tile is taken from Tile class
      self.draw_score([445,0], self.score)  # co-ordinates of position where we are going to place the timer/clock
      pygame.display.update() # make the updated surface appear on the display

   def draw_score(self, position, score):
      # draws the score as the timer 
         self.position = position
         score_color = pygame.Color('white') # color of the time
         score_display = str(score) # converting the time.clicks into an string so we can concatinate it!
         font = pygame.font.SysFont('Roman', 50) #for size and font of the score.
         font_image = font.render(score_display,True,score_color) #rendering the font created by using above function with pygame.
         self.surface.blit(font_image,self.position)
   
   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      self.score = pygame.time.get_ticks()//1000 # pygame function for timer.
      self.returning_question_mark_image()
   
   def decide_continue(self):
      tile_exposed_counter = 0  # counter for an each tile.  Hint:- Taken from SLACK.
      for row in self.board:
         for self.tile in row:  # same nested loops made in the starting of the code
               if self.tile.exposed_tile == True: # if the tile exposed is true that is when we click the tile it switches in to the image.
                  tile_exposed_counter += 1 # when we click the tile and its tile converts to images.bmp except image0.bmp. it will add 1
      if tile_exposed_counter == 16:
         self.continue_game = False # game will stop working
        


class Tile: 

   def __init__(self,x,y,width,height,image_expose,surface): 
      self.rect = pygame.Rect(x,y,width,height)
      self.color = pygame.Color('black')
      self.border_width = 5
      self.image_hidden = pygame.image.load("image0.bmp") # load the image of the question mark
      self.image_expose = image_expose  # All taken from TTT
      self.exposed_tile = False # initially no tile is exposed.
      self.surface = surface
      
   def select_expose(self,position):
      if self.rect.collidepoint(position): # using collidepoint to check if the click is inside the tile or not
            if not self.exposed_tile:
                return True
            else:
                return False 
   
   def draw(self):
      pygame.draw.rect(self.surface,self.color,self.rect, self.border_width)
      location = (self.rect.x, self.rect.y) # gievs the lovcation of teh rectangeles and we takle the co-ordinates.
      image_exposed = self.image_expose
      self.surface.blit(self.image_hidden, location)
      if self.exposed_tile == True: # we click the tile and exposed_tile becomes true.
         self.surface.blit(image_exposed, self.rect)
      else:
         self.surface.blit(self.image_hidden, location) # if exposed_tile is false
      pygame.draw.rect(self.surface,self.color,self.rect, self.border_width)
   
   def pairs_of_tiles(self, exposing_image): # This funtion extends the functionality which tells that 2 tiles remain exposed if they match
        self.exposed_tile = exposing_image

   def matching_images(self, other_tile): # This funtion tells if the two selected tiles clicked match or not
        return (self.image_expose == other_tile.return_image())  
   
   def return_image(self): # created this funtion because in line 188 i can't use self.
        return self.image_expose     

main()