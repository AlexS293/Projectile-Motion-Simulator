import pygame
import pygame.display
from pygame.locals import *
import math
import matplotlib.pyplot as plt
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import tkinter as tk
from tkinter import ttk

pygame.init() # Initialise the pygame library
win = pygame.display.set_mode((1500, 800), DOUBLEBUF) # Create pygame window
screen = pygame.display.get_surface()

white = (255,255,255) # Define the colour white
background = pygame.Surface((1500, 800)) # Give background colour
background.fill((190,255,255)) # Fill background with light blue

choices = ['Particle - DC = 0','Sphere - DC = 0.47','Cube - DC = 0.8','Streamlined body - DC = 0.04','Cow - DC = 0.5', 'Custom - DC = Input'] # list of drop-down menu options

tblProjectiles = [['Particle',0,0,10,0,2,0.1,0.1], #######GROUP B - 2-Dimensional list - [Name, Drag Coeff, Lower mass range, Upper mass range, Lower radius range, Upper radius range, Mass slider step, Radius slider step]#######
['Sphere',0.47,0.1,25,0.01,1,0.1,0.01],                                   
['Cube',0.8,0.1,25,0.01,1,0.1,0.01],
['Streamlined body',0.04,0.05,4,0.01,1,0.05,0.01],
['Cow',0.50,40,640,0.5,2,20,0.1]]

# Create the labels for the results boxes, disables them so they cannot be interacted with then hides them
heightResultLabel = TextBox(win, 140, 500, 100, 50, fontSize=35, colour=(190,255,255), borderThickness=0)
heightResultLabel.disable()
heightResultLabel.setText('Max Height: ')
distanceResultLabel = TextBox(win, 460, 500, 100, 50, fontSize=35, colour=(190,255,255), borderThickness=0)
distanceResultLabel.disable()
distanceResultLabel.setText('Max Distance: ')
timeResultLabel = TextBox(win, 780, 500, 100, 50, fontSize=35, colour=(190,255,255), borderThickness=0)
timeResultLabel.disable()
timeResultLabel.setText('Total time: ')
heightResultLabel.hide()
distanceResultLabel.hide()
timeResultLabel.hide()

def Results(heightResult, distanceResult, timeResult): # Create results boxes to show the results of projectile motion taken from the parameters of the function
  heightResultLabel.show()
  distanceResultLabel.show() # Make the results boxes reappear if they are hidden
  timeResultLabel.show()
  heightResultBox = TextBox(win, 140, 550, 275, 75, colour=(0,200,230), borderThickness=2, fontSize=50)
  heightResultBox.disable()
  heightResultBox.setText(heightResult) 
  distanceResultBox = TextBox(win, 460, 550, 275, 75, colour=(0,200,230), borderThickness=2, fontSize=50)
  distanceResultBox.disable()
  distanceResultBox.setText(distanceResult)
  timeResultBox = TextBox(win, 780, 550, 275, 75, colour=(0,200,230), borderThickness=2, fontSize=50)
  timeResultBox.disable()
  timeResultBox.setText(timeResult)

def errorBox(): # Creates an error box that says to say to try again
  root = tk.Tk()
  root.geometry('200x100')
  root.resizable(False,False)
  root.title('Error')
  errorLabel = ttk.Label(root, text=('An error occured - Try again'))
  errorLabel.pack(ipadx=10, ipady=10)
  root.mainloop()

