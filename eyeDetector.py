## MIT LICENSE
#Copyright (c) 2014 Hugo Arguinariz.
#http://www.hugoargui.com
#
#Permission is hereby granted, free of charge, to any person
#obtaining a copy of this software and associated documentation
#files (the "Software"), to deal in the Software without
#restriction, including without limitation the rights to use,
#copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the
#Software is furnished to do so, subject to the following
#conditions:

#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#OTHER DEALINGS IN THE SOFTWARE.

####################################################################################################

## eyeDetector.py
## Implements 3 related functions:
## decodeImage(rawImage) returns decImage.         ## Decode an image to a format usable by OpenCV
## detectEyes(decImage) returns img, eyesX, eyesY  ## Detects the eyes
## encodeImage (img) returns encImage              ## Encode the image to jpeg

####################################################################################################
## This module can be run to detect eyes on a video stream if it is called once per frame. 
## It was fast enough to do this on an american server receiving real time video from Europe, 
## So it should work fine in most situations. 
## 
####################################################################################################

####################################################################################################
import cv2
####################################################################################################



####################################################################################################
def decodeImage(img):
    ## Takes byte-encoded image and makes it usable for other OpenCV images
    ## Most common image formats are supported, including png, jpeg, tif, bmp
    decImg = cv2.imdecode(img, 1)
    return decImg
    
    

####################################################################################################
## We load Haar classifiers to use by openCV to detect faces
## This and other Haar classifiers can be obtained from https://github.com/Itseez/opencv/tree/master/data/haarcascades
## Frontal face is used to detect faces looking frontally into the image. 
## It will not detect the face if tilted or not frontal
face_cascade = cv2.CascadeClassifier('haarCascadesXML/haarcascade_frontalface_default.xml')
## eye_cascade
eye_cascade = cv2.CascadeClassifier('haarCascadesXML/haarcascade_eye.xml')

## Optionally we could try to use other databases
## Detecting left and right eyes independently sounds like a great idea but didn't perform well during this particular application
#eye_pair_cascade = cv2.CascadeClassifier('haarCascadesXML/haarcascade_mcs_eyepair_small.xml')
#eye_right_cascade = cv2.CascadeClassifier('haarCascadesXML/haarcascade_mcs_righteye.xml')
#eye_left_cascade = cv2.CascadeClassifier('haarCascadesXML/haarcascade_mcs_lefteye.xml')

# Reduce scale of the image when processing to compute faster. 
# This module has been tested with images that were already very low quality (few kb, 20% jpeg compression, 240p)
# Therefore too much scaling down is not required, and could actually screw things up
# 0.7 seems to be quite a good value
scale = 0.7

## Hardcoded RGB colors to play with for drawing rectangles around the eyes
green =  ( 0   , 255  , 0     )
red   =  ( 0   , 0    , 255   )
blue  =  ( 255 , 0    , 0     )

## Haar detectors take as input maximum and minimum expected area of the pattern to detect
## Adjust to scale
## This sizes are optimized for images taken from a webcam in front of the user
## Other kind of images may have different scales
faceMinSize = int(60*scale)
faceMaxSize = int(300*scale)
eyesMinSize = int(12*scale)
eyesMaxSize = int(40*scale)


