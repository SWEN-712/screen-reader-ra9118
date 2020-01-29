#https://towardsdatascience.com/object-detection-with-less-than-10-lines-of-code-using-python-2d28eebc5b11

#  opencv-python
#  cvlib
#  matplotlib
#  tensorflow
#  keras

import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox

import time
import ctypes


#Load the NVDA client library
clientLib=ctypes.windll.LoadLibrary('nvdaControllerClient64.dll')

#Test if NVDA is running, and if its not show a message
res=clientLib.nvdaController_testIfRunning()
if res!=0:
	errorMessage=str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0,u"Error: %s"%errorMessage,u"Error communicating with NVDA",0)


class ImageAnalysis:
	def findObjectName(self,x,y):
		text=""
		minBox = None
		for i in range(0, len(bbox)):
			box = bbox[i]
			if( box[0]<= x and  box[1]<= y and box[2]>= x and  box[3]>=y ):
				if minBox == None:
					text = label[i]
					minBox = box
				else:
					if (abs( (minBox[0]-minBox[2]) * (minBox[1]-minBox[3]))
							> abs( (box[0]-box[2]) * (box[1]-box[3])) ):
						text = label[i]
						minBox= box
						#print(text)

		print(text)
		clientLib.nvdaController_speakText(text)
		##TODO: call  NVADA API for the process
		#print("---")

	def onclick(self,event):
		#print(event.xdata, event.ydata)
		self.findObjectName(event.xdata, event.ydata)

imageAnalysis = ImageAnalysis()


imagePath = input('Enter image path: ')
im = cv2.imread(imagePath)
#fig = plt.figure()
bbox, label, conf = cv.detect_common_objects(im)
output_image = draw_bbox(im, bbox, label, conf)


objectsNames=[]
for i in range(0,len(bbox)):
	if not( label[i] in str(objectsNames)):
		objectsNames.append(label[i])

	# print(bbox[i])
	# print(label[i])
	# print(conf[i])
	# print("=======")

clientLib.nvdaController_speakText('summary of image content')
clientLib.nvdaController_cancelSpeech()
for name in objectsNames:
	print('Number of '+ name +'s in the image is ' + str(label.count(name)))
	clientLib.nvdaController_speakText('Number of '+ name +'s in the image is ' + str(label.count(name)))
	time.sleep(2.625)
	clientLib.nvdaController_cancelSpeech()


fig,ax = plt.subplots()
ax.plot(range(10))
fig.canvas.mpl_connect('button_press_event', imageAnalysis.onclick)
plt.imshow(output_image)
plt.show()