class Projectile: #######GROUP A - Complex user-defined OOP - Superclass ########
#Hierarchal OOP class system used to create projectiles based on user inputs
#The Projectile class is used to represent a particle so the variables initiated (drag coeff, air density and mass) are not needed when just calling the projectile class but will be needed for the sub-class that includes drag
#As the projectile represents a particle then it only experiences projectile motion without drag as drag is not experienced by particles/makes no noticeable difference

  def __init__(self,c,p,m,g):
    self.dragCoeff = c                                # c = drag coefficient (No units)
    self.airDensity = p                               # p = air density (kgm^-3)
    self.mass = m                                     # m = mass (kg)
    self.gravity = g                                  # g = gravity (ms^-2)
  
  def getDragCoeff(self): # Returns drag coefficient, if drag coeff = 0 then the motion is not effected by drag
    return self.dragCoeff
  
  def getAirDensity(self): # Returns air density
    return self.airDensity
  
  def getMass(self): # Returns mass
    return self.mass

  def getGravity(self): # Returns gravity
    return self.gravity
  
  def Motion(self,y,u,a):#######GROUP A - Complex scientific model ####### 
                         # Calculate projectile motion excluding drag, this is done by calculating the linear motion between thousands of small coordinates until a stopping condition is reached
    g = Projectile.getGravity(self) # Get value of gravity
    a = math.radians(a) # convert angle to radians
    uy = u*math.sin(a)                                # uy = vertical velocity (ms^-1)
    ux = u*math.cos(a)                                # ux = horizontal velocity (ms^-1)
    tt = 0 # Total time is initially 0
    x = 0 # horizontal displacement is initially 0
    xmaxFound = False # maximum horizontal displacement hasnt been found yet
    ymaxFound = False # maximum vertical displacement hasnt been found yet
    xlist = [] #######GROUP C - Single dimensional array - list of x coordinates for graph ########
    ylist = [] #######GROUP C - Single dimensional array - list of y coordinates for graph ########
    errorOccured = False # An error hasnt occured yet
    while True: # This algorithm calculates the motion of a projectile by calculating the displacement each 0.1 millisecond until the height of the projectile above ground is within 1 decimal place of 0 metres 
      t = 0.0001 # 0.1 ms
      tt += 0.0001 # 0.1 ms added to the total time each iteration                                     
      vy = uy-(g*t)
      y += ((vy*t) + (0.5*g*(t**2)))                    # y = vertical displacement/height (m)
      x += ux*t                                       # x = horizontal displacement/distance (m)
      xlist.append(x) #######GROUP A - List operations - adds calculated x-coordinate to list ########
      ylist.append(y) #######GROUP A - List operations - adds calculated y-coordinate to list ########
      if (round(vy,1)==0) and (ymaxFound == False): # if vertical velocity is within 1 decimal place of 0 ms^-1 and maximum height hasn't been found yet then calculate maximum height
        t += (vy/g)
        y += (-(vy**2))/(2*g) #######GROUP A - Complex mathematics ########                      
        x += (ux*t)
        ymax = y #Define maximum height to be displayed as result later
        ymaxFound = True # Maximum height has been found
        tt += t
        xlist.append(x) #######GROUP A - List operations ########
        ylist.append(y) #######GROUP A - List operations ########
      if (round(y,1)==0) and (tt>1) and (xmaxFound == False): # If vertical displacement is within 1 decimal place from 0, total time is above 1 and maximum distance hasnt been found yet then find the maximum distance
        vy = -(math.sqrt((uy**2)+(2*g*t)))                    # This selection statement acts as the while loops stopping condition
        t += ((vy-uy)/g)                  #######GROUP A - Complex mathematics ########
        x += ux*t
        xmax = x #Define maximum height to be displayed as result later
        xmaxFound = True # Maximum horizontal displacement has been found
        tt += t # Define the total time to be displayed as result later
        xlist.append(x) #######GROUP A - List operations ########
        ylist.append(y) #######GROUP A - List operations ########
        break # Break out of the iterative loop
      if tt>210: # If total time is greater than 210s then and error has occured and creates an error box, 210 seconds is a few seconds over the highest possible total time achievable using my program
        errorBox()
        errorOccured = True
        break
      
      uy = vy # initial vertical velocity of the next motion becomes the final vertical velocity of the motion just calculated, this is to make it so that the next coordinate found starts off from it's previous point

    if not errorOccured: # If an error hasn't occured then display the results on screen and plot a graph using the lists of coordinates (xlist and ylist)
      Results((str(round(ymax,2)) + ' metres'),(str(round(((round(tt,2))*(u*math.cos(a))),2))+ ' metres'), (str(round(tt,2)) + ' seconds')) # Values of results are turned to strings so they can be displayed
      events = pygame.event.get()
      pygame_widgets.update(events) # Update the program's main screen
      pygame.display.update(pygame.Rect((140,500),(1055,125))) # Update specific rectangle of space on main screen where all results and labels are displayed so that it doesn't cause issues with other objects on screen

      plt.plot(xlist,ylist, label = 'Excluding Drag') # Plot graph of motion on new tab
      plt.legend()
      plt.show()
      
  