def detectEyes(img):
    ## Takes OpenCV formatted image, converts it to greyscale, detects eyes
    ## Returns eyesX, eyesY coordinates, image with green rectangles around eyes

    # Initialize eyes location to -1 (not found)
    # If we find them, we will change this value
    eyesX = -1
    eyesY = -1

    # Convert to grey and equalize 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    # Make image smaller
    ## Resizing image to improve performance is generally very stupid
    ## The resizing itself takes some time
    ## However Haar detectors are very CPU intensive
    ## And it scales exponentially with area
    ## Performance comparisons show this makes sense here
    gray = cv2.resize(gray, (0,0), fx=scale, fy=scale)

    ## Initialize Haar cascade to detect human faces 
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=6, minSize=(faceMinSize, faceMinSize), maxSize=(faceMaxSize, faceMaxSize)) 

    # It may have found more than one face (Sometimes small background complex patterns sneak in as faces)
    # Just take the face of maximum area	
    foundFlag = False
    if (list(faces)):
        areaFaceFound = 0
        for (x,y,w,h) in faces:
            if (w*h > areaFaceFound):
                foundFace =  [[x,y,w,h]]
        foundFlag = True

        ## I know, it seems like foundFlag is always true, but strange bugs when it's not checked 
        if (foundFlag):
            ## We should have detected ONE face at this point
            for (x,y,w,h) in foundFace:
                ## Take ROI (Region of Interest) of the face only, so we don't look for eyes outside the face
                roi_gray = gray[y:int(y+(0.7*h)), int(x + (0.0*w)):int(x + (1.0*w))]
                roi_gray = cv2.equalizeHist(roi_gray)

                ## Draw rectangle around face in color image img
                roi_color = img[int(y/scale):int((y+h)/scale), int(x/scale):int((x+w)/scale)]
                cv2.rectangle(img,(int(x/scale),int(y/scale)),(int((x+w)/scale),int((y+h)/scale)),green,1)

                ## DETECT EYES INSIDE FACE AREA
                ## 3 methods have been tried
                ## 1) Look for eyes one by one with a general pattern, without taking right and left eye shape differences into account
                ## 2) Look for eye pairs (one pattern consisting of the two eyes)
                ## 3) Look for right eyes and left eyes using a different pattern for each eye
        # ########################################################################################################
        # 1
        # Detecting all eyes in the face region at the same time
        # This seems like the less logical way to do it
        # But somehow it is the most stable		
        
                eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor= 1.01, minSize=(eyesMinSize,eyesMinSize), maxSize=(eyesMaxSize,eyesMaxSize))
                
        if (len(eyes) == 2): 
                ## Great, we found exactly two eyes. If more or less we return without detecting eyes (something went wrong)
                for (ex,ey,ew,eh) in eyes:
                        ## Draw a rectangle around each eye in color image img
                        cv2.rectangle(roi_color,(int(ex/scale),int(ey/scale)),(int((ex+ew)/scale),int((ey+eh)/scale)),green,2)


            ## We have detected the eyes
            ## Translate local coordinates (respective to the face ROI) into image coordinates

            (faceX, faceY, faceW, faceH) = (x,y,w,h)
            (aX,aY, aW, aH) = eyes[0]
            (bX,bY, bW, bH) = eyes[1]
            aX = int(aX + 0.5*aW)
            aY = int(aY + 0.5*aH)
            bX = int(bX + 0.5*bW)
            bY = int(bY + 0.5*bH)

            eyesX = faceX + int( 0.5 * (aX+bX))
            eyesY = faceY + int( 0.5 * (aY+bY))
            eyesX = int(eyesX/scale)
            eyesY = int(eyesY/scale)
        
        # ######################################################################################################
        # 2
        # Detecting two pairs at the same time in pairs would make much more sense
        # But it is extremely unstable, giving segfaults out of nowhere as soon as we change anything
        # Maybe there is something wrong with the XML file for eyepairs?
        #
        # eyes_pair = eye_pair_cascade.detectMultiScale(roi_gray, scaleFactor= 1.01)
                # for (ex,ey,ew,eh) in eyes_pair:
                    #cv2.rectangle(roi_color,(int(ex/scale),int(ey/scale)),(int((ex+eh)/scale),int((ey+ew)/scale)),green,2)

        # ######################################################################################################
        # 3
        # Detecting both eyes separetely with two different Haar cascades (a separate XML file for left and right) would also make sense
        # But if we can get by using only one detector and it works, why use 2?
        #
                # roi_gray_left = gray[y:int(y+(0.7*h)), x:int(x+(0.5*w))]
                # roi_gray_left = cv2.equalizeHist(roi_gray_left)
                #
                # roi_gray_right = gray[y:int(y+(0.7*h)), int(x+(0.5*w)):x+w]
                # roi_gray_right = cv2.equalizeHist(roi_gray_right)
                #
                # eyes_left = eye_cascade_left.detectMultiScale(roi_gray_left, scaleFactor=1.01, minSize=(eyesMinSize,eyesMinSize))
                # for (ex,ey,ew,eh) in eyes_left:
                # 	cv2.rectangle(roi_color,(int(ex/scale),int(ey/scale)),(int((ex+ew)/scale),int((ey+eh)/scale)),blue,2)
                #
                # eyes_right = eye_cascade_right.detectMultiScale(roi_gray_right, scaleFactor=1.01, minSize=(eyesMinSize,eyesMinSize))
                # for (ex,ey,ew,eh) in eyes_right:
                # 	cv2.rectangle(roi_color,(int(ex/scale),int(ey/scale)),(int((ex+ew)/scale),int((ey+eh)/scale)),red,2)

    return img, eyesX, eyesY

###############################################################################################################################
def encodeImage(img):
    ## Encode into jpeg format
    ## Input: openCV formatted image
    ## Output: Encoded image, retval (error flag)
    jpg_encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
    retval, encImg = cv2.imencode(".jpg",img,jpg_encode_param)
    return retval,encImg



