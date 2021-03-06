import sys

import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes
# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution

def pause_menu():
   stddraw.setFontSize(35)
   stddraw.setPenColor(Color(0, 0, 0))
   stddraw.boldText(6, 10, "Click to Resume")
   while True:
      stddraw.show(50)
      if stddraw.mousePressed():
         break
   return

def start():
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 18
   # set the size of the drawing canvas
   canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
   stddraw.setCanvasSize(canvas_w, canvas_h) 
   # set the scale of the coordinate system
   stddraw.setXscale(-0.5, grid_w - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w - 6
   
   # create the game grid
   grid = GameGrid(grid_h, grid_w - 6)
   # create the first tetromino to enter the game grid 
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino(grid_h, grid_w - 6)
   grid.current_tetromino = current_tetromino

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w)
   has_next = 0
   score = 0
   # the main game loop (keyboard interaction for moving the tetromino) 
   while True:
      # Used to pause the game
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has
         # most recently been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= 15 and mouse_x <= 17:
            if mouse_y >= 18.5 and mouse_y <= 19.5:
               pause_menu()
      # Create tetromino that will be used to show next piece
      if(has_next == 0):
         next_tetromino = create_tetromino(grid_h, grid_w - 6)
         has_next += 1
      # check user interactions via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
            current_tetromino.didUpdate = 1
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
            current_tetromino.didUpdate = 1
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one 
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)

         elif key_typed == "space":
            # hard drop, piece will fall until it can't
            while(current_tetromino.move(key_typed, grid)):
               current_tetromino.move(key_typed, grid)





         elif key_typed == "r":

            #rotate the active tetromino in clockwise
            if (current_tetromino.type == "O"):
               nums = []#scans the tile matrix and appends numbers on each tile
               for row in current_tetromino.tile_matrix:
                  for col in row:
                     if not (col == None):
                        nums.append(col.number)

               current_tetromino.turn(grid)
               current_tetromino.tile_matrix[0][0].number = nums[2]
               current_tetromino.tile_matrix[0][1].number = nums[0]
               current_tetromino.tile_matrix[1][0].number = nums[3]
               current_tetromino.tile_matrix[1][1].number = nums[1]
            for row in current_tetromino.tile_matrix:
               for col in row:
                  if not (col == None):
                     if (col.number == 2):
                        col.background_color = Color(238, 238, 218)
                     elif (col.number == 4):
                        col.background_color = Color(237, 224, 200)

            if ( current_tetromino.type == "S"):
               if (current_tetromino.notTurn == 1):
                  nums = []
                  for row in current_tetromino.tile_matrix:
                     for col in row:
                        if not (col == None):
                           nums.append(col.number)
               current_tetromino.turn(grid)
               if (current_tetromino.turnType == 0):
                  current_tetromino.tile_matrix[0][1].number = nums[0]
                  current_tetromino.tile_matrix[0][2].number = nums[1]
                  current_tetromino.tile_matrix[1][0].number = nums[2]
                  current_tetromino.tile_matrix[1][1].number = nums[3]
               elif (current_tetromino.turnType == 1):
                  current_tetromino.tile_matrix[1][2].number = nums[0]
                  current_tetromino.tile_matrix[2][2].number = nums[1]
                  current_tetromino.tile_matrix[0][1].number = nums[2]
                  current_tetromino.tile_matrix[1][1].number = nums[3]
               elif (current_tetromino.turnType == 2):
                  current_tetromino.tile_matrix[2][1].number = nums[0]
                  current_tetromino.tile_matrix[2][0].number = nums[1]
                  current_tetromino.tile_matrix[1][2].number = nums[2]
                  current_tetromino.tile_matrix[1][1].number = nums[3]
               elif (current_tetromino.turnType == 3):
                  current_tetromino.tile_matrix[1][0].number = nums[0]
                  current_tetromino.tile_matrix[0][0].number = nums[1]
                  current_tetromino.tile_matrix[2][1].number = nums[2]
                  current_tetromino.tile_matrix[1][1].number = nums[3]
               for row in current_tetromino.tile_matrix:
                  for col in row:
                     if not (col == None):
                        if (col.number == 2):
                           col.background_color = Color(238, 238, 218)
                        elif (col.number == 4):
                           col.background_color = Color(237, 224, 200)

            if ( current_tetromino.type == "T"):
               if (current_tetromino.notTurn == 1):
                  nums = []
                  for row in current_tetromino.tile_matrix:
                     for col in row:
                        if not (col == None):
                           nums.append(col.number)
               current_tetromino.turn(grid)
               if (current_tetromino.turnType == 0):
                  current_tetromino.tile_matrix[1][0].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[1][2].number = nums[2]
                  current_tetromino.tile_matrix[2][1].number = nums[3]
               elif (current_tetromino.turnType == 1):
                  current_tetromino.tile_matrix[0][1].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[2][1].number = nums[2]
                  current_tetromino.tile_matrix[1][0].number = nums[3]
               elif (current_tetromino.turnType == 2):
                  current_tetromino.tile_matrix[1][2].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[1][0].number = nums[2]
                  current_tetromino.tile_matrix[0][1].number = nums[3]
               elif (current_tetromino.turnType == 3):
                  current_tetromino.tile_matrix[2][1].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[0][1].number = nums[2]
                  current_tetromino.tile_matrix[1][2].number = nums[3]
               for row in current_tetromino.tile_matrix:
                  for col in row:
                     if not (col == None):
                        if (col.number == 2):
                           col.background_color = Color(238, 238, 218)
                        elif (col.number == 4):
                           col.background_color = Color(237, 224, 200)

            if ( current_tetromino.type == "I"):
               if (current_tetromino.notTurn == 1):
                  nums = []
                  for row in current_tetromino.tile_matrix:
                     for col in row:
                        if not (col == None):
                           nums.append(col.number)
               current_tetromino.turn(grid)
               if (current_tetromino.turnType == 0):
                  current_tetromino.tile_matrix[0][1].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[2][1].number = nums[2]
                  current_tetromino.tile_matrix[3][1].number = nums[3]
               elif (current_tetromino.turnType == 1):
                  current_tetromino.tile_matrix[1][3].number = nums[0]
                  current_tetromino.tile_matrix[1][2].number = nums[1]
                  current_tetromino.tile_matrix[1][1].number = nums[2]
                  current_tetromino.tile_matrix[1][0].number = nums[3]
               elif (current_tetromino.turnType == 2):
                  current_tetromino.tile_matrix[3][2].number = nums[0]
                  current_tetromino.tile_matrix[2][2].number = nums[1]
                  current_tetromino.tile_matrix[1][2].number = nums[2]
                  current_tetromino.tile_matrix[0][2].number = nums[3]
               elif (current_tetromino.turnType == 3):
                  current_tetromino.tile_matrix[2][0].number = nums[0]
                  current_tetromino.tile_matrix[2][1].number = nums[1]
                  current_tetromino.tile_matrix[2][2].number = nums[2]
                  current_tetromino.tile_matrix[2][3].number = nums[3]
               for row in current_tetromino.tile_matrix:
                  for col in row:
                     if not (col == None):
                        if (col.number == 2):
                           col.background_color = Color(238, 238, 218)
                        elif (col.number == 4):
                           col.background_color = Color(237, 224, 200)

            if ( current_tetromino.type == "L"):
               if (current_tetromino.notTurn == 1):
                  nums = []
                  for row in current_tetromino.tile_matrix:
                     for col in row:
                        if not (col == None):
                           nums.append(col.number)
               current_tetromino.turn(grid)
               if (current_tetromino.turnType == 0):
                  current_tetromino.tile_matrix[0][1].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[2][1].number = nums[2]
                  current_tetromino.tile_matrix[2][2].number = nums[3]
               elif (current_tetromino.turnType == 1):
                  current_tetromino.tile_matrix[1][2].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[1][0].number = nums[2]
                  current_tetromino.tile_matrix[2][0].number = nums[3]
               elif (current_tetromino.turnType == 2):
                  current_tetromino.tile_matrix[2][1].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[0][1].number = nums[2]
                  current_tetromino.tile_matrix[0][0].number = nums[3]
               elif (current_tetromino.turnType == 3):
                  current_tetromino.tile_matrix[1][0].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[1][2].number = nums[2]
                  current_tetromino.tile_matrix[0][2].number = nums[3]
               for row in current_tetromino.tile_matrix:
                  for col in row:
                     if not (col == None):
                        if (col.number == 2):
                           col.background_color = Color(238, 238, 218)
                        elif (col.number == 4):
                           col.background_color = Color(237, 224, 200)

            if ( current_tetromino.type == "J"):
               if (current_tetromino.notTurn == 1):
                  nums = []
                  for row in current_tetromino.tile_matrix:
                     for col in row:
                        if not (col == None):
                           nums.append(col.number)
               current_tetromino.turn(grid)
               if (current_tetromino.turnType == 0):
                  current_tetromino.tile_matrix[0][1].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[2][0].number = nums[2]
                  current_tetromino.tile_matrix[2][1].number = nums[3]
               elif (current_tetromino.turnType == 1):
                  current_tetromino.tile_matrix[1][2].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[0][0].number = nums[2]
                  current_tetromino.tile_matrix[1][0].number = nums[3]
               elif (current_tetromino.turnType == 2):
                  current_tetromino.tile_matrix[2][1].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[0][2].number = nums[2]
                  current_tetromino.tile_matrix[0][1].number = nums[3]
               elif (current_tetromino.turnType == 3):
                  current_tetromino.tile_matrix[1][0].number = nums[0]
                  current_tetromino.tile_matrix[1][1].number = nums[1]
                  current_tetromino.tile_matrix[2][2].number = nums[2]
                  current_tetromino.tile_matrix[1][2].number = nums[3]
               for row in current_tetromino.tile_matrix:
                  for col in row:
                     if not (col == None):
                        if (col.number == 2):
                           col.background_color = Color(238, 238, 218)
                        elif (col.number == 4):
                           col.background_color = Color(237, 224, 200)

            if ( current_tetromino.type == "Z"):
               if (current_tetromino.notTurn == 1):
                  nums = []
                  for row in current_tetromino.tile_matrix:
                     for col in row:
                        if not (col == None):
                           nums.append(col.number)
               current_tetromino.turn(grid)
               if (current_tetromino.turnType == 0):
                  current_tetromino.tile_matrix[0][0].number = nums[0]
                  current_tetromino.tile_matrix[0][1].number = nums[1]
                  current_tetromino.tile_matrix[1][1].number = nums[2]
                  current_tetromino.tile_matrix[1][2].number = nums[3]
               elif (current_tetromino.turnType == 1):
                  current_tetromino.tile_matrix[0][2].number = nums[0]
                  current_tetromino.tile_matrix[1][2].number = nums[1]
                  current_tetromino.tile_matrix[1][1].number = nums[2]
                  current_tetromino.tile_matrix[2][1].number = nums[3]
               elif (current_tetromino.turnType == 2):
                  current_tetromino.tile_matrix[2][2].number = nums[0]
                  current_tetromino.tile_matrix[2][1].number = nums[1]
                  current_tetromino.tile_matrix[1][1].number = nums[2]
                  current_tetromino.tile_matrix[1][0].number = nums[3]
               elif (current_tetromino.turnType == 3):
                  current_tetromino.tile_matrix[2][0].number = nums[0]
                  current_tetromino.tile_matrix[1][0].number = nums[1]
                  current_tetromino.tile_matrix[1][1].number = nums[2]
                  current_tetromino.tile_matrix[0][1].number = nums[3]
               for row in current_tetromino.tile_matrix:
                  for col in row:
                     if not (col == None):
                        if (col.number == 2):
                           col.background_color = Color(238, 238, 218)
                        elif (col.number == 4):
                           col.background_color = Color(237, 224, 200)


         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)

      score = grid.checkColumns(grid.tile_matrix, score) # add same tiles, move columns, change colors, update score
      score = grid.elimGaps(grid.tile_matrix, score) # removing isolated tiles, update score
      score = grid.checkRows(grid.tile_matrix, score) # remove filled rows, move rows down, update score

      # place the active tetromino on the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            return score
         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         current_tetromino = Tetromino(next_tetromino.type)
         current_tetromino.tile_matrix = next_tetromino.tile_matrix
         has_next -= 1
         grid.current_tetromino = current_tetromino

      # display the game grid and the current tetromino
      grid.display(next_tetromino,score)


   # print a message on the console when the game is over
   print("Game over")

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   tetromino_types = ['S', 'O', 'T', 'I', 'L', 'J', 'Z']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_width - 1.5, 2
   # coordinates of the bottom left corner of the start game button 
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has 
         # most recently been left-clicked  
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h: 
               break # break the loop to end the method and start the game

# Game over menu
def display_game_over(score):
   grid_height, grid_width = 20, 18
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # colors used for the menu
   background_color = Color(206,192,181)
   button_color = Color(140,132,124)
   text_color = Color(255,215,0)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   button_w, button_h = grid_width - 1.5, 2
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   stddraw.setPenColor(Color(245,149,99))
   stddraw.setPenRadius(0.04)
   stddraw.rectangle(-0.5, -0.5, grid_width, grid_height)
   stddraw.setPenRadius()
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(65)
   stddraw.setPenColor(Color(245,149,99))
   stddraw.boldText(img_center_x, 15, "Game Over")
   stddraw.setFontSize(45)
   stddraw.setPenColor(text_color)
   scoretxt = "Score: " + str(score)
   stddraw.boldText(img_center_x, 10, scoretxt)
   stddraw.text(img_center_x, 5, "Restart")
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has
         # most recently been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game
   return

# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__== '__main__':
   sys.setrecursionlimit(10000)
   while True:
       score = start()
       display_game_over(score)