class includingDrag(Projectile): #######GROUP A - Complex user-defined OOP - Subclass ########
  
  def __init__(self,c,p,m,g,r,pt):
    super().__init__(c,p,m,g) #######GROUP A - Complex user-defined OOP - Inheritance from superclass ########
    self.radius = r                                   # r = radius (m)
    self.projectileType = pt                          # pt = projectile type e.g. sphere, cube, streamlined body, cow or custom                          
    self.isCube = False # Boolean used to find out whether to calculate area as square or circular
  
  def getRadius(self): # Return radius
    return self.radius

  def getProjectileType(self): # Return projectile type
    return self.projectileType

  def checkIfCube(self): # Checks if projectile type is cube or not
    if (includingDrag.getProjectileType(self)) == choices[2]: # choices[2] gives 'Cube - DC = 0.8', projectileType is also given in this form
      self.isCube = True
    return self.isCube
      
  def getArea(self): # get cross-sectional area of projectile, if it is a cube then the equation for area is different
    if includingDrag.checkIfCube(self):
      A = (includingDrag.getRadius(self)**2)                   # A = cross-sectional area (m^2), area of cube is two sides multiplied together which is the same as finding area of a square
    else:
      A = (math.pi)*((includingDrag.getRadius(self)**2))       # A = cross-sectional area (m^2), area of any other projectile type has a circular cross-sectional area
    self.area = A 
    return self.area
  
  def getConstant(self): # Get the drag constant to help calculate drag
    k = 0.5*(includingDrag.getDragCoeff(self))*(includingDrag.getAirDensity(self))*(includingDrag.getArea(self)) #######GROUP A - Complex user-defined OOP - Inheritance of subroutines from superclass########
    self.constant = k                                 # k = drag constant (No units)                             #######GROUP C - Simple mathematical calculations ########
    return self.constant
  
  def Motion(self,y,u,a): #######GROUP A - Complex user-defined OOP - Polymorphism of Motion subroutine from superclass - The motion algortihm is augmented to the subclass to execute motion differently as this motion includes drag########
                          #######GROUP A - Complex scientific model ####### 
                          
    # This algorithm does not create a curve but a series of thousands of tiny straight lines from point to point,
    # these lines are only around for 0.1 millisecond, this makes little to no differnece to the accuracy of my program
    # Motion is caluclated differently as motion with drag includes an new way of calculating vertical acceleration as well as a new horizontal acceleration not present in motion excluding drag
    
    g = Projectile.getGravity(self) #######GROUP A - Complex user-defined OOP - Inheritance of subroutine from superclass########
    x = 0                                             # x = horizontal displacement (m)
    m = includingDrag.getMass(self)
    k = -(includingDrag.getConstant(self))
    a = math.radians(a)
    uy = u*math.sin(a)                                # uy = vertical velocity (ms^-1)
    ux = u*math.cos(a)                                # ux = horizontal velocity (ms^-1)
    ax = (k/m)*(math.sqrt((ux**2)+(uy**2)))*ux        # ax = horizontal acceleration (ms^-2)
    ay = ((k/m)*(math.sqrt((ux**2)+(uy**2)))*uy) - g  # ay = vertical acceleration (ms^-2)
    tt = 0                                            # tt = time elapsed (s), total time is initially 0
    ymax = 0                                          # ymax = maximum height (m)
    xmax = 0                                          # xmax = maximum horizontal displacement (m)
    xmaxFound = False # Maximum horizontal displacement hasnt been found yet
    ymaxFound = False # Maximum vertical displacement hasnt been found yet
    xlist = [] #######GROUP C - Single dimensional array - list of x coordinates for graph ########
    ylist = [] #######GROUP C - Single dimensional array - list of y coordinates for graph ########
    errorOccured = False # An error hasn't occured yet
    while True: # Repeating loop to calculate the linear motion between two points until a stopping condition is met
      t = 0.0001                                       # t = 0.1ms 
      tt += 0.0001
      vx = ux + (ax*t)
      vy = uy + (ay*t)
      x += (ux*t) + (0.5*ax*(t**2)) #######GROUP A - Complex mathematics ########  
      y += (uy*t) + (0.5*ay*(t**2))                    
      xlist.append(x) #######GROUP A - List operations ######## 
      ylist.append(y) #######GROUP A - List operations ######## 
      if (round(vy,1) == 0) and (ymaxFound == False): # If vertical velocity is within 1 decimal place of 0 ms^-1 and maximum height hasn't been found yet then calculate maximum height
        ay = ((k/m) * vx) - g
        ax = (k/m) * vx
        t += (-vy/ay)
        y += (vy**2)/(2*ay)
        ymax = y
        x += (vx*t) + (0.5*ax*(t**2)) #######GROUP A - Complex mathematics ########
        tt += t
        ymaxFound = True
        xlist.append(x) #######GROUP A - List operations ########
        ylist.append(y) #######GROUP A - List operations ########
      if round(y,1)==0 and (tt>1) and (xmaxFound == False): # If vertical displacement is within 1 decimal place from 0, total time is above 1 and maximum distance hasnt been found yet then find the maximum distance,
                                                            # this selection statement is used as the stopping condition of the while loop
        ax = (k/m)*(math.sqrt((ux**2)+(uy**2)))*ux
        ay = ((k/m)*(math.sqrt((ux**2)+(uy**2)))*uy) - g #######GROUP A - Complex mathematics ########
        vy = -(math.sqrt((uy**2)+(2*-ay*y)))
        t += ((vy-uy)/ay)
        x += (ux*t) + (0.5*ax*(t**2))
        xmax = x
        tt += t
        xmaxFound = True
        xlist.append(x) #######GROUP A - List operations ########
        ylist.append(y) #######GROUP A - List operations ########
        break
      if tt>210:  # If total time is greater than 210s then and error has occured and creates an error box, 210 seconds is a few seconds over the highest possible total time achievable using my program
        errorBox()
        errorOccured = True
        break
        
      ux = vx # Initial vertical velocity of the next motion becomes the final vertical velocity of the motion just calculated, this is to make it so that the next coordinate found starts off from it's previous point,
      uy = vy # the horizontal and vertical accelerations are also redefined for the exact same reason as the acceleration is constantly changing as well
      ax = (k/m)*(math.sqrt((ux**2)+(uy**2)))*ux #######GROUP A - Complex mathematics ########
      ay = ((k/m)*(math.sqrt((ux**2)+(uy**2)))*uy) - g

    if not errorOccured: # If an error hasn't occured then display the results on screen and plot a graph using the lists of coordinates (xlist and ylist)
      Results((str(round(ymax,2)) + ' metres'),(str(round(xmax,2))+ ' metres'), (str(round(tt,2)) + ' seconds')) # Values of results are turned to strings so they can be displayed
      events = pygame.event.get()
      pygame_widgets.update(events) # Update the program's main screen
      pygame.display.update(pygame.Rect((140,550),(1055,75))) # Update specific rectangle of space on main screen where all results and labels are displayed so that it doesn't cause issues with other objects on screen

      plt.plot(xlist,ylist, 'r', label = 'Including Drag') # Plot graph of motion on new tab, the graph's line becomes red to represent when motion is including drag
      plt.legend()
      plt.show()

    
