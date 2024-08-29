# Projectile Motion Simulator
This is a GUI created in Python for accurately calculating projectile motion including or excluding drag.

The purpose of this project was to aid in the teaching and understanding of projectile motion to A-Level or Degree level students, as such there are also different information cards with insightful information regarding the topic.
## Prerequisites
Must use Python version 3.9 with the following modules installed: pygame, pygame.display, pygame.locals, pygame_widgets, matplotlib and tkinter.
All listed images must also be downloaded and be in the same file as the main code.
## Main Menu
The title screen that is displayed when launched:

![TitleScreen](https://github.com/user-attachments/assets/167cde9d-7b41-4945-9022-d82021429c67)

As can be noticed, all initial variables e.g. height and angle can be changed using sliders except for the air density which is an input box. 

There is a drop-down menu allowing the user to choose between different objects that have different drag coefficients.

Most of the screen is taken up by the information cards which can be cycled through using the '<' and '>' buttons on screen.

The 'Shoot' button calculates the projectile motion using the given inputs at the time of clicking it. There is also a red 'X' button in the top right corner which closes the program upon clicking.
## Functionality
I have uploaded video testing evidence to YouTube: https://youtu.be/nKqIcdqXFQE

This covers all functionality of my program although more brief tests are shown below.

Upon clicking the 'Shoot' button the following is displayed:

![TestImage](https://github.com/user-attachments/assets/055d842c-793f-46d3-a768-7f0ca11b389d)

The program is able to accurately calculate the motion and display the mathematical results of the maximum height, distance travelled and time with text boxes as well as visually display a graph of its trajectory on a moveable window that also allows the user to save the image or zoom in on a particular area.

![Drop-down](https://github.com/user-attachments/assets/091240ae-81bf-4412-a124-11a335577abe)

When the drop-down menu is clicked the objects listed can be chosen each with their own individual ranges for mass and radius. The custom option in particular changes the object variable inputs to all become text input boxes.

Upon changing the object to 'Custom', changing all motion and object inputs and clicking the 'Shoot' button the following is displayed:
![TestImage2](https://github.com/user-attachments/assets/a2297c90-0d89-49ec-b60e-eabc18aef174)

It is noticeable that when displaying motion including drag, the line of trajectory becomes red rather than blue. The parabola also becomes asymmetrical as expected when including drag. The mathematical results for heigh, distance and time are accurate as compared to similar programs.

![TestImage3](https://github.com/user-attachments/assets/24d08a05-08ca-4555-9836-098af9b6c95d)

When the '>' button is clicked on screen then the next information card in the cycle is displayed as shown above. The cycle is as in the contents page, once card 10 is reached then it will go back to 1 and vice versa. Each card is labelled in its top right corner.
## Project Details

This project taught me a lot about creating a Python GUI as well as implementing mathematics into a program. This program fulfilled its purpose as a usefeul tool to help teach projectile motion to A-Level / Degree level physics students.
