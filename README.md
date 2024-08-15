# Max Overview

A main file with 3 polys. Within the main file, poly objects are triggered for each color when an OSC message for a pixel of that color is received. Note also that different 
colors correspond to different notes within our octave. Also note that as not every pixel processed exactly matches the color it is closest to, we have an offset from the signal 
sent by our base “color” and the actual signal of our pixel. We additionally see oscillators offset from the color that play in correspondence with this at a volume and note 
reciprocal to that of the pixel. 
Redpoly:  plays when “red” input is received. Makes use of multiplicative saw~ objects for a harsher sound, and a line~ object.
Bluepoly: plays for “blue” input. Makes use of multiplicative saw~ and tri~ objects, and line~ objects for more natural transitions.
Greenpoly: plays for “blue” input. Makes use of multiplicative rect~ and cycle~ objects, and line~ objects for more natural transitions. Mirrors Bluepoly.

# Python Overview

Consists of a singular main.py file which controls all processes. It uses the Python Image Library and python-osc module to assist with this. It first reads in image information 
and program parameters through a GUI, and then takes this information to begin establishing behaviors for the overall process. It compresses our image as necessary 
for processing, defines our colors and octaves, sends general data to Max over OSC, and then begins to process our image pixel-by-pixel. For each pixel it performs a series of 
operations to determine its color, amplitude, panning, and offset from its associated color. It then sends this pixel info to Max using OSC, and moves on to the next pixel 
following a predefined delay. All OSC messages sent are additionally printed to the terminal. When a pixel is received by Max, we immediately begin to hear its output. Following 
along in the Python terminal output, we thus see which pixel is generating which signal.

# How to Run The Project

To activate the project and generate a composition, run the Python code through the command line while the Max file entitled main is open and all poly 
files are in its same directory. 
The command line input takes the following format: 

`python3 main.py <ip_address> <port>`

From here, the GUI window is opened.