def getProjectileIndex(): # Gets the current option of the drop-down menu and returns it's index in the choices list to later be used to locate values in the 2-D list e.g. slider ranges/increments
  if (dropdown.getSelected() == None) or (dropdown.getSelected() == choices[0]): # If there is no currently selected option then the returned index is 0
    return 0
  elif dropdown.getSelected() == choices[1]:
    return 1
  elif dropdown.getSelected() == choices[2]:
    return 2
  elif dropdown.getSelected() == choices[3]:
    return 3
  elif dropdown.getSelected() == choices[4]:
    return 4
  else:
    return 5
  
# Create drop-down menu, colour of the menu option gets progressively darker when hovered over or clicked
dropdown = Dropdown(win, 1125, 100, 200, 75, name='Objects - DC = Drag Coefficient', choices = choices, inactiveColour=(80,150,150), pressedColour=(20,90,90), hoverColour=(50,120,120), onClick = getProjectileIndex)

massSlider = Slider(win, 1100, 350, 250, 20, min= tblProjectiles[(getProjectileIndex())][2], # Gets the minimum, maximum and increment values of currently chosen object from the 2-D list
                    max= tblProjectiles[(getProjectileIndex())][3], step= (tblProjectiles[(getProjectileIndex())][6]), colour=(80,150,150), handleColour=(0,40,80)) # Create mass slider, a box that displays the slider's current value
                                                                                                                                                                    # and a label to say the slider effects mass with units 
