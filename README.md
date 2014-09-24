eyeDetector
===========

Python Eye Detection algorithms with OpenCV + server backendo to run from the internet 
(no front end)




===========


This is intended as a backup of one of our servers. It may be hard to run without having access to the
configured server. 

HOWEVER THE EYE DETECTION ALGORITHMS IN eyedetection.py ARE SELF CONTAINED AND CAN BE EASILY USED BY OTHER APPLICATIONS



The main file is eyeDetector.py. 

It defines 3 functions to take an input image and detect the face and eyes of a person.
The person must be facing the camera in order for the algorithm to work. 

This module needs the XML data included in haarCascadesXML.

All other files are a wrapupp to run the eye detection algorithm in a webserver that receives videostream
from websites. Originally our web app would access the users webcam to take real time video and send it to the 
server via websockets. The server would detect the eyes for every frame and report back to the website. 



