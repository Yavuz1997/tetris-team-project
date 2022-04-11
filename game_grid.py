import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing

# Class used for modelling the game grid
class GameGrid:
	# Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles landed onto the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(206,192,181)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(140,132,124)
      self.boundary_color = Color(245,149,99)
      # thickness values used for the grid lines and the boundaries
      self.line_thickness = 0.002
      self.box_thickness = 5 * self.line_thickness

   # Method used for displaying the game grid
   def display(self, next_tetromino,score):
      # clear the background to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_grid()
      stddraw.setPenColor(Color(242,203,155))
      stddraw.filledRectangle(11.5,-0.5,6,20) # UI background
      stddraw.setPenColor(Color(237, 197, 63))
      stddraw.filledRectangle(15, 18.5, 2, 0.85) # Pause botton background
      stddraw.setPenColor(Color(245, 149, 99))
      stddraw.setPenColor(Color(245, 149, 99))
      stddraw.setFontSize(25)
      stddraw.boldText(16, 19, "Pause")
      stddraw.boldText(14.5, 7, "Next Piece :")
      stddraw.boldText(12.6, 18, "Score :")
      stddraw.boldText(14.5, 16, "Controls")
      stddraw.boldText(14.5, 15.7, "------------------")
      stddraw.setFontSize(20)
      stddraw.boldText(14.6, 15, "Left Arrow : Left")
      stddraw.boldText(14.6, 14, "Right Arrow : Right")
      stddraw.boldText(14.6, 13, "Down Arrow : Down")
      stddraw.boldText(14.6, 12, "Space : Hard Drop")
      stddraw.boldText(14.6, 11, "R : Clockwise Rotation")
      stddraw.setPenColor(Color(246,94,59))
      stddraw.boldText(14.5, 18, str(score))
      next_tetromino.bottom_left_cell.x = 13.5
      if not(next_tetromino.type == 'I'):
         next_tetromino.bottom_left_cell.y = 3.5
      else:
         next_tetromino.bottom_left_cell.y = 2.5
      next_tetromino.draw()
      # draw the current/active tetromino if it is not None (the case when the 
      # game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
      # draw a box around the game grid 
      self.draw_boundaries()
      # show the resulting drawing with a pause duration = 250 ms
      stddraw.show(250)
         
   # Method for drawing the cells and the lines of the game grid
   def draw_grid(self):
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # draw the tile if the grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].draw(Point(col, row))
      # draw the inner lines of the grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value            
      
   # Method for drawing the boundaries around the game grid 
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible 
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # Method used for checking whether the grid cell with given row and column 
   # indexes is occupied by a tile or empty
   def is_occupied(self, row, col):
      # considering newly entered tetrominoes to the game grid that may have 
      # tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None
      
   # Method used for checking whether the cell with given row and column indexes 
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # Method that locks the tiles of the landed tetromino on the game grid while
   # checking if the game is over due to having tiles above the topmost grid row.
   # The method returns True when the game is over and False otherwise.
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the game grid 
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):            
            # place each tile onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True
      # return the game_over flag
      return self.game_over

   # Method method that checks columns and adds same numbers, moves the rows when theres a summation
   # and changes tile colors with the summation
   def checkColumns(self, tile_matrix, score):
      for column in tile_matrix.T: # transpose matrix to iterate trough columns
         for tileIndex, tile in enumerate(column): # go trough each tile that is occupied
            if (tileIndex+1 > 19):
               continue
            if not (tile == None or column[tileIndex + 1] == None):
               if (tile.number == column[tileIndex + 1].number):
                  score += tile.number
                  score += column[tileIndex + 1].number
                  tile.number += column[tileIndex + 1].number # Add tile numbers
                  if (tile.number == 4):  # Change tile colours with the values
                     tile.background_color = Color(237, 224, 200)
                  elif(tile.number == 8):   # Change tile colours with the values
                     tile.background_color = Color(242, 177, 121)
                  elif(tile.number == 16):
                     tile.background_color = Color(245, 149, 99)
                  elif(tile.number == 32):
                     tile.background_color = Color(246, 124, 95)
                  elif(tile.number == 64):
                     tile.background_color = Color(246, 94, 59)
                  elif(tile.number == 128):
                     tile.background_color = Color(237, 207, 114)
                  elif(tile.number == 256):
                     tile.background_color = Color(237, 204, 97)
                  elif(tile.number == 512):
                     tile.background_color = Color(237, 200, 80)
                  elif(tile.number == 1024):
                     tile.background_color = Color(237, 197, 63)
                  elif(tile.number > 1024):
                     tile.background_color = Color(237, 194, 46)
                  column[tileIndex + 1] = None # Consume the tile
                  for x in column: # Move column down by 1
                     if(tileIndex + 2 > 19):
                        break
                     column[tileIndex + 1] = column[tileIndex + 2]
                     tileIndex += 1
                  score = self.checkColumns(tile_matrix, score) # Check the grid again
                  return score
      return score

   # Method that checks rows from bottom up, if it finds a row without empty space
   # delete the tiles, move all rows above the deleted tiles down by 1
   def checkRows(self, tile_matrix, score):
      for rowIndex, row in enumerate(tile_matrix):
         if None not in row:
            for columnIndex, val in enumerate(row):
               score += val.number
               row[columnIndex] = None
            for j, x in enumerate(tile_matrix):
               j += rowIndex
               if (j == 18):
                  break
               tile_matrix[j] = tile_matrix[j + 1]
      return score

   # Method that checks tiles and deletes the tiles if they are isolated / not directly touching another tetromino
   def elimGaps(self, tile_matrix, score):
      for rowIndex, row in enumerate(tile_matrix):
         if (rowIndex == 0):
            continue
         for colIndex, col in enumerate(row):
            if (tile_matrix[rowIndex - 1][colIndex] == None and not (col == None)):
               if (colIndex == 0):  # Leftmost side
                  if (tile_matrix[rowIndex][colIndex + 1] == None):
                     score += col.number
                     tile_matrix[rowIndex][colIndex] = None
                  elif (not (tile_matrix[rowIndex][colIndex + 1] == None) and tile_matrix[rowIndex - 1][
                     colIndex + 1] == None and tile_matrix[rowIndex][colIndex + 2] == None):
                     score += col.number
                     score += tile_matrix[rowIndex][colIndex + 1].number
                     tile_matrix[rowIndex][colIndex] = None
                     tile_matrix[rowIndex][colIndex + 1] = None
                  elif (not (tile_matrix[rowIndex][colIndex + 1] == None) and not (
                        tile_matrix[rowIndex][colIndex + 2] == None) and tile_matrix[rowIndex - 1][
                        colIndex + 1] == None
                        and tile_matrix[rowIndex - 1][colIndex + 2] == None):
                     score += col.number
                     score += tile_matrix[rowIndex][colIndex + 1].number
                     score += tile_matrix[rowIndex][colIndex + 2].number
                     tile_matrix[rowIndex][colIndex] = None
                     tile_matrix[rowIndex][colIndex + 1] = None
                     tile_matrix[rowIndex][colIndex + 2] = None

               elif (colIndex == 11):  # Rightmost side
                  if (tile_matrix[rowIndex][colIndex - 1] == None):
                     score += col.number
                     tile_matrix[rowIndex][colIndex] = None
                  elif (not (tile_matrix[rowIndex][colIndex - 1] == None) and tile_matrix[rowIndex - 1][
                     colIndex - 1] == None and tile_matrix[rowIndex][colIndex - 2] == None):
                     score += col.number
                     score += tile_matrix[rowIndex][colIndex - 1].number
                     tile_matrix[rowIndex][colIndex] = None
                     tile_matrix[rowIndex][colIndex - 1] = None
                  elif (not (tile_matrix[rowIndex][colIndex - 1] == None) and not (
                           tile_matrix[rowIndex][colIndex - 2] == None) and tile_matrix[rowIndex - 1][
                            colIndex - 1] == None
                         and tile_matrix[rowIndex - 1][colIndex - 2] == None and tile_matrix[rowIndex][
                            colIndex - 3] == None):
                     score += col.number
                     score += tile_matrix[rowIndex][colIndex - 1].number
                     score += tile_matrix[rowIndex][colIndex - 2].number
                     tile_matrix[rowIndex][colIndex] = None
                     tile_matrix[rowIndex][colIndex - 1] = None
                     tile_matrix[rowIndex][colIndex - 2] = None
               else:
                  if (tile_matrix[rowIndex][colIndex - 1] == None and tile_matrix[rowIndex][
                     colIndex + 1] == None):
                     score += col.number
                     tile_matrix[rowIndex][colIndex] = None
                  if (colIndex + 2 <= 11):
                     if (tile_matrix[rowIndex][colIndex - 1] == None and not (
                              tile_matrix[rowIndex][colIndex + 1] == None) and tile_matrix[rowIndex - 1][
                         colIndex + 1] == None and tile_matrix[rowIndex][colIndex + 2] == None):
                        score += col.number
                        score += tile_matrix[rowIndex][colIndex + 1].number
                        tile_matrix[rowIndex][colIndex] = None
                        tile_matrix[rowIndex][colIndex + 1] = None
                  if (colIndex + 3 >= 12):
                     continue
                  if (tile_matrix[rowIndex][colIndex - 1] == None and not (
                           tile_matrix[rowIndex][colIndex + 1] == None) and not (
                           tile_matrix[rowIndex][colIndex + 2] == None) and tile_matrix[rowIndex - 1][
                      colIndex + 1] == None and tile_matrix[rowIndex - 1][colIndex + 2] == None and
                           tile_matrix[rowIndex][colIndex + 3] == None):
                     score += col.number
                     score += tile_matrix[rowIndex][colIndex + 1].number
                     score += tile_matrix[rowIndex][colIndex + 2].number
                     tile_matrix[rowIndex][colIndex] = None
                     tile_matrix[rowIndex][colIndex + 1] = None
                     tile_matrix[rowIndex][colIndex + 2] = None
      return score