massBox = TextBox(win, 1200, 400, 50, 40, colour=(80,150,150), borderThickness=2, fontSize=25)
massBox.disable()
massLabel = TextBox(win, 1250, 400, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0)
massLabel.setText('Mass (kg)')
massLabel.disable()

radiusSlider = Slider(win, 1100, 475, 250, 20, min= tblProjectiles[(getProjectileIndex())][4], # Gets the minimum, maximum and increment values of currently chosen object from the 2-D list
                    max= tblProjectiles[(getProjectileIndex())][5], step= (tblProjectiles[(getProjectileIndex())][7]), colour=(80,150,150), handleColour=(0,40,80)) # create radius slider, a box that displays the slider's current value
                                                                                                                                                                    # and a label to say the slider effects radius with units
radiusBox = TextBox(win, 1200, 525, 50, 40,colour=(80,150,150), borderThickness=2, fontSize=25)
radiusBox.disable()
radiusLabel = TextBox(win, 1250, 525, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0)
radiusLabel.setText('Radius (m)')
radiusLabel.disable()

coeffBox = TextBox(win, 1125, 500, 50, 40, colour=(80,150,150), fontSize=25, borderThickness=2)
coeffBox.hide()
coeffLabel = TextBox(win, 1250, 500, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0) # Creates a drag coefficient input box and it's label, the box is hidden until the drop-down menu's current object is custom
coeffLabel.setText('Drag Coefficient')
coeffLabel.disable()
coeffLabel.hide()

airDensityBox = TextBox(win, 1125, 250, 80, 40, colour=(80,150,150), borderThickness=2, fontSize=25)
airDensityBox.setText('1.225')
airDensityLabel = TextBox(win, 1205, 250, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0) # Creates an air density input box, a label with a range of it's accepted values 
airDensityLabel.setText('Air Density (kg/m^3) -')
airDensityLabel.disable()
airDensityRangeLabel = TextBox(win, 1205, 275, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0)
airDensityRangeLabel.setText('0.5 kg/m^3 to 1.5 kg/m^3')
airDensityRangeLabel.disable()

gravitySlider = Slider(win, 1100, 700, 250, 20, min= 0.5, max= 25, step= 0.1, initial= 9.8, colour=(70,130,190), handleColour=(20,60,100)) # Create gravity slider, a box that displays the sliders current value                                          
gravityBox = TextBox(win, 1200, 750, 50, 40, colour=(70,130,190), borderThickness=2, fontSize=25)                                          # and a label to say the slider effects gravity with units
gravityBox.disable()
gravityLabel = TextBox(win, 1250, 750, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0)
gravityLabel.setText('Gravity (m/s^2)')
gravityLabel.disable()

heightSlider = Slider(win, 140, 700, 250, 20, min = 0, max = 20, step=1, colour=(70,130,190), handleColour=(20,60,100), initial= 0) # Create height slider, a box that displays the sliders current values
heightBox = TextBox(win, 240, 750, 50, 40, colour=(70,130,190), borderThickness=2, fontSize=25)                                     # and a label to say the slider effects height with units
heightBox.disable()
heightLabel = TextBox(win, 290, 750, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0)
heightLabel.setText('Height (m)')
heightLabel.disable()

angleSlider = Slider(win, 460, 700, 250, 20, min=0, max = 90, step=1, colour=(70,130,190),  handleColour=(20,60,100), initial= 45) # Create angle slider, a box that displays the sliders current values
angleBox = TextBox(win, 560, 750, 50, 40, colour=(70,130,190), borderThickness=2, fontSize=25)                                     # and a label to say the slider effects angle with units
angleBox.disable()
angleLabel = TextBox(win, 610, 750, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0)
angleLabel.setText('Angle (degrees)')
angleLabel.disable()

