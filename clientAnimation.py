#Function: Mirror Adjustment
#input: xStartPosition, yStartPosition, xEndPosition, yEndPosition, fileTable, gridWidth, gridHeight, screenWidth, screenHeight
#output: array of files to iterate through, xNewStartPosition (in pixels in case grid size changes), yNewStartPosition (px)
#steps:  1. Determine starting position grid block
#		2. Determine ending position grid block
#		3. Find the array size
#		4. Fill the array with files: horizontal first, vertical second
#		5. Return image array
#		6. Return the end position
#
#


#define Screen
class Screen(object):
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 360
    GRID_WIDTH = 4
    GRID_HEIGHT = 4


##########################################################################################
def rightOrLeft(x_start_block, x_end_block):
    """
    determines if the user's eyes moved left or right, 
    and by how many blocks
    """
    #if no change in xBlock
    if x_start_block == x_end_block:
        num_x = 0
        right = False
    
    #if moved right
    elif x_start_block < x_end_block:
        num_x = x_end_block - x_start_block
        right = True
    
    #if moved left
    else:
        num_x = x_start_block - x_end_block
        right = False
    #return the number of blocks moved 
    #	and whether it was right or left
    return num_x, right

##########################################################################################
#determine if up or down, and by how many 
def upOrDown(y_start_block, y_end_block):
    """
    determines if the user's eyes moved up or down, 
    and by how many blocks
    """
    #if no change in yBlock
    if y_start_block == y_end_block:
        num_y = 0
        up = False

    #if moved down
    elif y_start_block < y_end_block:
        num_y = y_end_block - y_start_block
        up = False

    #if moved up
    else:
        num_y = y_start_block - y_end_block
        up = True
    #return the number of blocks moved 
    #	and whether it was up or down
    return num_y, up

##########################################################################################    
def fillImageArray(num_x, num_y, x_start_block, x_end_block, y_start_block, y_end_block, num_moves,right,up):
    """
    this function will fill the array with image files that will be sent
    to the client to simulate adjustment of the mirrors
    """
    #set the loop condition for n=0, and it will set to false and end loop
    #	when n>=num_moves (below); 
    #This dual set of statements is the python way of saying
    #	while n <= num_moves
    n = 0


    while True:
        if num_x > 0:

            if right:
                x_movements = xrange(x_start_block, x_end_block)
                #print '******************'
                #print 'GOING RIGHT' 
                #print 'x_movements = ', x_movements
                
                for i in x_movements:
                    #print 'Appending: ', stored_images[i][y_start_block]
                    image_array.append(stored_images[i][y_start_block])
                    n += 1  

            else:
                x_movements = xrange(x_start_block, x_end_block,-1)
                #print '*******************'
                #print 'GOING LEFT' 
                #print 'x_movements reversed = ', x_movements
               
                for j in x_movements:
                    image_array.append(stored_images[j][y_start_block])
                    #print 'Appending: ', stored_images[j][y_start_block]
                    n += 1

        # ####################################### 

        
        if num_y > 0:


            if up: 
                y_movements = xrange(y_start_block, y_end_block,-1)
                #print '*******************'
                #print 'GOING UP' 
                #print 'y_movements reversed = ', y_movements

                for k in y_movements:
                    image_array.append(stored_images[x_end_block][k])
                    #print 'Appending: ', stored_images[x_end_block][k]
                    n += 1
                
            else:
                y_movements = xrange(y_start_block, y_end_block)
                #print '*******************'
                #print 'GOING DOWN' 
                #print 'y_movements = ', y_movements


                for l in y_movements:
                    image_array.append(stored_images[x_end_block][l])
                    #print 'Appending: ', stored_images[x_end_block][l]
                    n += 1
        
        #once the number of moves has been reached, stop appending        
        if n >= num_moves:
            break	
            
    #append the end block to the array        
    image_array.append(stored_images[x_end_block][y_end_block])        
    return image_array

##########################################################################################
def getArray (x_start_position, y_start_position, x_end_position, y_end_position):
	
    #cover the edge cases of pixel on max edge
    if x_start_position == Screen.SCREEN_WIDTH:
        x_start_position -= 1
    if y_start_position == Screen.SCREEN_HEIGHT:
        y_start_position -= 1
    if x_end_position == Screen.SCREEN_WIDTH:
        x_end_position -= 1
    if y_end_position == Screen.SCREEN_HEIGHT:
        y_end_position -= 1

    #determine grid block for start and end eye location (force to integer value)
    x_start_block = int(x_start_position / x_pixels_per_grid_block)
    y_start_block = int(y_start_position / y_pixels_per_grid_block)

    x_end_block = int(x_end_position / x_pixels_per_grid_block)
    y_end_block = int(y_end_position / y_pixels_per_grid_block) 
    grid = (x_start_block, y_start_block,x_end_block,y_end_block) 

	
    #determine if left or right, and by how many 
    num_x, right = rightOrLeft(x_start_block, x_end_block)

    #determine if up or down, and by how many 
    num_y, up = upOrDown(y_start_block, y_end_block)


    #Find the array size: the total number of h & v moves to get from start to end position
    num_moves = num_x + num_y
    #require a minimal shift in order to calculate
    if (num_x + num_y) > 2:
        #build the array
        image_array = fillImageArray(num_x,num_y,x_start_block, x_end_block, y_start_block, y_end_block, num_moves,right,up)
        return image_array,grid
    else:
	return 'nope','nogrid'



##########################################################################################

#this is the array of file names, assuming a 4x4 block of screens
#I will expand this to a larger set of files as necessary
stored_images=[['zero_zero.jpg','zero_one.jpg','zero_two.jpg','zero_three.jpg'], 
               ['one_zero.jpg','one_one.jpg','one_two.jpg','one_three.jpg'],
               ['two_zero.jpg','two_one.jpg','two_two.jpg','two_three.jpg'],
               ['three_zero.jpg','three_one.jpg','three_two.jpg','three_three.jpg']]

#initialize the array that returns the file names
image_array=[]
right = False
up = False


#determine pixel dimensions of each grid block		
x_pixels_per_grid_block = Screen.SCREEN_WIDTH/Screen.GRID_WIDTH
y_pixels_per_grid_block = Screen.SCREEN_HEIGHT/Screen.GRID_HEIGHT


print ' '
print 'Animation array function initialized'
print ' '



    
