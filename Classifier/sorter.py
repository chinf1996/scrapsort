# import servo
# import ui
from ImageProcessing.camera import Camera
from vision import Classifier
from ImageProcessing import motiondetector
import time 
import brain
# from databasehelper import Database
import os
from Steper.vendor.StepMotor import StepMotor

middle_step = 1050
final_step = 2080
delay = 6/1000

def sort_trash(imgpath):
	camera = Camera()
	# database = Database()
	classifier = Classifier(os.path.abspath('Tf_classifier/trained_graph.pb'), os.path.abspath('Tf_classifier/output_labels.txt'))

	# statusThread = ui.start_status_shower_thread()
	stepmotor = StepMotor()
	while True:
		

		# wait for camera to detect motion, then sleep for a bit to
		# let the object settle down
		print ("waiting for motion...")
		motiondetector.waitForMotionDetection(camera.getPiCamera())
		time.sleep(0.5) # Lets object settle down, TODO maybe remove
		
		print ("detected motion")

		

		# take a photo and classify it
		camera.takePhoto(imgpath)
		labels = classifier.get_image_labels(imgpath)
		print (labels)
		selectedLabel = brain.getRecyclingLabel(labels)
		is_trash = selectedLabel == None

		
		

		if is_trash:
			print("It's trash.")
			# ui.set_status("trash")
			# servo.move(TRASH_POS)
		else:
			print("It's recyclable.")
			if str(selectedLabel).find('plastic') != -1 or str(selectedLabel).find('glass') != -1:
				stepmotor.forward(delay,middle_step)
				time.sleep(1)
				stepmotor.backward(delay,middle_step)
			elif str(selectedLabel).find('paper') != -1 :
				stepmotor.forward(delay,final_step)
				time.sleep(1)
				stepmotor.backward(delay,final_step)


def main():
	sort_trash('ImageProcessing/img/classificationImage.jpg')

if __name__ == '__main__':
	main()