velocitySlider = Slider(win, 780, 700, 250, 20, min=1, max=50, step=0.5, colour=(70,130,190),  handleColour=(20,60,100), initial= 25)# Create velocity slider, a box that displays the sliders current values
velocityBox = TextBox(win, 880, 750, 50, 40, colour=(70,130,190), borderThickness=2, fontSize = 25)                                  # and a label to say the slider effects velocity with units
velocityBox.disable()
velocityLabel = TextBox(win, 930, 750, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0)
velocityLabel.setText('Velocity (m/s)')
velocityLabel.disable()

def checkAirDensityInput(): # Exception handling is used to check the input of the air density box to see if it is in the range
  try:
    airDensityInput = (float(airDensityBox.getText()))
  except ValueError:
    return False
  else:
    if (airDensityInput<=1.5) and (airDensityInput>=0.5):
      return True
    
def checkCustomInput(): # Exception handling is used to check the input of the mass, radius and coeff boxes when the drop-down menu's current option is on custom
  try:
    massInput = float(massBox.getText())
    radiusInput = float(radiusBox.getText())
    coeffInput = float(coeffBox.getText())
  except ValueError: # If inputs are not integers or floats then a false is returned to cause an error
    return False
  else:
    if (massInput<=500) and (massInput>=0.01):
        if (radiusInput<=5) and (radiusInput>=0.01):
            if (coeffInput<=2) and (coeffInput>=0.01):
                return True

def getProjectile(): # Creates the projectile that is to be shot when the button is pressed using current values from sliders and input boxes, current drop-down menu choice changes value of drag coeff and projectile type
                         # Structure of inputs is Projectile/includingDrag(Drag coeff, air density, mass, gravity, radius, projectile type), no radius value or projectile type
                         # for Projectile class and drag coeff value is found from 2-D list, 
                         # choices[0] = Particle, choices[1] = Sphere, choices[2] = Cube, choices[3] = Streamlined body, choices[4] = Cow, choices[5] = Custom
  if (checkAirDensityInput()): # Check if air density input is within the specified range
    if (dropdown.getSelected() == None) or (dropdown.getSelected() == choices[0]): # If user has no current menu choice or particle option is chosen then projectile motion excludes drag
      return Projectile((tblProjectiles[0][1]),(float(airDensityBox.getText())),(massSlider.getValue()),(gravitySlider.getValue()))
    elif dropdown.getSelected() == choices[1]:
      return includingDrag((tblProjectiles[1][1]),(float(airDensityBox.getText())), (massSlider.getValue()),(gravitySlider.getValue()), (radiusSlider.getValue()), choices[1])
    elif dropdown.getSelected() == choices[2]:
      return includingDrag((tblProjectiles[2][1]),(float(airDensityBox.getText())),(massSlider.getValue()),(gravitySlider.getValue()), (radiusSlider.getValue()), choices[2])
    elif dropdown.getSelected() == choices[3]:
      return includingDrag((tblProjectiles[3][1]),(float(airDensityBox.getText())),(massSlider.getValue()),(gravitySlider.getValue()), (radiusSlider.getValue()), choices[3])
    elif dropdown.getSelected() == choices[4]:
      return includingDrag((tblProjectiles[4][1]),(float(airDensityBox.getText())),(massSlider.getValue()),(gravitySlider.getValue()), (radiusSlider.getValue()), choices[4])
    else:
      if (checkCustomInput()): # If the inputs are all valid then the projectile is created, if not then the projectile isn't created causing an error in the shootProjectile function and therefore creating an error pop-up
        return includingDrag((float(coeffBox.getText())), (float(airDensityBox.getText())), (float(massBox.getText())),(gravitySlider.getValue()), (float(radiusBox.getText())), choices[5])

      
def shootProjectile(projectile, initHeight, initVelocity, initAngle): # Function to calculate projectile motion using current inputs of sliders and input boxes, if it can't be calculated then an error box is made
    try: # Exception handling used to catch any errors that may have occured in the creation of the projectile e.g. input out of range, if an attribute error occurs due to this then an error pop-up is created
        return (projectile.Motion(initHeight, initVelocity, initAngle))
    except AttributeError:
      errorBox()

