# Straightmiro
--------------------ENRICO BORELLO's note--------------------------



-------------position of miro by motion capture------

the straight.py node subscrive a node that should publish in this way
-rostopic echo /miro/pose


--------------------mirosetup-----------------------------
follow this step


-Connect the miro with smarthone


-with the app put the miro in normal mode

-enable the bridge

- write in the terminal of your computer the ip of miro that you can see in the app
  ssh root@hereputtheIPofmiroapp

-digit the password 
 MIROOpen1

- write 
sudo nano ~/.profile

-write your IP in the file in a line with:
#.. bla bla (line simply for your reference)
#.. bla bla (line simply for your reference)
#.. bla bla (line simply for your reference) 
ROS_MASTER= putyourip

-save and exit from the miro room, you can do date writing:
   exit

-------------see if you are connectend with the miro-------- 

-enter in the folder where you dowload the miro file, if you dont already do that ->(http://labs.consequentialrobotics.com/miro/mdk/)
  ~/lib/mdk/bin/shared (in my case)

-write this in your terminal

- ./miro_ros_client_gui.py robot=rob01


-you should see what miro see.

-IF NOT

put miro in demo mode using your smartphone, and again in normal mode.



----------------lauch the program----------
-you can lauch all the three node:
roslaunch straightmiro miro.launch

-or run a single node using
rosrun straightmiro nameofthenode.py


----------set_goal.py------------------
Parameter Server is used for set the global parameters that we need for lauch the nodes.

 set_goal.py  declares and set the parameters




---------------------Stright miro-------------


miro should be able to follow a straight line given a goal position

-depending from how you take the miro position you could have problem of orientation.

-in the code the is a commented part that should be able to fix miro position if it go out from the straight line( for example if there is a note regual ground)




