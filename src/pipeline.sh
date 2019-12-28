#!/bin/bash
echo "Welcome to the GNN-based "
echo "Make sure the parameters in the config.py and in the launch/main.launch are what you need"
echo "Now it is the time to navigate the robot around to take photos. If everything good so far, type [y] and [n] otherwise"
read answer
if [ "$answer" = "y" ]; then

	echo "In a new terminal, type roslaunch gnn main.launch"
else
	exit "exited"
fi

echo "Once the robot is done with the navigation, shutdown that process. When you shutdown, hit [y]"

read answer
if [ "$answer" = "y" ]; then

	cd input_images
	
else
	exit "exited"
fi