def closeProgram(): # Function to close program, this is used for my program's close button and is used to stop my program's running loop
  pygame.quit()
  is_running = False
  quit()

# Creates a shoot button so that when it is clicked then projectile motion of current inputs is calculated so a graph is made and the results are displayed  
shootButton = Button(win, 1195, 600, 60, 60, text='Shoot', fontSize=20, margin=20, inactiveColour=(90, 180, 250), hoverColour=(90, 150, 240), pressedColour=(90, 130, 230), onClick=lambda: shootProjectile((getProjectile()),
                                                                                                                                                                                                           (heightSlider.getValue()),
                                                                                                                                                                                                           (velocitySlider.getValue()),
                                                                                                                                                                                                          (angleSlider.getValue())))
# Creates a button that closes the program when clicked
closeButton = Button(win, 1375, 25, 35, 35, text='X', fontSize=30, margin=20, inactiveColour=(250, 0, 0), hoverColour=(200, 0, 0), pressedColour=(150, 0, 0), onClick=lambda: closeProgram())


def changeImageNo(imageNum): # Changes the image number when left and right buttons are clicked
  global imageNo
  imageNo = imageNum
  
changeImageNo(1) # Initially the information card is the first card

# Create a right arrow button, when clicked the info card on screen changes to the next number in the loop
rightArrowButton = Button(win, 1000, 225, 50, 50, text='>', fontSize=30, margin=20, inactiveColour=(90, 180, 250), hoverColour=(90, 150, 240), pressedColour=(90, 130, 230), onClick=lambda: changeImage('R', imageNo))
# Create a left arrow button, when clicked the info card on screen changes to the previous number in the loop
leftArrowButton = Button(win, 150, 225, 50, 50, text='<', fontSize=30, margin=20, inactiveColour=(90, 180, 250), hoverColour=(90, 150, 240), pressedColour=(90, 130, 230), onClick=lambda: changeImage('L', imageNo))

def changeImage(choice, imageNum): # Changes the image when the left/right buttons are clicked, loops so it starts at 1 then ends at 10 and after 10 it goes back to 1
  if choice == 'R': # If right arrow is clicked
    if imageNum == 10:
      changeImageNo(1)
    else:
      imageNum +=1 
      changeImageNo(imageNum)
  if choice == 'L': # If left arrow is clicked
    if imageNum == 1:
      changeImageNo(10)
    else:
      imageNum -= 1
      changeImageNo(imageNum)
  if choice == 'C': # If there is no change then return the current choice
      pass
  return displayImage(imageNo)
    
def displayImage(imageNo): #######GROUP B - Files organised for sequential access - Loads images of information cards from file########
  if imageNo == 1:
   currentImage = pygame.image.load('TitlePage.png')
  elif imageNo == 2:
    currentImage = pygame.image.load('ContentsPage.png')
  elif imageNo == 3:
    currentImage = pygame.image.load('Key.png')
  elif imageNo == 4:
    currentImage = pygame.image.load('SUVATEquations.png')
  elif imageNo == 5:
    currentImage = pygame.image.load('ProjectileMotionEqs.png')
  elif imageNo == 6:
    currentImage = pygame.image.load('DragEquations.png')
  elif imageNo == 7:
    currentImage = pygame.image.load('StagesOfProjectileMotion.png')
  elif imageNo == 8:
    currentImage = pygame.image.load('ExamplesOfProjectileMotion.png')
  elif imageNo == 9:
    currentImage = pygame.image.load('PlanetGravities.png')
  else:
    currentImage = pygame.image.load('AirDensityAtDifferentAltitudes.png')
  win.blit(currentImage,(200,50))



is_running = True # Program is running

