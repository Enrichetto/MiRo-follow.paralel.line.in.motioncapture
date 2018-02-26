# [SoRo Project] MiRo Obstacle avoidance using sonar sensor and moving towards goal position

## Project Contributers: 
1. enrico.borello@yahoo.it
2. kai.sukumar@gmail.com
3. leonard.marsault@gmail.com

## Objective:
MiRo moving towards the goal set inside the motion capture area. Along with, using data coming from Sonar sensor of MiRo, to satisfy a control law that avoids obstacles.

## Accomplishments
### MiRo orients towards the goal and moves towards it. If there is an obstacle, it avoids it using SONAR
Decision on direction based on angle as well as distance from goal position

Discovery of 'drive body through motion controller' for natural movement of MiRo (motion controller is inbuilt in MiRo based on Park's and Kuiper's 2011 (ICRA) algorithm)

### Modules or Nodes in the system
Three nodes (orient and move towards goal, scan the obstacle, avoid the obstacle using odometry of MiRo)

### Limitations of the system
Sonar values not very accurate (Some values in he input-stream come in as zero, hence disturbing the logic of the obstacle avoidance code)

Markers on MiRo were not detected consistently, hence moving towards goal position using motion capture, is not working efficiently.

At the end of the project, the program logic is adhoc. This can be futher improved in future, by overcoming the above limitations.

## How to Run:

To configure MiRo with your workstation follow the setup guide on official website or https://github.com/EmaroLab/MIRO

To run our application (miro should be able to follow a straight line given a goal position)

----Lauch the program----

you can lauch all the three node: ```roslaunch straightmiro miro.launch``` OR run a single node using ```rosrun straightmiro nameofthenode.py```

----set_goal.py---- 

Parameter Server is used for set the global parameters that we need for lauch the nodes.

set_goal.py declares and sets the parameters

----MiRo moving in a straight line----

-depending from how you take the miro position you could have problem of orientation.

-in the code the is a commented part that should be able to fix miro position if it go out from the straight line( for example if there is a note regual ground)

-the straight.py node subscrive a node that should publish in this way ```rostopic echo /miro/pose```