while is_running: # While program is running it checks the events 
    events = pygame.event.get()
    previousMenuChoice = dropdown.getSelected() # Menu choice is remembered to see if it changes later
    
    for event in events: 
        if event.type == pygame.QUIT: # If user has clicked exit button then program closes
            pygame.quit()
            is_running = False
            quit()

    win.fill((190,255,255)) # Fill window with light blue colour
    changeImage('C',imageNo) # Keep loaded image/information card as the current choice
    
    gravityBox.setText(round((gravitySlider.getValue()),1))
    velocityBox.setText(round((velocitySlider.getValue()),1)) # Set slider boxes to current slider value to 1 decimal place
    angleBox.setText(round((angleSlider.getValue()),1))
    heightBox.setText(round((heightSlider.getValue()),1))

    if previousMenuChoice != choices[5]: # If menu choice isn't the custom object then set mass and radius slider boxes to current slider values to 3 decimal places
      massBox.setText(round((massSlider.getValue()),3))
      radiusBox.setText(round((radiusSlider.getValue()),3))
      
    pygame_widgets.update(events) # Update all widgets made from pygame-widgets to see if there have been any changes e.g drop-down menu clicked or slider moved
    
    if dropdown.getSelected() != previousMenuChoice: # If drop-down menu choice has changed after the update then the slider ranges and increments are changed to the ones specified in the 2-D list at the start
      if dropdown.getSelected() != choices[5]: # If the new menu choice isn't the custom object then change slider ranges and increments
        massSlider.hide() # Hide old slider
        massSlider = Slider(win, 1100, 350, 250, 20, min= tblProjectiles[(getProjectileIndex())][2], # Create new slider with updated slider ranges and increments
                      max= tblProjectiles[(getProjectileIndex())][3], step= (tblProjectiles[(getProjectileIndex())][6]), colour=(80,150,150), handleColour=(0,40,80))
        radiusSlider.hide() # Hide old slider
        radiusSlider = Slider(win, 1100, 475, 250, 20, min= tblProjectiles[(getProjectileIndex())][4], # Create new slider with updated slider ranges and increments
                      max= tblProjectiles[(getProjectileIndex())][5], step= (tblProjectiles[(getProjectileIndex())][7]), colour=(80,150,150), handleColour=(0,40,80))
        massBox.hide() # Hide old current value box
        massBox = TextBox(win, 1200, 400, 50, 40, colour=(80,150,150), fontSize=25, borderThickness=2) # Create new current value box
        radiusBox.hide() # Hide old current value box
        radiusBox = TextBox(win, 1200, 525, 50, 40, colour=(80,150,150), fontSize=25, borderThickness=2) # Create new current value box
        coeffBox.hide() # Hide drag coeff box and label (only used when another option is chosen after custom option)
        coeffLabel.hide()
        massLabel.hide()
        massLabel = TextBox(win, 1250, 400, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0) # Hide, remake and disable the labels for mass and radius, this is done in case the old current option was the custom object
        massLabel.setText('Mass (kg)')
        massLabel.disable()
        radiusLabel.hide()
        radiusLabel = TextBox(win, 1250, 525, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0)
        radiusLabel.setText('Radius (m)')
        radiusLabel.disable()
      else: # If the new menu choice is the custom object then input boxes replace the sliders
        massSlider.hide()
        radiusSlider.hide() # Sliders are hidden
        massBox.hide() 
        massBox = TextBox(win, 1125, 350, 50, 40, colour=(80,150,150), fontSize=25, borderThickness=2) # Mass box is hidden and remade into an input box
        radiusBox.hide()
        radiusBox = TextBox(win, 1125, 425, 50, 40, colour=(80,150,150), fontSize=25, borderThickness=2) # Radius box is hidden and remade into an input box
        coeffBox.show() # Show the drag coefficient input box that was hidden earlier
        massLabel.hide()
        massLabel = TextBox(win, 1175, 350, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0) # Hide, remake and disable all labels (mass, radius and coeff) in new positions, labels also show their allowed input ranges
        massLabel.setText('Mass - 0.01kg to 500kg')
        massLabel.disable()
        radiusLabel.hide()
        radiusLabel = TextBox(win, 1175, 425, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0)
        radiusLabel.setText('Radius - 0.01m to 5m')
        radiusLabel.disable()
        coeffLabel = TextBox(win, 1175, 500, 75, 30, fontSize=25, colour=(190,255,255), borderThickness=0)
        coeffLabel.setText('Drag Coefficient - 0.01 to 2')
        coeffLabel.disable()
    pygame.display.update() # Update the program's main screen


